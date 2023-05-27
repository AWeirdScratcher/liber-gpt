# aiassist
[aiassist.site](https://aiassist.site)

## Basic Usage
To stream a response:
```python
from aiassist import Completion

for chunk in Completion.create(
  prompt="Hello, World!",
  systemMessage="You're ChatGPT, a large language model trained by OpenAI."):
  print(chunk, end="", flush=True)
```

Example Output:
```
Hello! How can I assist you today?
```

## Advanced
1. Stream a response and get the additional data:

```python
from aiassist import Completion

response = Completion.create("What's 42?")

for chunk in response:
  print(chunk, end="", flush=True)

print()
print(response.data)
```

2. Get the plain data without streaming:

```python
from aiassist import Completion

response = Completion.create("What's 42?")
print(response.content)
```

3. Terminal chat:

```python
from aiassist import Completion

while True:
  for chunk in Completion.create(prompt=input("> "), parentMessageId=parent):
    print(chunk, end="", flush=True)

  print()
```

# Documentation
## Completion
```python
@staticmethod
def create(
  prompt: str,
  systemMessage: str = system,
  parentMessageId: str = "",
  temperature: float = 0.8,
  top_p: float = 1.0
) -> CompletionResponse
```
The completion class, simular to OpenAI's library.

To create a completion, use the `create` static method:

```python
Completion.create("Hello, World!")
```

**Returns: [`CompletionResponse`](#completionresponse)**

## CompletionResponse
```python
def __init__(
  self,
  request: Request
)
```
The completion response.

### Properties
- `content`: The text content (without streaming).
- `data`: Get the additional data (e.g., parent message ID, delta, etc.)

### \_\_iter\_\_
```python
def __iter__(
  self
)
```
Iterate through the chunks.

**Yields: `str`**

```python
# Completion.create returns CompletionResponse
for chunk in Completion.create("Hello!"):
  print(chunk, end="", flush=True)
```
