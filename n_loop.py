"""
n_loop
n回ループさせて、共通項や妥当性を得る
通常は（ブレはあるが）一定の回答に収束したので、seedを使って実験的に可変にする
created 2025.02.06
updated 2025.02.07
"""
from basic_module import basic_module

class n_loop(basic_module):

    def __init__(self, prompt, number, random_seed=False):
        super().__init__(prompt, random_seed=random_seed) # 明示的に引き継ぎ
        self.number=number

    # n_loop method
    def n_loop_method(self):
        
        start, start_str = self.get_current_time()
        print(f"debug: 開始時刻 {start_str}")

        tmp_inference_list = []
        prompt="# 依頼\n あなたが過去に回答した内容を用意した。共通項を探して妥当性のある解を明示してください。\n## 過去の回答"

        for i in range(self.number):
            tmp_inference_list.append(self.model_inference(self.prompt))

        for i in range(len(tmp_inference_list)):
            prompt = prompt + f"\n### {i+1}回目の回答 \n {tmp_inference_list[i]}"

        print(f"debug: {prompt}")

        self.improved_answer=self.model_inference(prompt)

        print(self.improved_answer)

        # Debug: 終了時刻
        end, end_str = self.get_current_time()
        print(f"debug: 終了時刻 {end_str}")

        # Debug: 実行時間
        diff_str = self.time_measurement(start, end)
        print(f"debug: 実行時間 {diff_str} 秒")

instance = n_loop("ギターを上達するには何から始めればいいか？優先する練習を3つあげて理由を述べよ（簡潔に）", 3, True)
instance.n_loop_method()