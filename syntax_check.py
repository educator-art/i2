"""
syntax_check_method
疎通できるまで「推論」を繰り返す
推論で与えられたコードは疎通するとは限らない
コードを実行したとき構文エラーをチェックして、疎通するところまで推論を繰り返すことで
初期の「推論」と比べて価値が向上する（疎通する推論となる）
※ 疎通しない机上の推論よりは価値があるだろうという考え方

- Docker Desktop及び、コンテナ（python:3.12-slim）を使用する
- Pythonのコード作成と検証の自動化を対応する

created 2025.02.09
updated 2025.02.12
"""

from basic_module import basic_module
import os
import subprocess
import docker

class syntax_check(basic_module):
    
    def __init__(self, prompt, filepath, max_loop_num=0):
        super().__init__(prompt) # 明示的に引き継ぎ
        self.filepath=filepath
        self.max_loop_num=max_loop_num

    # 今後、共通する処理があれば、Basic_Moduleに追記する(import osも定義しているため)
    def file_read(self):
        with open(self.filepath, "r", encoding="utf-8") as file:
            return file.read()
        
    def file_write(self, text):
        output_filepath=os.path.splitext(self.filepath)[0]+"_output.py"
        with open(output_filepath, "w", encoding="utf-8") as file:
            file.write(text)
            return output_filepath

    # syntax_check_method
    def syntax_check_method(self):
        
        start, start_str = self.get_current_time()
        print(f"debug: 開始時刻 {start_str}")

        # Check Value
        return_value=None
        return_error_value=None
        code=None
        err_loop_num=0

        while(True):

            # プロンプトを作成する
            prompt = self.file_read()
            if return_value:
                prompt = f"{self.prompt}\n{prompt} \n## code: \n{code} \n##return value: \n{return_value}"   # 今後、return値を評価するためのメソッドのために残しておく
            elif return_error_value:
                prompt = f"{self.prompt}\n{prompt} \n## code: \n{code} \n## エラーを修正してください \n### error message: \n{return_error_value}"
            else:
                prompt = f"{self.prompt}\n{prompt}"
            
            # 推論をする
            print(f"プロンプト:\n{prompt}")
            code=self.model_inference(prompt)
            
            # Code Blockを削除する
            code=code.replace("```python","").replace("```","").strip()
            
            # コードを出力する
            output_filepath=self.file_write(code)

            # 推論結果のコードを安全にテストする
            client = docker.from_env()

            # Dockerに送信するための絶対パスを取得する
            send_abs_output_filepath = os.path.abspath(output_filepath)
            send_abs_output_filename=os.path.basename(send_abs_output_filepath)

            # コンテナを実行する
            container = client.containers.run(
                "python:3.12-slim",
                f"python /home/{send_abs_output_filename}", 
                volumes={send_abs_output_filepath: {"bind": f"/home/{send_abs_output_filename}", "mode": "ro"}},
                detach=True, 
                remove=True
            )

            # コンテナが終了するのを待つ
            exit_code=container.wait()
            log_message=container.logs().decode('utf-8')
            
            if exit_code["StatusCode"]==0:
                # return_value=log_message
                print("finished")
                break
            else:
                return_error_value=log_message
                print(f"error message: {return_error_value}")
                err_loop_num=err_loop_num+1

            if err_loop_num==self.max_loop_num:
                print("既定回数、エラーが発生したので終了します")
                self.file_write(f"# モデルの推論結果（コード）\n{code}\n# エラーメッセージ:\nr\"\"\"{return_error_value}\"\"\"")
                break

        # Debug: 終了時刻
        end, end_str = self.get_current_time()
        print(f"debug: 終了時刻 {end_str}")

        # Debug: 実行時間
        diff_str = self.time_measurement(start, end)
        print(f"debug: 実行時間 {diff_str} 秒")

instance = syntax_check("下記を読んで対応してください", "syntax_check_sample.md", max_loop_num=3)
instance.syntax_check_method()