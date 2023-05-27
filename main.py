from gpt.chatbase import Completion, Role

messages = []
while True:
  messages.append(Role.user(input("> ")))

  gathered = ""
  for chunk in Completion.create(messages):
    print(chunk, end="", flush=True)
    gathered += chunk
  messages.append(Role.assistant(gathered))

  print()