# Project: RonJ

```plaintext
OS: nt
Directory: C:\Prj\RonJ

├─ app.py
├─ demo/
│  ├─ demo_split.py
│  ├─ demo_style_bert_api.py
├─ docker/
│  ├─ Dockerfile
│  ├─ README.md
├─ docker-compose.yml
├─ docs/
│  ├─ icon.png
│  ├─ icon_mini.png
│  ├─ README.app.md
│  ├─ RonJ-Mini-30s.gif
├─ modules/
│  ├─ Ronj2Json.py
│  ├─ tts_module.py
├─ README.md
├─ Template/
│  ├─ TemplateFormat.json
```

## .

`app.py`

```plaintext
import streamlit as st
import json
import time
import streamlit.components.v1 as components
import random
from modules.tts_module import TextToSpeech
import base64
import os
from pydub import AudioSegment
import re

st.set_page_config(
    page_title="RonJ",
    page_icon="📚",
    # layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Sunwood-ai-labs/RonJ.git',
        'About': "RonJ～論文を面白おかしく理解するツール～"
    }
)

with st.sidebar:
    st.markdown("""
<p align="center">
    <h1 align="center">Ron J</h1>
    <img src="https://raw.githubusercontent.com/Sunwood-ai-labs/RonJ/main/docs/icon_mini.png" width="100%">
    <br>
</p>

    """, unsafe_allow_html=True)


# サイドバーでパラメータを設定
json_file_path = st.sidebar.text_input("JSONファイルのパス", "data/ViTAR_KANA.json")
emoji_file_path = st.sidebar.text_input("絵文字のテキストファイルのパス", "assets/emojis.txt")
api_url = st.sidebar.text_input("音声生成のAPIエンドポイント", "http://style-bert-vits2-api:5000/voice")

# TextToSpeechインスタンスを作成
tts = TextToSpeech(api_url=api_url)

def load_chat_data(json_file_path):
    """チャットデータをJSONファイルから読み込む"""
    try:
        with open(json_file_path, "r") as f:
            chat_data = json.load(f)
        return chat_data
    except FileNotFoundError:
        st.error(f"JSONファイルが見つかりません: {json_file_path}")
        return []

def load_emojis(emoji_file_path):
    """絵文字のリストをテキストファイルから読み込む"""
    try:
        with open(emoji_file_path, "r", encoding="utf-8") as f:
            emojis = [line.strip() for line in f]
        return emojis
    except FileNotFoundError:
        st.warning(f"絵文字のテキストファイルが見つかりません: {emoji_file_path}")
        return []

def generate_name_emoji_map(chat_data, emojis):
    """名前と絵文字のマッピングを生成する"""
    unique_names = list(set([message["name"] for message in chat_data]))
    name_emoji_map = {name: random.choice(emojis) for name in unique_names}
    return name_emoji_map

def generate_name_voice_map(chat_data):
    """名前と音声IDのマッピングを生成する"""
    unique_names = list(set([message["name"] for message in chat_data]))
    name_voice_map = {name: random.randrange(0, 7, 1) for name in unique_names}
    return name_voice_map

def display_chat(chat_data, name_emoji_map, name_voice_map):
    """チャットを表示する"""
    chat_container = st.container()
    
    # JavaScriptコードを1回だけ実行
    components.html(
        """
        <script>
            window.onload = function() {
                setInterval(function() {
                    window.parent.document.querySelector('section.main').scrollTo(0, window.parent.document.querySelector('section.main').scrollHeight);
                }, 100);
            };
        </script>
        """,
        height=0
    )
    
    # チャットの表示
    for message in chat_data:
        name = message["name"]
        text = message["text"]
        number = message["number"]
        header = message["header"]
        
        # 名前に応じた絵文字を取得
        emoji = name_emoji_map.get(name, "👤")
        
        # チャットコンテナにメッセージを追加
        with chat_container:
            # メッセージの表示
            with st.chat_message("user", avatar=emoji):
                st.markdown(f"**{header}**")
    
                # 返信先の処理
                if message["replies"]:
                    reply_to = message["replies"][0][2:]
                    st.write(f"＞＞ {reply_to}")
                    
                # テキストを "。"、"！"、"!" で分割
                sentences = re.split(r'[。！!]', text)
                for sentence in sentences:
                    if sentence:
                        st.write(sentence)
                        play_audio(sentence, name_voice_map.get(name, 1))
        
        time.sleep(2)

def play_audio(text, voice_id):
    """音声を再生する"""
    # 音声ファイルを生成
    output_filename = f"{text}.wav"
    audio_path = f"output/{output_filename}"
    try:
        voice_data = tts.generate_audio(text, output_filename=output_filename, model_id=voice_id)
    except Exception as e:
        st.error(f"音声生成エラー: {str(e)}")
        return
    
    # 音声ファイルを読み込む
    with open(audio_path, "rb") as audio_file:
        voice_data = audio_file.read()
    
    if voice_data:
        audio_str = "data:audio/wav;base64,%s" % (base64.b64encode(voice_data).decode())
        audio_html = f"""
            <audio autoplay=True>
                <source src="{audio_str}" type="audio/wav" autoplay=True>
                Your browser does not support the audio element.
            </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    
    # 音声ファイルの読み込み
    sound = AudioSegment.from_file(audio_path, "wav")
    audio_duration = sound.duration_seconds
    
    time.sleep(audio_duration)
    
    # 生成された音声ファイルを削除
    os.remove(audio_path)

def main():
    # st.title("解説求む!新しいVision Transformerアーキテクチャ「ViTAR」")
    st.title("解説求む!新しいVision Transformerアーキテクチャ「ViTAR」")

    
    if st.button("再生"):
        chat_data = load_chat_data(json_file_path)
        emojis = load_emojis(emoji_file_path)
        name_emoji_map = generate_name_emoji_map(chat_data, emojis)
        name_voice_map = generate_name_voice_map(chat_data)
        
        display_chat(chat_data, name_emoji_map, name_voice_map)

if __name__ == "__main__":
    main()
```

`docker-compose.yml`

```plaintext
version: '3.8'

services:

  style-bert-vits2-api:
    build: 
      context: .
      dockerfile: Style-Bert-VITS2/Dockerfile.external

    volumes:
      - ./Style-Bert-VITS2:/app
      - ./Style-Bert-VITS2/model_assets:/model_assets
      - ./Style-Bert-VITS2/Data:/Data

    ports:
      - "8000:8000"
      - "5000:5000"
    tty: true
    working_dir: /app
    command: >
      sh -c "python initialize.py && 
             python server_fastapi.py"

  ron-j:
    build:
      context: ./docker
      dockerfile: Dockerfile
    volumes:
      - ./:/app
      - ./.cache:/root/.cache
      - ./.streamlit:/root/.streamlit
    environment:
      - PULSE_SERVER=/mnt/wslg/PulseServer
      - DISPLAY=$DISPLAY
      # - PULSE_SERVER=$PULSE_SERVER
      - WAYLAND_DISPLAY=$WAYLAND_DISPLAY
      - XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR
    ports:
      - 8502:8502
      - 8503:8503
    env_file:
      - .env
    working_dir: /app
    tty: true
    command: streamlit run app.py --server.port 8502
    # network_mode: "host"
```

`README.md`

```plaintext
<p align="center">
  <img alt="OpenDevin Logo" src="./docs/icon.png" width="400" />
</p>


# ろんJ - 論文を面白おかしく理解するツール


[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-available-blue)](https://www.docker.com/)
[![](https://img.shields.io/static/v1?label=Blog&message=Sunwood-AI-labs.&color=green)](https://hamaruki.com/)

論文は難しそうで読むのが億劫だと感じたことはありませんか？でもそんな人でも、「ろんJ」を使えば論文の内容が面白おかしく理解できるかもしれません。

「ろんJ」は、アップロードした論文の内容を、あの有名な２ちゃんねるの「なんでも実況J」（通称：なんJ）のスレッド風に解説・実況してくれる画期的なサービスです。難解な論文の内容を、親しみやすいなんJのノリで楽しく理解することができます。

![](https://github.com/Sunwood-ai-labs/RonJ/blob/main/docs/RonJ-Mini-30s.gif)

## 特徴

- 論文の内容をなんJスレッド風に自動解説
- 音声合成(Style-Bert-VITS2)による臨場感あふれる実況
- シンプルで直感的なユーザーインターフェース
- Dockerを使用した簡単なセットアップ

## セットアップ

1. このリポジトリをクローンします。

   ```bash
   git clone https://github.com/Sunwood-ai-labs/RonJ.git
   cd ronj
   ```

2. Dockerコンテナを起動します。

   ```bash
   docker-compose up -d
   ```

   Dockerコンテナについての詳細はこちらを参照してください。([docker/README.md](docker/README.md))

3. セットアップが完了したら、ブラウザで `http://localhost:8502/` にアクセスしてください。

    ろんJのStreamlitアプリケーションについてはこちらを参照してください。([docs/README.app.md](docs/README.app.md))

## 使い方

1. なんJ風に解説したスレッドの情報をJSONファイルで準備します。JSONファイルのフォーマットは以下の通りです。

   ```json
   [
     {
       "name": "風吹けば名無し",
       "text": "論文の内容を面白おかしく解説するで！",
       "number": "1",
       "header": "1番セカンド",
       "replies": []
     },
     {
       "name": "風吹けば名無し",
       "text": "著者らは新しい手法を提案しとるな。画期的やと思うで！",
       "number": "2",
       "header": "2番セカンド",
       "replies": [">>1"]
     }
   ]
   ```

2. ろんJのwebページ(`http://localhost:8502/`)にアクセスします。

3. Streamlitのサイドバーで、以下の情報を入力します。
   - JSONファイルのパス
   - 絵文字のテキストファイルのパス（デフォルト: `assets/emojis.txt`）
   - 音声生成のAPIエンドポイント（デフォルト: `http://style-bert-vits2-api:5000/voice`）

4. 「再生」ボタンをクリックすると、style-bert-vits2によるなんJスレッド風の実況が始まります。

5. 実況を楽しみながら、論文の内容を理解していきましょう！

## デモ

style-bert-vits2 APIのデモを実行するには、以下のコマンドを実行してください。

```bash
docker-compose exec ron-j python demo/demo_style_bert_api.py
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細については、[LICENSE](LICENSE)ファイルを参照してください。

## 貢献

プルリクエストや改善案は大歓迎です！バグ報告や機能リクエストがある場合は、Issueを作成してください。


---

ろんJで、論文の理解が楽しくなること間違いなし！さっそく使ってみましょう！
```

## demo

`demo\demo_split.py`

```plaintext
import requests
import os
import time

import sys
import pprint
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.Ronj2Json import Ronj2Json


if __name__ == '__main__':
    parser = Ronj2Json('data/ViTAR.md')
    # parser.process_markdown('data/ViTAR.json')
    parser.process_markdown()
```

`demo\demo_style_bert_api.py`

```plaintext
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
tts.generate_audio(text, model_id=5)
```

## docker

`docker\Dockerfile`

```plaintext
FROM python:3.11

WORKDIR /app

RUN apt -y update && apt -y upgrade
RUN apt -y install libopencv-dev

RUN pip install --upgrade pip  \
                streamlit \
                audio-recorder-streamlit \
                fastapi uvicorn python-multipart \
                google-generativeai 
RUN pip install opencv-python streamlit-webrtc
RUN pip install audio-recorder-streamlit pydub
```

`docker\README.md`

```plaintext
# Dockerを使用したろんJの実行方法

このフォルダには、ろんJをDockerで実行するための `docker-compose.yml` ファイルと `Dockerfile` が含まれています。

## 前提条件

- Dockerがインストールされていること
- docker-composeがインストールされていること

## 使用方法

1. このフォルダ内で、以下のコマンドを実行してDockerコンテナを起動します。

   ```bash
   docker-compose up -d
   ```

   このコマンドにより、以下のサービスが起動します。
   - `style-bert-vits2-api`: Style-Bert-VITS2モデルのAPIサーバー
   - `ron-j`: ろんJのStreamlitアプリケーション

2. コンテナが正常に起動したら、以下のURLにアクセスしてろんJを使用できます。

   - ろんJ: `http://localhost:8502/`
   - Style-Bert-VITS2 API: `http://localhost:5000/`

3. ろんJの使用が終了したら、以下のコマンドでDockerコンテナを停止します。

   ```bash
   docker-compose down
   ```

## 設定

- `docker-compose.yml` ファイルには、各サービスの設定が記載されています。
  - `style-bert-vits2-api` サービスは、Style-Bert-VITS2モデルのAPIサーバーを起動します。
  - `ron-j` サービスは、ろんJのStreamlitアプリケーションを起動します。

- `Dockerfile` には、ろんJのStreamlitアプリケーションを実行するためのDockerイメージの構成が記載されています。
  - 必要なPythonパッケージのインストールなどが行われます。

## ボリュームのマウント

- `docker-compose.yml` ファイルでは、ホストマシンのディレクトリをコンテナ内にマウントしています。
  - `./Style-Bert-VITS2` ディレクトリは、Style-Bert-VITS2モデルの関連ファイルを格納するために使用されます。
  - `./` ディレクトリは、ろんJのアプリケーションファイルを格納するために使用されます。
  - `./.cache` ディレクトリは、キャッシュファイルを格納するために使用されます。
  - `./.streamlit` ディレクトリは、Streamlitの設定ファイルを格納するために使用されます。

## 注意事項

- `.env` ファイルには、必要な環境変数を設定してください。
- コンテナを起動する前に、必要なディレクトリとファイルが存在することを確認してください。

以上が、ろんJをDockerで実行するための手順です。不明な点がある場合は、お気軽にお問い合わせください。
```

## docs

`docs\icon.png` - Error reading file: 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte

`docs\icon_mini.png` - Error reading file: 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte

`docs\README.app.md`

```plaintext
# ろんJ - Streamlitアプリケーション

このPythonスクリプト(`app.py`)は、ろんJのメインアプリケーションを構成するStreamlitアプリケーションです。論文の内容をなんJスレッド風に解説・実況するための機能を提供します。

## 1. インポートと設定

まず、必要なライブラリをインポートし、Streamlitアプリケーションの基本設定を行います。

```python
import streamlit as st
import json
import time
import streamlit.components.v1 as components
import random
from modules.tts_module import TextToSpeech
import base64
import os
from pydub import AudioSegment
import re

st.set_page_config(
    page_title="RonJ",
    page_icon="📚",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Sunwood-ai-labs/RonJ.git',
        'About': "RonJ～論文を面白おかしく理解するツール～"
    }
)
```

ここでは、Streamlitの基本設定として、ページタイトル、アイコン、サイドバーの初期状態、ヘルプリンクとアプリケーションの説明を設定しています。

## 2. サイドバーの設定

次に、Streamlitのサイドバーを使用して、アプリケーションのパラメータを設定します。

```python
with st.sidebar:
    st.markdown("""
<p align="center">
    <h1 align="center">Ron J</h1>
    <img src="https://raw.githubusercontent.com/Sunwood-ai-labs/RonJ/main/docs/icon_mini.png" width="100%">
    <br>
</p>

    """, unsafe_allow_html=True)

json_file_path = st.sidebar.text_input("JSONファイルのパス", "data/ViTAR_KANA.json")
emoji_file_path = st.sidebar.text_input("絵文字のテキストファイルのパス", "assets/emojis.txt")
api_url = st.sidebar.text_input("音声生成のAPIエンドポイント", "http://style-bert-vits2-api:5000/voice")
```

サイドバーには、アプリケーションのロゴと説明を表示し、JSONファイルのパス、絵文字のテキストファイルのパス、音声生成のAPIエンドポイントを入力するためのテキストボックスを配置しています。

## 3. 音声合成の設定

TextToSpeechクラスを使用して、音声合成のインスタンスを作成します。

```python
tts = TextToSpeech(api_url=api_url)
```

## 4. データの読み込み

### 4.1. チャットデータの読み込み

`load_chat_data`関数を使用して、指定されたJSONファイルからチャットデータを読み込みます。

```python
def load_chat_data(json_file_path):
    """チャットデータをJSONファイルから読み込む"""
    try:
        with open(json_file_path, "r") as f:
            chat_data = json.load(f)
        return chat_data
    except FileNotFoundError:
        st.error(f"JSONファイルが見つかりません: {json_file_path}")
        return []
```

### 4.2. 絵文字データの読み込み

`load_emojis`関数を使用して、指定されたテキストファイルから絵文字のリストを読み込みます。

```python
def load_emojis(emoji_file_path):
    """絵文字のリストをテキストファイルから読み込む"""
    try:
        with open(emoji_file_path, "r", encoding="utf-8") as f:
            emojis = [line.strip() for line in f]
        return emojis
    except FileNotFoundError:
        st.warning(f"絵文字のテキストファイルが見つかりません: {emoji_file_path}")
        return []
```

## 5. マッピングの生成

### 5.1. 名前と絵文字のマッピング

`generate_name_emoji_map`関数を使用して、登場人物の名前と絵文字のマッピングを生成します。

```python
def generate_name_emoji_map(chat_data, emojis):
    """名前と絵文字のマッピングを生成する"""
    unique_names = list(set([message["name"] for message in chat_data]))
    name_emoji_map = {name: random.choice(emojis) for name in unique_names}
    return name_emoji_map
```

### 5.2. 名前と音声IDのマッピング

`generate_name_voice_map`関数を使用して、登場人物の名前と音声IDのマッピングを生成します。

```python
def generate_name_voice_map(chat_data):
    """名前と音声IDのマッピングを生成する"""
    unique_names = list(set([message["name"] for message in chat_data]))
    name_voice_map = {name: random.randrange(0, 7, 1) for name in unique_names}
    return name_voice_map
```

## 6. チャットの表示

`display_chat`関数を使用して、チャットを表示します。

```python
def display_chat(chat_data, name_emoji_map, name_voice_map):
    """チャットを表示する"""
    chat_container = st.container()
    
    # JavaScriptコードを1回だけ実行
    components.html(
        """
        <script>
            window.onload = function() {
                setInterval(function() {
                    window.parent.document.querySelector('section.main').scrollTo(0, window.parent.document.querySelector('section.main').scrollHeight);
                }, 100);
            };
        </script>
        """,
        height=0
    )
    
    # チャットの表示
    for message in chat_data:
        name = message["name"]
        text = message["text"]
        number = message["number"]
        header = message["header"]
        
        # 名前に応じた絵文字を取得
        emoji = name_emoji_map.get(name, "👤")
        
        # チャットコンテナにメッセージを追加
        with chat_container:
            # メッセージの表示
            with st.chat_message("user", avatar=emoji):
                st.markdown(f"**{header}**")
    
                # 返信先の処理
                if message["replies"]:
                    reply_to = message["replies"][0][2:]
                    st.write(f"＞＞ {reply_to}")
                    
                # テキストを "。"、"！"、"!" で分割
                sentences = re.split(r'[。！!]', text)
                for sentence in sentences:
                    if sentence:
                        st.write(sentence)
                        play_audio(sentence, name_voice_map.get(name, 1))
        
        time.sleep(2)
```

ここでは、チャットコンテナを作成し、各メッセージを順番に表示します。また、JavaScriptを使用してチャットメッセージが自動的にスクロールするようにしています。

## 7. 音声の再生

`play_audio`関数を使用して、音声を再生します。

```python
def play_audio(text, voice_id):
    """音声を再生する"""
    # 音声ファイルを生成
    output_filename = f"{text}.wav"
    audio_path = f"output/{output_filename}"
    try:
        voice_data = tts.generate_audio(text, output_filename=output_filename, model_id=voice_id)
    except Exception as e:
        st.error(f"音声生成エラー: {str(e)}")
        return
    
    # 音声ファイルを読み込む
    with open(audio_path, "rb") as audio_file:
        voice_data = audio_file.read()
    
    if voice_data:
        audio_str = "data:audio/wav;base64,%s" % (base64.b64encode(voice_data).decode())
        audio_html = f"""
            <audio autoplay=True>
                <source src="{audio_str}" type="audio/wav" autoplay=True>
                Your browser does not support the audio element.
            </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    
    # 音声ファイルの読み込み
    sound = AudioSegment.from_file(audio_path, "wav")
    audio_duration = sound.duration_seconds
    
    time.sleep(audio_duration)
    
    # 生成された音声ファイルを削除
    os.remove(audio_path)
```

ここでは、指定されたテキストと音声IDを使用して音声ファイルを生成し、再生します。また、再生後に生成された音声ファイルを削除します。

## 8. メイン関数

`main`関数を使用して、アプリケーションのメイン処理を実行します。

```python
def main():
    st.title("解説求む!新しいVision Transformerアーキテクチャ「ViTAR」")
    
    if st.button("再生"):
        chat_data = load_chat_data(json_file_path)
        emojis = load_emojis(emoji_file_path)
        name_emoji_map = generate_name_emoji_map(chat_data, emojis)
        name_voice_map = generate_name_voice_map(chat_data)
        
        display_chat(chat_data, name_emoji_map, name_voice_map)

if __name__ == "__main__":
    main()
```

ここでは、「再生」ボタンがクリックされたときに、チャットデータと絵文字データを読み込み、マッピングを生成し、チャットを表示します。

以上が、ろんJのStreamlitアプリケーションの構成と機能の説明です。このアプリケーションを使用することで、論文の内容をなんJスレッド風に解説・実況することができます。初心者の方でも、コードを読むことで処理の流れを理解し、必要に応じてカスタマイズや拡張を行うことができます。
```

`docs\RonJ-Mini-30s.gif` - Error reading file: 'utf-8' codec can't decode byte 0x80 in position 6: invalid start byte

## modules

`modules\Ronj2Json.py`

```plaintext
import re
import json
import re

class Ronj2Json:
    def __init__(self, file_path):
        self.file_path = file_path
        self.markdown_text = ''
        self.result = []

    def read_markdown_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.markdown_text = f.read()

    def parse_markdown(self):
        pattern = re.compile(r'(\d+)\s名前：(.+?)\s\d{4}/\d{2}/\d{2}\(\w+\)\s\d{2}:\d{2}:\d{2}\.\d{2}\sID:\w+\n\*\*(.*?)\*\*(?:\n|$)', re.MULTILINE | re.DOTALL)
        matches = pattern.findall(self.markdown_text)

        for match in matches:
            item = {
                'number': match[0],
                'name': match[1],
                'message': match[2].strip()
            }
            self.result.append(item)

    def display_result(self):
        for item in self.result:
            print(f"{item['number']} 名前：{item['name']}")
            print(f"メッセージ：{item['message']}\n")

    def process_markdown(self):
        self.read_markdown_file()
        self.parse_markdown()
        self.display_result()
# # 使用例
# file_path = 'path/to/your/markdown/file.md'
# processor = Ronj2Json(file_path)
# processor.process_markdown()
```

`modules\tts_module.py`

```plaintext
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
```

## Template

`Template\TemplateFormat.json`

```plaintext
[
  {
    "number": "スレ番号",
    "header": "名前＋日付＋IDなど",
    "name": "名前",
    "replies": ["返信相手の番号"],
    "text": "スレ内容"
  },
  {
    "number": "スレ番号",
    "header": "名前＋日付＋IDなど",
    "name": "名前",
    "replies": ["返信相手の番号"],
    "text": "スレ内容"
  }
]
```



