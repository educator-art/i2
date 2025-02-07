"""
basic_module
created 2025.02.07
"""

import requests
from bs4 import BeautifulSoup
import os
import sys
# import google.generativeai as genai
from google import genai
from google.genai import types
import datetime
import random

INT_MAX_VALUE = 2147483647

class basic_module:

    def __init__(self, prompt, random_seed=False):
        self.prompt = prompt
        self.random_seed = random_seed
        self.initial_answer = None
        self.keyword = None
        self.url = None
        self.verification = None
        self.improved_answer = None

    def model_inference(self, prompt):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            # APIキーが未設定
            sys.exit()

        # SDKの更新により記述方法が更新された。APIドキュメントの修正を確認してから落ち着いたタイミングで更新をはかる
        # https://ai.google.dev/gemini-api/docs/quickstart?hl=ja&lang=python
        # https://github.com/google-gemini/generative-ai-python?tab=readme-ov-file#authenticate
        # genai.configure(api_key=api_key)
        client = genai.Client(api_key=api_key)

        if self.random_seed == True:
            # オプション引数
            # https://github.com/google-gemini/generative-ai-python?tab=readme-ov-file#optional-arguments
            # https://ai.google.dev/api/generate-content?hl=ja#generationconfig
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt,
                config=types.GenerateContentConfig(
                    seed=random.randint(0,INT_MAX_VALUE),
                ),
            )

        else:
            # model = genai.GenerativeModel("gemini-2.0-flash-exp")
            # response = model.generate_content(prompt)
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp", contents=prompt
            )

        return response.text

    # Mock implementation
    # Probably, needs to Custom Search JSON API
    # https://developers.google.com/custom-search/v1/introduction?hl=ja
    def google_search(self, keyword):
        link = "https://pub.dev/packages/receive_sharing_intent"
        return link

    def extractbody(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        body_tag = soup.find("body")
        body_tag.text
        return body_tag.text

    # 時刻の確認
    def get_current_time(self):
        current = datetime.datetime.now()
        return current, current.strftime("%Y-%m-%d %H:%M:%S")

    # 時間の計測
    def time_measurement(self, start_time, end_time):
        return (end_time - start_time).seconds

# experimental enable to use random seed
# bm = basic_module("Hello World", random_seed=True)
# print(bm.model_inference(bm.prompt))
