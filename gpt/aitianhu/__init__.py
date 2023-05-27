from __future__ import annotations

import requests
import json

class Completion:
  @staticmethod
  def create(
    prompt: str,
    conversationId: str = "",
    parentMessageId: str = ""
  ) -> CompletionResponse:
    res = requests.post("https://www.aitianhu.com/api/chat-process", json={
      "prompt": prompt,
      "options": { "conversationId": conversationId, "parentMessageId": parentMessageId }
    }, stream=True)
    return CompletionResponse(res)

class CompletionResponse:
  def __init__(self, req: requests.Request):
    self.req = req
    self.fetched = {
      "content": "",
      "data": {}
    }

  def __iter__(self):
    for chunk in self.req.iter_lines():
      payload = json.loads(chunk.decode('utf-8'))

      if not payload.get('text'):
        # we need to use method #2
        delta = payload['detail']['choices'][0]['delta'].get('content', '')
        self.fetched['content'] += delta
        self.fetched['data'] = payload

        yield delta
      else:
        yield payload['text'][len(self.fetched['content']):] # yield first
  
        self.fetched['content'] = payload['text']
        self.fetched['data'] = payload


  @property
  def content(self):
    payload = self.fetched or json.loads(self.req.content.decode('utf-8').rsplit('\n')[-1])
    return payload['content']

  @property
  def data(self):
    payload = self.fetched['data'] or json.loads(self.req.content.decode('utf-8').rsplit('\n')[-1])

    return payload

class Error(Exception):
  pass