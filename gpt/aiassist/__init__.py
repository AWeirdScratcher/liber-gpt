from __future__ import annotations

import json
import requests

system = "You're ChatGPT, a large language model trained by OpenAI."


class Completion:

  @staticmethod
  def create(
    prompt: str,
    systemMessage: str = system,
    parentMessageId: str = "",
    temperature: float = 0.8,
    top_p: float = 1.0,
  ) -> CompletionResponse:
    payload = {
      "prompt": prompt,
      "options": {
        "parentMessageId": parentMessageId
      },
      "systemMessage": systemMessage,
      "temperature": temperature,
      "top_p": top_p,
    }

    url = "http://43.153.7.56:8080/api/chat-process"
    request = requests.post(url, json=payload, stream=True)
    return CompletionResponse(request)


class CompletionResponse:

  def __init__(self, request: requests.Request):
    self.req = request
    self.fetched = {}

  def __iter__(self):
    for chunk in self.req.iter_lines():
      response = json.loads(chunk.decode('utf-8'))
      if response['detail']['choices'][0]['finish_reason'] == "stop":
        self.fetched = response

      yield response.get('delta', '')

  @property
  def content(self):
    """
    The text content.
    """
    contents = (self.fetched or json.loads(
      self.req.content.decode('utf-8').rsplit('\n')[-1]))['text']

    return contents

  @property
  def data(self):
    """
    Get the additional information such as message ID, delta, etc. Usually takes the last part (`STOP`) of the data.
    """
    return self.fetched or json.loads(
      self.req.content.decode('utf-8').rsplit('\n')[-1])
