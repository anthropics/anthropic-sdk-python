from __future__ import annotations

import httpx


def get_auth_headers(
    *,
    method: str,
    url: str,
    headers: httpx.Headers,
    aws_access_key: str | None,
    aws_secret_key: str | None,
    aws_session_token: str | None,
    region: str | None,
    data: str | None,
) -> dict[str, str]:
    import boto3
    from botocore.auth import SigV4Auth
    from botocore.awsrequest import AWSRequest

    session = boto3.Session(
        region_name=region,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        aws_session_token=aws_session_token,
    )

    # The connection header may be stripped by a proxy somewhere, so the receiver
    # of this message may not see this header, so we remove it from the set of headers
    # that are signed.
    headers = headers.copy()
    del headers["connection"]

    request = AWSRequest(method=method.upper(), url=url, headers=headers, data=data)
    credentials = session.get_credentials()

    signer = SigV4Auth(credentials, "bedrock", session.region_name)
    signer.add_auth(request)

    prepped = request.prepare()

    return {key: value for key, value in dict(prepped.headers).items() if value is not None}
