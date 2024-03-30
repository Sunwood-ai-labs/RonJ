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
from loguru import logger
import aiohttp
import asyncio

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
json_file_path = st.sidebar.text_input("JSONファイルのパス", "data/FitbitDI_KANA.json")
emoji_file_path = st.sidebar.text_input("絵文字のテキストファイルのパス", "assets/emojis.txt")
api_url = st.sidebar.text_input("音声生成のAPIエンドポイント", "http://style-bert-vits2-api:5000/voice")

VTUBESTUDIO_MODEL_NUM = 7
STYLE_BERT_MODEL_NUM = 7


# TextToSpeechインスタンスを作成
tts = TextToSpeech(api_url=api_url)

async def switch_model(model_index=0, random_expression=False):
    url = "http://vts:8787/switch_model"
    data = {"model_index": model_index, "random_expression": random_expression}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                result = await response.json()
                print(result["message"])
            else:
                print(f"Error: {response.status}")

def load_chat_data(json_file_path):
    """チャットデータをJSONファイルから読み込む。"""
    try:
        with open(json_file_path, "r") as f:
            chat_data = json.load(f)
        
        # コードブロックのパターンを定義
        code_block_pattern = re.compile(r"```[a-z]+\n.*?\n```", re.DOTALL)
        
        # コードブロックを削除
        for item in chat_data:
            item["text_KANA"] = re.sub(code_block_pattern, "", item["text_KANA"])
        
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
    name_voice_map = {name: random.randrange(0, STYLE_BERT_MODEL_NUM, 1) for name in unique_names}
    return name_voice_map

def generate_name_model_map(chat_data):
    """名前とModle IDのマッピングを生成する"""
    unique_names = list(set([message["name"] for message in chat_data]))
    name_model_map = {name: random.randrange(0, VTUBESTUDIO_MODEL_NUM, 1) for name in unique_names}
    return name_model_map

async def display_chat(chat_data, name_emoji_map, name_voice_map, name_model_map):
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
        text_KANA = message["text_KANA"]
        number = message["number"]
        header = message["header"]
        
        logger.info(f"text_KANA:{text_KANA}")
        logger.info(f"text:{text}")

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
                    
                # テキストを "。"、"！"、"!"、そして改行で分割
                sentences = re.split(r'[。！!\n?？]', text_KANA)
                await switch_model(model_index=name_model_map.get(name, 1), random_expression=True)
                st.markdown(text)

                for sentence in sentences:
                    if sentence:
                        # model switch
                        play_audio(sentence, name_voice_map.get(name, 1))
        
        time.sleep(2)

def play_audio(text, voice_id):
    """音声を再生する"""
    # 音声ファイルを生成
    output_filename = f"{text}.wav".replace("/", "_")
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

async def main():
    # st.title("解説求む!新しいVision Transformerアーキテクチャ「ViTAR」")
    st.title("【朗報】FitbitDI、AI駆使した究極の健康管理アプリ爆誕！ Jの者も健康的になれるんか？")
    
    if st.button("再生"):
        chat_data = load_chat_data(json_file_path)
        emojis = load_emojis(emoji_file_path)
        name_emoji_map = generate_name_emoji_map(chat_data, emojis)
        name_voice_map = generate_name_voice_map(chat_data)
        name_model_map = generate_name_model_map(chat_data)
        logger.info(f"name_model_map:{name_model_map}")

        await display_chat(chat_data, name_emoji_map, name_voice_map, name_model_map)

if __name__ == "__main__":
    asyncio.run(main())
