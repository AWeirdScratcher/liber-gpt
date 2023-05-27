import requests

class Completion:
  @staticmethod
  def create(prompt: str, replaceSettings: bool = True):
    res = requests.post("https://api.xjai.cc:3007/api/chat-process",
                        json={
                          "prompt": prompt,
                          "type": "text",
                          "options": {},
                          "key": ""
                        },
                        headers={"origin": "https://f12.xjai.cc"},
                        stream=True)

    fetched = ""
    splitter = "&KFw6loC9Qvy&"
    s = len(splitter) + 1
    contents = []

    for chunk in res.iter_content():
      payload = chunk.decode('utf-8', 'ignore')
      if replaceSettings:
        payload = payload\
          .replace("小杰AI", " ChatGPT ")\
          .replace("China", "OpenAI")
      fetched += payload

      if fetched.endswith(splitter):
        if len(contents) in [0, 1]:
          contents.append(fetched[:-s])
          fetched = ""

      if len(contents) == 1: # already begins

        if payload.startswith("&"):
          payload = payload[1:]

        if not "https://xcdn.52chye.cn/static/image/zanshangma.jpeg" in payload:
          # ad blocker
          yield payload

class Image:
  @staticmethod
  def create(prompt: str) -> str:
    #image&KFw6loC9Qvy&
    res = requests.post("https://api.xjai.cc:3007/api/chat-process",
                        json={
                          "prompt": prompt,
                          "type": "image",
                          "options": {},
                          "key": ""
                        },
                        headers={"origin": "https://f12.xjai.cc"},
                        stream=True)
    return res.content.decode('utf-8', 'ignore').replace('image&KFw6loC9Qvy&', '', 1)
