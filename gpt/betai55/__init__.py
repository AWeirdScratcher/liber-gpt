from __future__ import annotations

import requests
from fake_useragent import UserAgent

ua = UserAgent()
url = "https://b1.betai55.uk/api/chat-stream"

class Completion:
  @staticmethod
  def create(
    messages: list[dict],
    temperature: float = 1.0,
    persence_penalty: float = 0.0
  ) -> CompletionResponse:
    res = requests.post(url, json={
      "messages": messages,
      "model": "gpt-3.5-turbo",
      "stream": True,
      "presence_penalty": 0,
      "temperature": 1
    }, headers={
      "User-Agent": ua.random,
      "origin": "https://b1.betai55.uk",
      "access-code": "586-484-535D",
      "path": "v1/chat/completions"
    }, stream=True)

    return CompletionResponse(res)

class CompletionResponse:
  def __init__(self, req: requests.Request):
    self.req = req
    self.fetched = ""

  def __iter__(self):
    for chunk in self.req.iter_content():
      payload = chunk.decode('utf-8')
      self.fetched += payload

      yield payload

  @property
  def content(self):
    return self.fetched or self.req.content.decode('utf-8')

class Error(Exception):
  pass