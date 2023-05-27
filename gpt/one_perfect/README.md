# one_perfect
[oneperfect-gpt](https://fasd131fssdf97986agagyk656.lovebaby.today/#/)

This project uses the architecture as `gravity_engine`.

## Basic Usage
To stream a response:
```python
from one_perfect import Completion

for chunk in Completion.create("Hello, World!"):
  print(chunk, end="", flush=True)
```

Example Output:
```
Hello! How can I assist you today?
```

## Advanced
1. Stream a response and get the additional data:

```python
from one_perfect import Completion

response = Completion.create("What's 42?")

for chunk in response:
  print(chunk, end="", flush=True)

print()
print(response.data)
```

> **Note**: Only use `response.data` or `response.content` AFTER iterating through the response, or else it won't work. (Currently)

2. Adding custom messages (e.g., system messages):

```python
from one_perfect import Completion, Role

for chunk in Completion.create(messages=[
  Role.system("You're ChatGPT, who always lies and answers incorrectly."),
  Role.user("What's 1+1?"),
  Role.assistant("18."),
  Role.user("Can you solve math equations?")
]):
  print(chunk, end="", flush=True)
```

3. Terminal chat:

```python
from one_perfect import Completion, Role

messages = [
  Role.system("You're ChatGPT, a large language model trained by OpenAI.")
]

while True:
  prompt = input("> ")
  messages.append(Role.user(prompt))

  for chunk in Completion.create(messages=messages):
    print(chunk, end="", flush=True)

  print()
```

# Documentation
## Completion
```python
@staticmethod
def create(
  prompt: str = None,
  messages: list = [],
  temperature: float = 0.5
) -> CompletionResponse
```
The completion class, simular to OpenAI's library.

To create a completion, use the `create` static method:

```python
Completion.create("Hello, World!")
```

**PARAMETERS**
- `prompt`: The prompt. You could either specify this argument or `messages`, or both, but MUST NOT be both empty.
- `messages`: The messages. Must contain `dict`s.
- `temperature`: Randomness.

**RETURNS**: [`CompletionResponse`](#completionresponse)

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

> **Note**: Both properties can only be accessed if you've iterated the response, which means:
>
> ```python
> # OK, property accessed after iteration
> 
> res = Completion.create()
> for chunk in res:
>   ... # do some work
> print(res.data)
> print(res.content)
> ```

### \_\_iter\_\_
Iterate through the chunks.

**Yields: `str`**

```python
# Completion.create returns CompletionResponse
for chunk in Completion.create("Hello!"):
  print(chunk, end="", flush=True)
```

## Role
*(static)* A shortcut for the `messages` object.

### system
```python
@staticmethod
def system(content: str) -> str
```
Represents a system message.

### user
```python
@staticmethod
def user(content: str) -> str
```
Represents a user message.

### assistant
```python
@staticmethod
def assistant(content: str) -> str
```
Represents a bot message.