# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import httpx
import pytest
from respx import MockRouter

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
)
from anthropic.pagination import SyncPage, AsyncPage
from anthropic.types.beta import DeletedFile, FileMetadata

# pyright: reportDeprecated=false

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFiles:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        file = client.beta.files.list()
        assert_matches_type(SyncPage[FileMetadata], file, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        file = client.beta.files.list(
            after_id="after_id",
            before_id="before_id",
            limit=1,
            betas=["string"],
        )
        assert_matches_type(SyncPage[FileMetadata], file, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.files.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = response.parse()
        assert_matches_type(SyncPage[FileMetadata], file, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.files.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = response.parse()
            assert_matches_type(SyncPage[FileMetadata], file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Anthropic) -> None:
        file = client.beta.files.delete(
            file_id="file_id",
        )
        assert_matches_type(DeletedFile, file, path=["response"])

    @parametrize
    def test_method_delete_with_all_params(self, client: Anthropic) -> None:
        file = client.beta.files.delete(
            file_id="file_id",
            betas=["string"],
        )
        assert_matches_type(DeletedFile, file, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Anthropic) -> None:
        response = client.beta.files.with_raw_response.delete(
            file_id="file_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = response.parse()
        assert_matches_type(DeletedFile, file, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Anthropic) -> None:
        with client.beta.files.with_streaming_response.delete(
            file_id="file_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = response.parse()
            assert_matches_type(DeletedFile, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_id` but received ''"):
            client.beta.files.with_raw_response.delete(
                file_id="",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_download(self, client: Anthropic, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/files/file_id/content?beta=true").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        file = client.beta.files.download(
            file_id="file_id",
        )
        assert file.is_closed
        assert file.json() == {"foo": "bar"}
        assert cast(Any, file.is_closed) is True
        assert isinstance(file, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_download_with_all_params(self, client: Anthropic, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/files/file_id/content?beta=true").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        file = client.beta.files.download(
            file_id="file_id",
            betas=["string"],
        )
        assert file.is_closed
        assert file.json() == {"foo": "bar"}
        assert cast(Any, file.is_closed) is True
        assert isinstance(file, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_download(self, client: Anthropic, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/files/file_id/content?beta=true").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        file = client.beta.files.with_raw_response.download(
            file_id="file_id",
        )

        assert file.is_closed is True
        assert file.http_request.headers.get("X-Stainless-Lang") == "python"
        assert file.json() == {"foo": "bar"}
        assert isinstance(file, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_download(self, client: Anthropic, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/files/file_id/content?beta=true").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.beta.files.with_streaming_response.download(
            file_id="file_id",
        ) as file:
            assert not file.is_closed
            assert file.http_request.headers.get("X-Stainless-Lang") == "python"

            assert file.json() == {"foo": "bar"}
            assert cast(Any, file.is_closed) is True
            assert isinstance(file, StreamedBinaryAPIResponse)

        assert cast(Any, file.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_download(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_id` but received ''"):
            client.beta.files.with_raw_response.download(
                file_id="",
            )

    @parametrize
    def test_method_retrieve_metadata(self, client: Anthropic) -> None:
        file = client.beta.files.retrieve_metadata(
            file_id="file_id",
        )
        assert_matches_type(FileMetadata, file, path=["response"])

    @parametrize
    def test_method_retrieve_metadata_with_all_params(self, client: Anthropic) -> None:
        file = client.beta.files.retrieve_metadata(
            file_id="file_id",
            betas=["string"],
        )
        assert_matches_type(FileMetadata, file, path=["response"])

    @parametrize
    def test_raw_response_retrieve_metadata(self, client: Anthropic) -> None:
        response = client.beta.files.with_raw_response.retrieve_metadata(
            file_id="file_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = response.parse()
        assert_matches_type(FileMetadata, file, path=["response"])

    @parametrize
    def test_streaming_response_retrieve_metadata(self, client: Anthropic) -> None:
        with client.beta.files.with_streaming_response.retrieve_metadata(
            file_id="file_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = response.parse()
            assert_matches_type(FileMetadata, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve_metadata(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_id` but received ''"):
            client.beta.files.with_raw_response.retrieve_metadata(
                file_id="",
            )

    @parametrize
    def test_method_upload(self, client: Anthropic) -> None:
        file = client.beta.files.upload(
            file=b"raw file contents",
        )
        assert_matches_type(FileMetadata, file, path=["response"])

    @parametrize
    def test_method_upload_with_all_params(self, client: Anthropic) -> None:
        file = client.beta.files.upload(
            file=b"raw file contents",
            betas=["string"],
        )
        assert_matches_type(FileMetadata, file, path=["response"])

    @parametrize
    def test_raw_response_upload(self, client: Anthropic) -> None:
        response = client.beta.files.with_raw_response.upload(
            file=b"raw file contents",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = response.parse()
        assert_matches_type(FileMetadata, file, path=["response"])

    @parametrize
    def test_streaming_response_upload(self, client: Anthropic) -> None:
        with client.beta.files.with_streaming_response.upload(
            file=b"raw file contents",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = response.parse()
            assert_matches_type(FileMetadata, file, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncFiles:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        file = await async_client.beta.files.list()
        assert_matches_type(AsyncPage[FileMetadata], file, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        file = await async_client.beta.files.list(
            after_id="after_id",
            before_id="before_id",
            limit=1,
            betas=["string"],
        )
        assert_matches_type(AsyncPage[FileMetadata], file, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.files.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = response.parse()
        assert_matches_type(AsyncPage[FileMetadata], file, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.files.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = await response.parse()
            assert_matches_type(AsyncPage[FileMetadata], file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncAnthropic) -> None:
        file = await async_client.beta.files.delete(
            file_id="file_id",
        )
        assert_matches_type(DeletedFile, file, path=["response"])

    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncAnthropic) -> None:
        file = await async_client.beta.files.delete(
            file_id="file_id",
            betas=["string"],
        )
        assert_matches_type(DeletedFile, file, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.files.with_raw_response.delete(
            file_id="file_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = response.parse()
        assert_matches_type(DeletedFile, file, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.files.with_streaming_response.delete(
            file_id="file_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = await response.parse()
            assert_matches_type(DeletedFile, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_id` but received ''"):
            await async_client.beta.files.with_raw_response.delete(
                file_id="",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_download(self, async_client: AsyncAnthropic, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/files/file_id/content?beta=true").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        file = await async_client.beta.files.download(
            file_id="file_id",
        )
        assert file.is_closed
        assert await file.json() == {"foo": "bar"}
        assert cast(Any, file.is_closed) is True
        assert isinstance(file, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_download_with_all_params(self, async_client: AsyncAnthropic, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/files/file_id/content?beta=true").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        file = await async_client.beta.files.download(
            file_id="file_id",
            betas=["string"],
        )
        assert file.is_closed
        assert await file.json() == {"foo": "bar"}
        assert cast(Any, file.is_closed) is True
        assert isinstance(file, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_download(self, async_client: AsyncAnthropic, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/files/file_id/content?beta=true").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        file = await async_client.beta.files.with_raw_response.download(
            file_id="file_id",
        )

        assert file.is_closed is True
        assert file.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await file.json() == {"foo": "bar"}
        assert isinstance(file, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_download(self, async_client: AsyncAnthropic, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/files/file_id/content?beta=true").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.beta.files.with_streaming_response.download(
            file_id="file_id",
        ) as file:
            assert not file.is_closed
            assert file.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await file.json() == {"foo": "bar"}
            assert cast(Any, file.is_closed) is True
            assert isinstance(file, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, file.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_download(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_id` but received ''"):
            await async_client.beta.files.with_raw_response.download(
                file_id="",
            )

    @parametrize
    async def test_method_retrieve_metadata(self, async_client: AsyncAnthropic) -> None:
        file = await async_client.beta.files.retrieve_metadata(
            file_id="file_id",
        )
        assert_matches_type(FileMetadata, file, path=["response"])

    @parametrize
    async def test_method_retrieve_metadata_with_all_params(self, async_client: AsyncAnthropic) -> None:
        file = await async_client.beta.files.retrieve_metadata(
            file_id="file_id",
            betas=["string"],
        )
        assert_matches_type(FileMetadata, file, path=["response"])

    @parametrize
    async def test_raw_response_retrieve_metadata(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.files.with_raw_response.retrieve_metadata(
            file_id="file_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = response.parse()
        assert_matches_type(FileMetadata, file, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve_metadata(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.files.with_streaming_response.retrieve_metadata(
            file_id="file_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = await response.parse()
            assert_matches_type(FileMetadata, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve_metadata(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_id` but received ''"):
            await async_client.beta.files.with_raw_response.retrieve_metadata(
                file_id="",
            )

    @parametrize
    async def test_method_upload(self, async_client: AsyncAnthropic) -> None:
        file = await async_client.beta.files.upload(
            file=b"raw file contents",
        )
        assert_matches_type(FileMetadata, file, path=["response"])

    @parametrize
    async def test_method_upload_with_all_params(self, async_client: AsyncAnthropic) -> None:
        file = await async_client.beta.files.upload(
            file=b"raw file contents",
            betas=["string"],
        )
        assert_matches_type(FileMetadata, file, path=["response"])

    @parametrize
    async def test_raw_response_upload(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.files.with_raw_response.upload(
            file=b"raw file contents",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = response.parse()
        assert_matches_type(FileMetadata, file, path=["response"])

    @parametrize
    async def test_streaming_response_upload(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.files.with_streaming_response.upload(
            file=b"raw file contents",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = await response.parse()
            assert_matches_type(FileMetadata, file, path=["response"])

        assert cast(Any, response.is_closed) is True
