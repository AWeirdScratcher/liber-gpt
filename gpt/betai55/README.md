# betai55
[b1.betai55.uk](b1.betai55.uk)

> **Note**: Chinese site.

## Basic Usage
To stream a response:

```python
from betai55 import Completion, Role

for chunk in Completion.create([
  Role.user("How can you assist me today?")
]):
  print(chunk, end="", flush=True) 
```

## Advanced
1. Get the content without streaming:
```python
from betai55 import Completion, Role

res = Completion.create([Role.user("hi")])
print(res.content)
```

2. Terminal chat:
```python
from betai55 import Completion, Role

messages = [
  Role.system("You're ChatGPT, a large language model trained by OpenAI.")
]
while True:
  messages.append(
    Role.user(input("> "))
  )
  fetched = ""
  for chunk in Completion.create(messages):
    print(chunk, end="", flush=True)
    fetched += chunk
  messages.append(Role.assistant(fetched))
  
  print() # next line
```

# Documentation
## Completion
```python
@staticmethod
def create(
  messages: list[dict],
  temperature: float = 1.0,
  persence_penalty: float = 0.0
) -> CompletionResponse
```
Create a completion.

**PARAMETERS**
- `messages`: Messages object.
- `temperature`: Randomess.
- `presence_penalty`: The probabilty of switching the topics.

**RETURNS**: `CompletionResponse`

## CompletionResponse
```python
def __init__(self, req: Request)
```
The completion response.

**PROPERTIES**
- `content`: The text content without streaming.

### \_\_iter\_\_
```python
def __iter__(self)
```
Iterate through the chunks.

**Yields**: `str`
