"""
improve inference
created 2025.02.05

# アプローチ

## 手順
step1: プロンプト
step2: 推論の結果を取得する(初期の推論)
step3: 検索用のキーワードを取得する
step4: キーワードを元に検索結果のTOPのLINK(URL)を取得する
step5: LINK(URL)のbodyタグを取得する
step6: step2とstep6を参照してstep2の推論の情報は古くなっていないか推論して結果を取得する(improve inference)

## 期待
- ユーザーはステップ毎にプロンプトを入力する回数を減らせる（自動化）
- モデルは推論結果の情報が古ければ訂正することで、ユーザーにとっての推論結果が向上する（古い推論内容を実行してエラーを受ける体験を未然に防ぐ）

## 着想
- モデルは現在の情報と比較して分からないと答えられる
    - ユーザーは解決しない方向性でモデルとのやりとりを減らすことが出来るのではないか
        - モデルは無駄なGPUの消費、ユーザーは無駄な時間の浪費を避けられる

- モデルもRAGも学習した世界の範囲で推論する
    - 一方でインターネットは日々更新されるので、情報に差異が発生する
        - RAGよりも検索した方がアップデートに対応できる（ユーザーフレンドリーではないか）

## 特徴
- 特定のモデルに依存せずに実施できること

"""

import requests
from bs4 import BeautifulSoup
import os
import sys
import google.generativeai as genai
import datetime

class improve_inference:

    def __init__(self, prompt):
        self.prompt = prompt
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

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content(prompt)
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

    # 時間の確認
    def get_current_time(self):
        current = datetime.datetime.now()
        return current, current.strftime("%Y-%m-%d %H:%M:%S")

    # 時間の計測
    def time_measurement(self, start_time, end_time):
        return (end_time-start_time).seconds

    # 検証性Check
    def verification_method(self):

        # Debug: 開始時刻
        start, start_str = self.get_current_time()
        print(f"debug: 開始時刻 {start_str}")

        print("process: ①")
        self.initial_answer = self.model_inference(self.prompt)
        # print(f"process: ① \n {self.initial_answer}")        
        print(f"intial_answers： \n {self.initial_answer}")

        print("process: ②")
        self.keyword = self.model_inference(f"#あなたが以前にした回答が古い情報ではないか検索して確かめるので、オフィシャルサイトを検索できるキーワードを20文字以内にまとめてください\n##以前の内容：{self.initial_answer }")
        #print(f"process: ② \n {self.keyword}")
        
        print("process: ③")
        self.link = self.google_search(self.keyword)
        #print(f"process: ③ \n {self.link}")
        
        print("process: ④")
        self.verification = self.extractbody(self.link)
        #print(f"process: ④ \n {self.verification}")
        
        print("process: ⑤")
        self.improved_answer = self.model_inference(f"\n # <1> あなたの以前の回答と実際の検索結果を比較してください\n # <2> 次に、あなたが以前に回答した関数やプロパティは実際の検索結果（オフィシャルサイト）に書かれていますか？\n ## もし、あなたが以前に回答した関数やプロパティが書かれていない場合は、提示した機能は廃止されていて使用できないことを疑う必要があります。\n # <3> 最後に、あなたが以前に行った回答は古い情報でしたか？ # あなたの以前の回答\n{self.initial_answer}\n##実際の検索結果\n{self.verification}")
        print(f"improved answer \n {self.improved_answer} \nReference URL is {self.link}")

        # Debug: 終了時刻
        end, end_str = self.get_current_time()
        print(f"debug: 終了時刻 {end_str}")

        # Debug: 実行時間
        diff_str = self.time_measurement(start, end)
        print(f"debug: 実行時間 {diff_str} 秒")

# 検索の実行
search = improve_inference("flutterで共有テキストを受け取るには？何かライブラリ、そして関数はあるか？まずは、それだけ教えて")
search.verification_method()

# 後書き
# 過去に手動でやりとりしたが、結果的に別なアプローチを取った
# プロンプトの内容（視点）を変える（発想する）ことで、今までの方向性にはない別の回答（推論結果）を得られた
## 似たようなプロンプトでは似たような推論結果にしかならない
## 実はモデルは解を知っている（備えている）のかもしれないが、似た方向性のプロンプトではモデルはユーザーに提示することまで行きつかない
# print(search.model_inference("flutter pluginは何で出来ているか？"))
# print(search.model_inference("Kotlinで共有テキストを受け取るには？"))