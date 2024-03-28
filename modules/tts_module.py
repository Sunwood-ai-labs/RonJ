import requests
import os
import time

class TextToSpeech:
    def __init__(self, api_url="http://style-bert-vits2-api:5000/voice"):
        self.api_url = api_url

    def generate_audio(self, text, model_id=0, speaker_id=0, output_folder="output", output_filename="output.wav"):
        # クエリパラメータ
        params = {
            "text": text,
            "encoding": "utf-8",
            "model_id": model_id,
            "speaker_id": speaker_id,
            "sdp_ratio": 0.2,
            "noise": 0.6,
            "noisew": 0.8,
            "length": 1,
            "language": "JP",
            "auto_split": True,
            "split_interval": 0.5,
            "assist_text": "",
            "assist_text_weight": 1,
            "style": "Neutral",
            "style_weight": 5
        }

        # フォルダが存在しない場合は作成
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # 音声ファイルの保存パス
        output_path = os.path.join(output_folder, output_filename)

        # リクエスト開始時間を記録
        start_time = time.time()

        # リクエストの送信とレスポンスの確認
        response = requests.get(self.api_url, params=params)

        # リクエスト終了時間を記録
        end_time = time.time()

        # リクエストにかかった時間を計算
        request_time = end_time - start_time

        if response.status_code == 200:
            # レスポンスから音声データを取得し、ファイルに保存
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"音声ファイルを '{output_path}' に保存しました。")
            print(f"リクエストにかかった時間: {request_time:.2f}秒")
        else:
            print("エラーが発生しました。ステータスコード:", response.status_code)