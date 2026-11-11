from __future__ import annotations

import re

# Bytes that end a JSON string, start an escape or are not allowed in one.
_STRING_SPECIAL = re.compile(rb'["\\\x00-\x1f]')
_SIMPLE_ESCAPES = frozenset(b'"\\/bfnrt')
_HEX_DIGITS = frozenset(b"0123456789abcdefABCDEF")


class PartialJsonBuffer:
    """Collects the `partial_json` deltas of one content block.

    `from_json(..., partial_mode=True)` drops a trailing unclosed string, so a delta that only extends
    an open string does not change the parsed value and the buffer does not need to be parsed again.
    Anything that is not valid inside a JSON string marks the buffer as unsafe to skip from then on,
    so that the parser still sees it and raises the same error.
    """

    def __init__(self) -> None:
        self._buf = bytearray()
        self._in_string = False
        self._invalid = False
        # 0: no escape, 1: after a backslash, 2-5: reading the hex digits of `\u`
        self._escape = 0
        self._code = 0
        self._high_surrogate = False

    def __len__(self) -> int:
        return len(self._buf)

    def getvalue(self) -> bytes:
        return bytes(self._buf)

    def feed(self, data: bytes) -> bool:
        """Appends `data` and returns whether it only extended an open string with valid content."""
        self._buf += data
        if self._invalid:
            return False

        extends_open_string = self._in_string
        pos = 0
        end = len(data)
        while pos < end:
            if not self._in_string:
                quote = data.find(b'"', pos)
                if quote < 0:
                    break
                self._in_string = True
                pos = quote + 1
                continue

            char = data[pos]
            if self._escape == 0:
                if self._high_surrogate and char != 0x5C:  # a high surrogate must be followed by `\u`
                    self._invalid = True
                    return False
                match = _STRING_SPECIAL.search(data, pos)
                if match is None:
                    break
                pos = match.end()
                char = data[pos - 1]
                if char == 0x22:  # '"'
                    self._in_string = False
                    extends_open_string = False
                elif char == 0x5C:  # '\\'
                    self._escape = 1
                else:
                    self._invalid = True
                    return False
            elif self._escape == 1:
                pos += 1
                if char == 0x75:  # 'u'
                    self._escape = 2
                    self._code = 0
                elif char in _SIMPLE_ESCAPES and not self._high_surrogate:
                    self._escape = 0
                else:
                    self._invalid = True
                    return False
            else:
                pos += 1
                if char not in _HEX_DIGITS:
                    self._invalid = True
                    return False
                self._code = self._code * 16 + int(chr(char), 16)
                self._escape += 1
                if self._escape == 6:
                    self._escape = 0
                    is_high = 0xD800 <= self._code <= 0xDBFF
                    is_low = 0xDC00 <= self._code <= 0xDFFF
                    if self._high_surrogate != is_low:
                        self._invalid = True
                        return False
                    self._high_surrogate = is_high

        return extends_open_string
