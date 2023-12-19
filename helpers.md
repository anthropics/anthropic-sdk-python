# Message Helpers

## Streaming Responses

```python
async with client.beta.messages.stream(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Say hello there!",
        }
    ],
    model="claude-2.1",
) as stream:
    async for text in stream.text_stream:
        print(text, end="", flush=True)
    print()
```

`client.beta.messages.stream()` returns a `MessageStreamManager`, which is a context manager that yields a `MessageStream` which is iterable, emits events and accumulates messages.

Alternatively, you can use `client.beta.messages.create(..., stream=True)` which returns an
iteratable of the events in the stream and uses less memory (most notably, it does not accumulate a final message
object for you).

The stream will be cancelled when the context manager exits but you can also close it prematurely by calling `stream.close()`.

See an example of streaming helpers in action in [`examples/messages_stream.py`](examples/messages_stream.py) and defining custom event handlers in [`examples/messages_stream_handler.py`](examples/messages_stream_handler.py)

> [!NOTE]  
> The synchronous client has the same interface just without `async/await`.

### Lenses

#### `.text_stream`

Provides an iterator over just the text deltas in the stream:

```py
async for text in stream.text_stream:
    print(text, end="", flush=True)
print()
```

### Events

#### `await on_stream_event(event: MessageStreamEvent)`

The event is fired when an event is received from the API.

#### `await on_message(message: Message)`

The event is fired when a full Message object has been accumulated. This corresponds to the `message_stop` SSE.

#### `await on_content_block(content_block: ContentBlock)`

The event is fired when a full ContentBlock object has been accumulated. This corresponds to the `content_block_stop` SSE.

#### `await on_text(text: str, snapshot: str)`

The event is fired when a `text` ContentBlock object is being accumulated. The first argument is the text delta and the second is the current accumulated text, for example:

```py
on_text('Hello', 'Hello')
on_text(' there', 'Hello there')
on_text('!', 'Hello there!')
```

This corresponds to the `content_block_delta` SSE.

#### `await on_exception(exception: Exception)`

The event is fired when an exception is encountered while streaming the response.

#### `await on_timeout()`

The event is fired when the request times out.

#### `await on_end()`

The last event fired in the stream.

### Methods

#### `await .close()`

Aborts the request.

#### `await .until_done()`

Blocks until the stream has been read to completion.

#### `await .get_final_message()`

Blocks until the stream has been read to completion and returns the accumulated `Message` object.

#### `await .get_final_text()`

> [!NOTE]  
> Currently the API will only ever return 1 content block

Blocks until the stream has been read to completion and returns all `text` content blocks concatenated together.
