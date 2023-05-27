# chatbase
[chatbase.co](https://chatbase.co/)

We've cleaned up the original system prompt (which is the Chatbase official bot) by creating our own for this model.

It's worth noting that Chatbase will automatically delete bots that're inactive for 7 days, so please support us by chatting with our bot ;)

Rate limit: 20000 messages every second (P.S. Although it's set, chatbase will probably sneakly add THEIR rate limit on their APIs)

[→ Chat With Our Bot](https://www.chatbase.co/chatbot-iframe/0nmlH49YOz2t8e7urE9QA)

## Basic Usage
To stream a response:
```python
from chatbase import Completion, Role

for chunk in Completion.create([
  Role.user("Hello!")
]):
  print(chunk, end="", flush=True)
```

Example Output:
```
Hello! How can I assist you today?
```

## Advanced
1. Get the plain data without streaming:

```python
from aiassist import Completion, Role

response = Completion.create([
  Role.user("What's 42?")
])
print(response.content)
```

2. Terminal chat:
```python
from aiassist import Completion, Role

messages = []
while True:
  messages.append(Role.user(input("> ")))

  gathered = ""
  for chunk in Completion.create(messages):
    print(chunk, end="", flush=True)
    gathered += chunk
  messages.append(Role.assistant(gathered))

  print()
```
