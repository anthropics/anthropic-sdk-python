from typing import Dict, AsyncIterator, Iterator, Optional, Tuple, NamedTuple, Union
import aiohttp
import logging
import requests
import requests.adapters
import urllib.parse
import json

from . import constants


class ApiException(Exception):
    pass


class Request(NamedTuple):
    method: str
    url: str
    headers: Optional[Dict[str, str]]
    data: bytes
    stream: bool
    timeout: Optional[Union[float, Tuple[float, float]]]


def _process_request_error(method: str, content: str, status_code: int):
    try:
        formatted_content = json.loads(content)
    except json.decoder.JSONDecodeError:
        formatted_content = content
    raise ApiException(
        f"{method} request failed with status code: {status_code}",
        formatted_content,
    )


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

    def _request_params(
        self,
        headers: Optional[Dict[str, str]],
        method: str,
        params: dict,
        path: str,
        request_timeout: Optional[Union[float, Tuple[float, float]]],
    ) -> Request:
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
        return Request(
            method,
            abs_url,
            final_headers,
            data,
            stream,
            request_timeout or self.default_request_timeout,
        )

    def _request_raw(
        self,
        method: str,
        path: str,
        params: dict,
        headers: Optional[Dict[str, str]] = None,
        request_timeout: Optional[Union[float, Tuple[float, float]]] = None,
    ) -> requests.Response:
        request = self._request_params(headers, method, params, path, request_timeout)
        result = self._session.request(
            request.method,
            request.url,
            headers=request.headers,
            data=request.data,
            stream=request.stream,
            timeout=request.timeout,
        )

        if result.status_code != 200:
            _process_request_error(
                method, result.content.decode("utf-8"), result.status_code
            )
        return result

    async def _arequest_as_json(
        self,
        method: str,
        path: str,
        params: dict,
        headers: Optional[Dict[str, str]] = None,
        request_timeout: Optional[Union[float, Tuple[float, float]]] = None,
    ) -> dict:
        request = self._request_params(headers, method, params, path, request_timeout)
        async with aiohttp.ClientSession() as session:
            async with session.request(
                request.method,
                request.url,
                headers=request.headers,
                data=request.data,
                timeout=request.timeout,
            ) as result:
                content = await result.text()
                if result.status != 200:
                    _process_request_error(method, content, result.status)
                json_body = json.loads(content)
                return json_body

    async def _arequest_as_stream(
        self,
        method: str,
        path: str,
        params: dict,
        headers: Optional[Dict[str, str]] = None,
        request_timeout: Optional[Union[float, Tuple[float, float]]] = None,
    ) -> AsyncIterator[dict]:
        request = self._request_params(headers, method, params, path, request_timeout)
        awaiting_ping_data = False
        async with aiohttp.ClientSession() as session:
            async with session.request(
                request.method,
                request.url,
                headers=request.headers,
                data=request.data,
                timeout=request.timeout,
            ) as result:
                if result.status != 200:
                    _process_request_error(method, await result.text(), result.status)
                async for line in result.content:
                    line = line.strip()
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
                    yield json.loads(line)

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

    async def acompletion(self, **kwargs) -> dict:
        return await self._arequest_as_json(
            "post",
            "/v1/complete",
            params=kwargs,
        )

    async def acompletion_stream(self, **kwargs) -> AsyncIterator[dict]:
        new_kwargs = {"stream": True, **kwargs}
        return self._arequest_as_stream(
            "post",
            "/v1/complete",
            params=new_kwargs,
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
