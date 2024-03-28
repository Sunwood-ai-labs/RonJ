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