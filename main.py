from gpt.usesless import Account, Completion, Context

@Completion.create("Hello, World!")
def callback(chunk: Context):
  print(chunk.content, end="", flush=True)
