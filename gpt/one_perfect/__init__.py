from __future__ import annotations

import warnings
import requests
import datetime
import json

from fake_useragent import UserAgent


base_url = "https://fasd131fssdf97986agagyk656.lovebaby.today/api/openai/v1/chat/completions"
ua = UserAgent()

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # disable the unverified warning, use our custom ones
# credit to https://stackoverflow.com/questions/27981545/
def format(msg, *args, **kwargs):
    # ignore everything except the message
    return str(msg) + '\n'

warnings.formatwarning = format


class Completion:

  @staticmethod
  def create(prompt: str = None,
             messages: list = [],
             temperature: float = 0.5,
             disable_warnings: bool = False) -> CompletionResponse:
    msgs = [{
      "role":
      "system",
      "content":
      f"You're ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible, and use Markdown for your response.\nKnowledge cut-off: 2021 Sep.\nCurrent Date: {datetime.datetime.now().strftime('%Y-%m-%d')}"
    }, {
      "role": "user",
      "content": prompt
    }]

    if (not prompt) and (not messages):
      raise ValueError("Either `prompt` or `messages` must be set.")
    elif prompt and messages:
      msgs = [*messages, {"role": "user", "content": prompt}]
    elif (not prompt) and messages:
      msgs = messages

    if not disable_warnings:
      warnings.warn("`one_perfect` uses an untrusted SSL certificate. Use at your own risk.\nUsing `gravity_engine` instead is highly recommended.\n\n")

    res = requests.post(base_url,
                        json={
                          "messages": msgs,
                          "model": "gpt-3.5-turbo",
                          "presence_penalty": 0,
                          "stream": True,
                          "temperature": temperature
                        },
                        stream=True, headers={
                          "User-Agent": ua.random
                        }, verify=False)

    if res.status_code != 200:
      raise Error(res.content)

    return CompletionResponse(res)


class CompletionResponse:
  req: requests.Request

  def __init__(self, req: requests.Request):
    self.req = req
    self.fetched = {}

  def __iter__(self):
    for chunk in self.req.iter_lines():
      plain = chunk.decode('utf-8')

      if plain.startswith('data: '):
        content = plain[6:]  # replace 'data: ' with ''

        if content != "[DONE]":
          payload = json.loads(content)
          if payload['choices'][0]['finish_reason'] == 'stop':
            self.fetched = payload

          yield payload['choices'][0]['delta'].get('content', '')

  @property
  def content(self):
    if not self.fetched:
      raise Error("Cannot get data, please iterate the response first.")

    return self.fetched['choices'][0]['delta'].get('content', '')

  @property
  def data(self):
    if not self.fetched:
      raise Error("Cannot get data, please iterate the response first.")

    return self.fetched


class Error(Exception):
  """
  Uncaught Error.
  """
  pass


class Role:
  """
  A shortcut for the `messages` object.
  """

  @staticmethod
  def system(content: str):
    return {"role": "system", "content": content}

  @staticmethod
  def user(content: str):
    return {"role": "user", "content": content}

  @staticmethod
  def assistant(content: str):
    return {"role": "assistant", "content": content}
