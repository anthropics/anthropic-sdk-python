from anthropic.lib.bedrock._stream_decoder import AWSEventStreamDecoder


def test_build_sse_uses_payload_type() -> None:
    decoder = AWSEventStreamDecoder()

    sse = decoder._build_sse('{"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"hi"}}')

    assert sse is not None
    assert sse.event == "content_block_delta"
    assert sse.json() == {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "hi"}}


def test_build_sse_drops_non_message_payloads() -> None:
    decoder = AWSEventStreamDecoder()

    sse = decoder._build_sse('{"amazon-bedrock-invocationMetrics":{"inputTokenCount":1}}')

    assert sse is None
