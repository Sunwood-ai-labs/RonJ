import requests
import os
import time

import sys
import pprint
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.tts_module import TextToSpeech

# TextToSpeechインスタンスを作成
tts = TextToSpeech(api_url="http://style-bert-vits2-api:5000/voice")

# テキストを指定して音声を生成
text = "こんにちは、今日の気分はどうですか？"
text = "なるほど、Transformerを画像に使うんですね！位置情報って具体的にはどういうことですか？"
tts.generate_audio(text, model_id=4)