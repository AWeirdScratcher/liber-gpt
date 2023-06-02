from __future__ import annotations

import re
import time
import uuid
import json
import random
import base64
import requests
import threading
import fake_useragent # pip install fake-useragent
from faker import Faker # pip install faker
from typing import Callable
from pydantic import BaseModel # pip install pydantic

no_warnings = False

def warn(msg):
  if not no_warnings:
    print(f"\033[93m\n{msg}\033[0m\n")

class Account:
  def __init__(self, auto_load: bool = True, save_token: bool = True, no_warnings: bool = False):
    self.save_token = save_token

    if auto_load:
      try:
        with open("tokens.txt", "r") as file:
          for line in file.readlines():
            if line and line != "\n":
              self.token = line.replace("\n", "")
              self.ua = fake_useragent.UserAgent().random
              self.line = "used"
              warn("Using pre-generated tokens.")
              return None # skip the following parts
      except:
        pass # noqa
      # no tokens found, jump outside of the `if` block.

    self.initialize()

  def initialize(self):
    email = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1").json()
    self.mail = email[0]
    self.domain = self.mail.split('@')[1]
    self.username = self.mail.split('@')[0]
    self.tries = 0
    self.register()
    self.line = "no-auto-load"

  def inbox(self):
    contents = requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={self.username}&domain={self.domain}").json()
    return contents

  def get_email_content(self, id: int):
    email = requests.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={self.username}&domain={self.domain}&id={id}").json()
    return email

  def wait_until_receive_email(self, callback: Callable):
    """
    This function uses threading.
    """
    def attempt():
      self.tries += 1 # noqa
      inbox = self.inbox()

      if self.tries == 6:
        raise Error("The receiving process is taking longer than expected. It's recommended to re-create an email account.\n(ACTION CANCELED)")
        return callback
      if not len(inbox) >= 1 and self.tries < 6:
        threading.Timer(5.0, attempt).start()
      else:
        self.generate_token(inbox)
        callback(inbox)

    attempt()

  def sync_wait_until_receive_email(self):
    """
    This function uses normal sync, which is not recommended for API projects such as FastAPI for flask, as it contains a `time.sleep` block.
    """
    while True:
      self.tries += 1
      inbox = self.inbox()

      if self.tries >= 6:
        raise Error("The receiving process is taking longer than expected. It's recommended to re-create an email account.\n(ACTION CANCELED)")
        return False

      if len(inbox) >= 1:
        self.generate_token(inbox)
        return inbox

      time.sleep(5.0)

  def register(self):
    fake = Faker('zh_CN') # Since it's a Chinese site, it's better to use the Chinese localization
    self.ua = ua = fake_useragent.UserAgent().random # always use the same user agent
    self.password = password = base64.b64encode("".join([str(uuid.uuid4()) for _ in range(2)]).encode('utf-8')).decode('utf-8')

    # register an account
    res = requests.post("https://ai.usesless.com/api/cms/auth/local/register", json={
      "username": fake.name() + str(random.randrange(1000, 9999)),
      "email": self.mail,
      "password": password
    }, headers={
      "User-Agent": ua,
    })
    if res.status_code != 200:
      raise Error(res.content)

  def generate_token(self, email):
    content = self.get_email_content(email[0]['id'])
    link = re.findall(r"http:\/\/ai\.usesless\.com\/api\/cms\/auth\/email-confirmation\?confirmation\=\w.+\w\w", content['textBody'])[0]
    requests.get(link, headers={
      "User-Agent": self.ua
    })
    result = requests.post("https://ai.usesless.com/api/cms/auth/local", json={
      "identifier": self.mail,
      "password": self.password
    }).json()
    self.token = token = result['jwt']

    if self.save_token:
      with open("tokens.txt", "a") as file:
        file.write(token + "\n")

def generate(account: Account, prompt, systemMessage, parentMessageId, presence_penalty, temperature, creation_function: Callable = None):
  """
  Generate response from the prompt.
  """
  generated = requests.post("https://ai.usesless.com/api/chat-process", headers={
    "User-Agent": account.ua,
    "Referer": "https://ai.usesless.com/chat",
    "Origin": "https://ai.usesless.com",
    "Authorization": f"Bearer {account.token}"
  }, json={
    "openaiKey": "",
    "prompt": prompt,
    "options": {
      "parentMessageId": parentMessageId,
      "systemMessage": systemMessage,
      "completionParams": {
        "model": "gpt-3.5-turbo",
        "presence_penalty": presence_penalty,
        "temperature": temperature
      }
    }
  }, stream=True)
  
  if generated.status_code != 200:
    raise Error(generated.content)

  for chunk in generated.iter_lines():
    response = json.loads(chunk.decode('utf-8'))

    class ResContext:
      parent = response['id'] # the website dev probably messed up with it
      content = response['detail']['choices'][0]['delta'].get('content', '')
      ip_chat_count = response.get('ipChatCount', 'UNKNOWN')
      used_integral = response.get('usedIntegral', 'UNKNOWN')
      finished = response.get('ipChatCount') is not None
      
      def __repr__(self):
        return f"<class Context parent='{self.parent}' content='{self.content}' ip_chat_count={self.ip_chat_count} used_integral={self.used_integral} finished={self.finished}>"

    if creation_function:
      creation_function(ResContext())
    else:
      yield ResContext()

class Completion:
  @staticmethod
  def create(
    prompt: str,
    account: Account = None,
    systemMessage: str = None,
    presence_penalty: float = 0,
    temperature: float = 1.0,
    parentMessageId: str = None
  ):
    if not account:
      account = Account()
      warn("Warning: Passing in the `account` parameter in your code for this whole session is recommended, so the server-side could stay stable.")

    def wrapper(creation_function):
      if account.line == "no-auto-load":
        @account.wait_until_receive_email
        def callback(_):
          for chunk in generate(account, prompt, systemMessage, parentMessageId, presence_penalty, temperature):
            creation_function(chunk)
      else:
        try:
          for chunk in generate(account, prompt, systemMessage, parentMessageId, presence_penalty, temperature):
            creation_function(chunk)
        except Exception as err:
          # due to the token is invalid, take away!
          with open("tokens.txt", "r+") as file:
            lines = file.readlines()
            lines.remove(account.token)
            file.seek(0)
            file.truncate()
            file.write("\n".join(lines))

          raise Error(err)

      return creation_function
    return wrapper

class DelayedCompletion:
  @staticmethod
  def create(
    prompt: str,
    account: Account = None,
    systemMessage: str = None,
    presence_penalty: float = 0,
    temperature: float = 1.0,
    parentMessageId: str = None
  ):
    if not account:
      account = Account()
      warn("Warning: Passing in the `account` parameter in your code for this whole session is recommended, so the server-side could stay stable.")

    if account.line == "no-auto-load":
      account.sync_wait_until_receive_email()

      for chunk in generate(account, prompt, systemMessage, parentMessageId, presence_penalty, temperature):
        yield chunk
    else:
      # with pre-generated tokens
      try:
        for chunk in generate(account, prompt, systemMessage, parentMessageId, presence_penalty, temperature):
          yield chunk
      except Exception as err:
        with open("tokens.txt", "r+") as file:
          lines = file.readlines()
          lines.remove(account.token)
          file.seek(0)
          file.truncate()
          file.write("\n".join(lines))

        raise Error(err)

class Error(Exception):
  """Uncaught Exception"""

class Context(BaseModel):
  parent: str
  content: str = ""
  ip_chat_count: int | str = 'UNKNOWN'
  used_integral: int | str = 'UNKNOWN'
  finished: bool = False
