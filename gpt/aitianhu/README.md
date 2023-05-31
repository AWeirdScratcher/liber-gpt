# aitianhu
[aitianhu.com](https://aitianhu.com)

## Basic Usage
```py
from aitianhu import Completion

for chunk in Completion.create("knock knock"):
  print(chunk, end="", flush=True)
```

Example response:
```
Who's there?
```

## Advanced
1. Get the content without streaming:
```py
from aitianhu import Completion

res = Completion.create("knock knock")
print(res.content)
```

2. Get additional information with streaming:
```py
from aitianhu import Completion

res = Completion.create("How may you assist me today?")

for chunk in res:
  print(chunk, end="", flush=True)

print()
print(res.data)
```

# Documentation
## Completion
```py
@staticmethod
def create(
  prompt: str,
  conversationId: str = "",
  parentMessageId: str = ""
) -> CompletionResponse
```

Creates a new completion.

**PARAMETERS**
- `prompt`: The prompt.
- `conversationId`: The conversation ID (optional).
- `parentMessageId`: The parent message ID (optional).

**RETURNS**: `CompletionResponse`

## CompletionResponse
```py
def __init__(self, req: Request)
```
The completion response.

**PROPERTIES**
- `content`: Get the content without streaming.
- `data`: Get additional information about the session.

### \_\_iter\_\_
```py
def __iter__(self)
```
Iterate through the chunks.

**YIELDS**: `str`
