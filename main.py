from gpt.chatbase import Completion, Role

for chunk in Completion.create([
  Role.user("Who are you?")
]):
  print(chunk, end="", flush=True)