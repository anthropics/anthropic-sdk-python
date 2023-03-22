from typing import Dict, Iterator, Optional, Tuple, Union
import requests
import requests.adapters
import urllib.parse
import json
from . import constants
from . import tokenizer

class ApiException(Exception):
    pass

class Client:
    def __init__(
        self,
        api_key: str,
        api_url: str = "https://api.anthropic.com",
        proxy_url: Optional[str] = None,
        default_request_timeout: Optional[Union[float, Tuple[float, float]]] = 600,
    ):
        self.api_key = api_key
        self.api_url = api_url
        self.proxy_url = proxy_url
        self.max_connection_retries = 2
        self.default_request_timeout = default_request_timeout
        self._session = self._setup_session()

    def _setup_session(self) -> requests.Session:
        self._session = requests.Session()
        if self.proxy_url:
            self._session.proxies = {"https": self.proxy_url}
        self._session.mount(
            "https://",
            requests.adapters.HTTPAdapter(max_retries=self.max_connection_retries),
        )
        return self._session

    def _request_raw(
        self,
        method: str,
        path: str,
        params: dict,
        headers: Optional[Dict[str, str]] = None,
        request_timeout: Optional[Union[float, Tuple[float, float]]] = None,
    ) -> requests.Response:
        method = method.lower()

        abs_url = urllib.parse.urljoin(self.api_url, path)
        final_headers: dict[str, str] = {
            "Accept": "application/json",
            "Client": constants.ANTHROPIC_CLIENT_VERSION,
            "X-API-Key": self.api_key,
            **(headers or {}),
        }

        if params.get("disable_checks"):
            del params["disable_checks"]
        else:
            # NOTE: disabling_checks can lead to very poor sampling quality from our API.
            # _Please_ read the docs on "Claude instructions when using the API" before disabling this.
            # Also note, future versions of the API will enforce these as hard constraints automatically,
            # so please consider these SDK-side checks as things you'll need to handle regardless.
            _validate_request(params)

        data = None
        if params:
            if method in {"get"}:
                encoded_params = urllib.parse.urlencode(
                    [(k, v) for k, v in params.items() if v is not None]
                )
                abs_url += "&%s" % encoded_params
            elif method in {"post", "put"}:
                data = json.dumps(params).encode()
                final_headers["Content-Type"] = "application/json"
            else:
                raise ValueError(f"Unrecognized method: {method}")

        # If we're requesting a stream from the server, let's tell requests to expect the same
        stream = params.get("stream", None)
        result = self._session.request(
            method,
            abs_url,
            headers=final_headers,
            data=data,
            stream=stream,
            timeout=request_timeout
            if request_timeout
            else self.default_request_timeout,
        )
        if result.status_code != 200:
            content = result.content.decode("utf-8")
            try:
                formatted_content = json.loads(content)
            except json.decoder.JSONDecodeError:
                formatted_content = content
            raise ApiException(
                f'{method} request failed with status code: {result.status_code}',
                formatted_content
            )
        return result

    def _request_as_json(self, *args, **kwargs) -> dict:
        result = self._request_raw(*args, **kwargs)
        content = result.content.decode("utf-8")
        json_body = json.loads(content)
        return json_body

    def _request_as_stream(self, *args, **kwargs) -> Iterator[dict]:
        result = self._request_raw(*args, **kwargs)

        awaiting_ping_data = False
        for line in result.iter_lines():
            if not line:
                continue
            if line == b"event: ping":
                awaiting_ping_data = True
                continue
            if awaiting_ping_data:
                awaiting_ping_data = False
                continue

            if line == b"data: [DONE]":
                continue
            line = line.decode("utf-8")

            prefix = "data: "
            if line.startswith(prefix):
                line = line[len(prefix) :]
            try:
                json_body = json.loads(line)
            except json.decoder.JSONDecodeError as e:
                raise ApiException(e, f"Error processing stream data", line)
            yield json_body

    def completion_stream(self, **kwargs) -> Iterator[dict]:
        new_kwargs = {"stream": True, **kwargs}
        return self._request_as_stream(
            "post",
            "/v1/complete",
            params=new_kwargs,
        )

    def completion(self, **kwargs) -> dict:
        return self._request_as_json(
            "post",
            "/v1/complete",
            params=kwargs,
        )

def _validate_request(params: dict) -> None:
    prompt: str = params["prompt"]
    if not prompt.startswith(constants.HUMAN_PROMPT):
        raise ApiException(
            f"Prompt must start with anthropic.HUMAN_PROMPT ({repr(constants.HUMAN_PROMPT)})"
        )
    if constants.AI_PROMPT not in prompt:
        raise ApiException(
            f"Prompt must contain anthropic.AI_PROMPT ({repr(constants.AI_PROMPT)})"
        )
    if prompt.endswith(" "):
        raise ApiException(f"Prompt must not end with a space character")
    _validate_prompt_length(params)

def _validate_prompt_length(params: dict) -> None:
    prompt: str = params["prompt"]
    prompt_tokens = tokenizer.count_tokens(prompt)
    max_tokens_to_sample: int = params["max_tokens_to_sample"]
    token_limit = 9 * 1024
    if prompt_tokens + max_tokens_to_sample > token_limit:
        raise ApiException(
            f"Prompt tokens ({prompt_tokens}) + max-sampled tokens ({max_tokens_to_sample}) exceeds max ({token_limit})",
        )
