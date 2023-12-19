import sys
import asyncio
import threading
import concurrent.futures
from multiprocessing import Pool

import pytest

from anthropic import _tokenizers


@pytest.fixture(autouse=True)
def before_test() -> None:
    # clear cache
    _tokenizers._tokenizer = None


def _sync_tokenizer_test() -> None:
    tokenizer = _tokenizers.sync_get_tokenizer()
    encoded_text = tokenizer.encode("hello world")  # type: ignore
    assert len(encoded_text.ids) == 2  # type: ignore


def test_tokenizers_is_not_imported() -> None:
    # note: this test relies on being executed before any of the
    # other tests but is a valuable test to avoid issues like this
    # https://github.com/anthropics/anthropic-sdk-python/issues/280
    assert "tokenizers" not in sys.modules

    _sync_tokenizer_test()

    assert "tokenizers" in sys.modules


def test_threading() -> None:
    failed = False

    def target() -> None:
        nonlocal failed

        try:
            _sync_tokenizer_test()
        except Exception:
            failed = True
            raise

    t1 = threading.Thread(target=target)
    t2 = threading.Thread(target=target)

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    assert not failed


def test_concurrent_futures() -> None:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future1 = executor.submit(_sync_tokenizer_test)
        future2 = executor.submit(_sync_tokenizer_test)

        future1.result()
        future2.result()


def test_multiprocessing() -> None:
    with Pool(processes=10) as pool:
        pool.apply(_sync_tokenizer_test)


async def _async_tokenizer_test() -> None:
    tokenizer = await _tokenizers.async_get_tokenizer()
    encoded_text = tokenizer.encode("hello world")  # type: ignore
    assert len(encoded_text.ids) == 2  # type: ignore


async def test_asyncio_tasks() -> None:
    loop = asyncio.get_event_loop()

    task1 = loop.create_task(_async_tokenizer_test())
    task2 = loop.create_task(_async_tokenizer_test())

    await asyncio.gather(task1, task2)


async def test_asyncio_gather() -> None:
    await asyncio.gather(_async_tokenizer_test(), _async_tokenizer_test())
