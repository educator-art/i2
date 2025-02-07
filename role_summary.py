"""
role_summary
ロールプレイで視点を変えて整理する
created 2025.02.06
updated 2025.02.07
"""

from basic_module import basic_module

class role_summary(basic_module):

    def __init__(self, prompt, role):
        super().__init__(prompt)
        self.role=role

    def role_play_summary_method(self):
        
        start, start_str = self.get_current_time()
        print(f"debug: 開始時刻 {start_str}")

        # 要約のプロンプト（前文）
        prompt=f"# 依頼\n 「{self.prompt}」話をまとめるとどうか？\n## 過去の回答"

        # 意見の収集
        tmp_inference_list = []
        for i in range(len(self.role)):
            tmp_inference_list.append(self.model_inference(f"{self.role[i]}になりきって入会検討者として感想を、{self.prompt}"))
            prompt = prompt + f"\n### {i+1}人目の回答 \n {tmp_inference_list[i]}"

        print(f"debug: {prompt}")

        # 要約
        self.improved_answer=self.model_inference(prompt)

        print(self.improved_answer)

        # Debug: 終了時刻
        end, end_str = self.get_current_time()
        print(f"debug: 終了時刻 {end_str}")

        # Debug: 実行時間
        diff_str = self.time_measurement(start, end)
        print(f"debug: 実行時間 {diff_str} 秒")

isinstance = role_summary("月額1000円のオンライン英会話に入りたいと思うか？", ["経営者","専門職","一般職"])
isinstance.role_play_summary_method()