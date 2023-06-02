# usesless
[ai.usesless.com](https://ai.usesless.com)

> **Note**: Logins are supported.

## Basic Usage
Here's a basic demo on how you can use the basic completion method:

```python
from usesless import DelayedCompletion, Account

account = Account() # initialize an account, takes a while
for chunk in DelayedCompletion.create("Hello, World!", account=account):
  print(chunk.content, end="", flush=True)
```

However, this method might not be ideal when it comes to large projects such as APIs, as it uses `time.sleep` as an interval approach to check for the (verification) email. Use `Completion` instead. Also, we're looking for a developer who're willing to help us to implement coroutine methods.

Additionally, when you are initializing a new account, a new file (`tokens.txt`) will pop up. This is used to prevent a "request hell", and re-use the tokens if available.

## Advanced
1. Using the `Completion` class:
```python
from usesless import Completion, Account, Context

print("Creating account...")
account = Account()

@Completion.create("Knock knock.", account=account)
def callback(ctx: Context):
  print(ctx.content, end="", flush=True)

  if ctx.finished:
    print()
    print("IP Chat Count:", ctx.ip_chat_count)

print("(end of code)\n")
```

Output:
```
Creating account...
(end of code)

Who's there?
IP Chat Count: 1
```

2. Terminal Chat:
```python
from usesless import DelayedCompletion, Account

print("Initializing account...")
account = Account()
parent = None

while True:
  prompt = input("Q: ")
  print("A: ", end="")

  for chunk in DelayedCompletion.create(prompt, account, parentMessageId=parent):
    print(chunk.content, end="", flush=True)
    if chunk.finished:
      parent = chunk.parent
      print()
```

## Things to note
1. To disable the warning messages, try:

```python
import usesless

# monkey patching
usesless.no_warnings = True
```
<details>
  <summary>2. Coming Soon...</summary>

We will add a new parameter (`proxies`) for both of the completion methods (Completion, DelayedCompletion). Here's an example:

```python
http_proxy  = "http://10.10.1.10:9012"
https_proxy = "https://10.10.1.11:5678"
ftp_proxy   = "ftp://10.10.1.10:1234"

proxies = { 
  "http"  : http_proxy, 
  "https" : https_proxy, 
  "ftp"   : ftp_proxy
}
# from https://stackoverflow.com/questions/8287628/proxies-with-python-requests-module
```

</details>

# Documentation
## DelayedCompletion
```python
@staticmethod
def create(
  prompt: str,
  account: Account = None,
  systemMessage: str = None,
  presence_penalty: float = 0,
  temperature: float = 1.0,
  parentMessageId: str = None
)
```
A delayed completion (generator) that uses thr `time.sleep` approach to receive emails with an interval.

**PARAMETERS**
- `prompt`: The prompt.
- `account`: An initialize account class. Although it's optional, we still recommend initializing your own. (opt)
- `systemMessage`: The system message. Optional. (opt)
- `presence_penalty`: The probability of switching topics. (opt)
- `temperature`: Randomness. (opt)
- `parentMessageId`: The parent message ID. Could be accessed with `Context.parent`. (opt)

Example:
```python
for chunk in DelayedCompletion.create("knock knock"):
  print(chunk.content, end="", flush=True)
```

## Completion
```python
@staticmethod
def create(
  prompt: str,
  account: Account = None,
  systemMessage: str = None,
  presence_penalty: float = 0,
  temperature: float = 1.0,
  parentMessageId: str = None
)
```
A non-delaying completion session to avoid race conditions.

**PARAMETERS**

Same as the above (`DelayedCompletion`).

Example:
```python
from usesless import Context

@Completion.create("Hi!")
def callback(ctx: Context):
  print(ctx.content, end="", flush=True)
```

## Account
```python
def __init__(
  self, 
  auto_load: bool = True, 
  save_token: bool = True
)
```
An account session.

**PARAMETERS**
- `auto_load`: Whether to automatically load the tokens from the pre-generated `tokens.txt` file or not. (opt, True)
- `save_token`: Whether to save the generated token to the `tokens.txt` file for later use or not. (opt, True)

## Context *(model)*
The context model that both Completion and DelayedCompletion uses.

- `parent`: The parent message ID.
- `content`: The delta.
- `ip_chat_count`: IP chat count.
- `used_integral`: Used integral.
- `finished`: Whether the session has finished or not.

### \_\_repr\_\_
```python
<class Context parent=str content=str ip_chat_count=int used_integral=int finished=bool>
```