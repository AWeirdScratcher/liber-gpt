from __future__ import annotations

import requests
import json
from fake_useragent import UserAgent

ua = UserAgent()

class Completion:
  @staticmethod
  def create(
    messages: list[dict],
  ) -> CompletionResponse:
    res = requests.post("https://www.chatbase.co/api/fe/chat", headers={
      "referer": "https://www.chatbase.co/chatbot-iframe/0nmlH49YOz2t8e7urE9QA",
      "User-Agent": ua.chrome
    }, json={
      "captchaCode": "hadsa",
      "chatId": "0nmlH49YOz2t8e7urE9QA",
      "messages": messages
    }, stream=True)

    if res.status_code != 200:
      raise Error("Uncaught, \n" + res.content.decode('utf-8'))

    return CompletionResponse(res)

class CompletionResponse:
  def __init__(self, request: requests.Request):
    self.req = request
    self.fetched = ""

  def __iter__(self):
    for chunk in self.req.iter_content():
      content = chunk.decode('utf-8')
  
      self.fetched += content
      yield content

  @property
  def content(self):
    return self.fetched or self.req.content

class Role:
  """Shortcut for the `messages` object."""
  user = lambda t: { "role": "user", "content": t }
  assistant = lambda t: { "role": "assistant", "content": t }

class Error(Exception):
  pass