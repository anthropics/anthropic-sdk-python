# `respx` (used by our test-suite) is typed against `httpx`, while this SDK is built on `httpx2`.
# At runtime the tests alias `httpx` to `httpx2` (see `tests/_alias_httpx.py`); this stub does the
# same for pyright (whose `stubPath` defaults to `typings/`), so that e.g.
# `respx_mock.get(...).mock(return_value=httpx2.Response(...))` type-checks.
from httpx2 import *
from httpx2 import _client as _client
