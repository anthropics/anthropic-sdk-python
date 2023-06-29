# Anthropic

Methods:

- <code>client.<a href="./src/anthropic/_client.py">count_tokens</a>(\*args) -> int</code>

# Completions

Types:

```python
from anthropic.types import Completion
```

Methods:

- <code title="post /v1/complete">client.completions.<a href="./src/anthropic/resources/completions.py">create</a>(\*\*<a href="src/anthropic/types/completion_create_params.py">params</a>) -> <a href="./src/anthropic/types/completion.py">Completion</a></code>
