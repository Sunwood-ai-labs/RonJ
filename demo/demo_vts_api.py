import requests
import os
import time
import asyncio
import random
import sys
import pprint
from loguru import logger

# モジュールディレクトリをシステムパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# VTubeStudioAPIモジュールをインポート
from modules.VTubeStudioAPI import VTubeStudioAPI

async def switch_models_and_expressions(vts_api):
    # 利用可能なモデルの一覧を取得
    models = await vts_api.get_available_models()
    logger.info(f"models num: {len(models)}")
    

    # 各モデルを順番に切り替え、ランダムに表情を適用
    for i, model in enumerate(models):
        model_id = model["modelID"]
        model_name = model["modelName"]
        await vts_api.load_model(model_id)
        logger.info(f"Loaded model name: {model_name}")
        logger.info(f"Loaded model id: {model_id}")
        logger.info(f"Loaded model i: {i}")

        # 表情の一覧を取得
        expressions = await vts_api.get_expressions()

        # 表情が存在する場合、ランダムに選択して適用
        if expressions:
            random_expression = random.choice(expressions)
            expression_file = random_expression["file"]
            expression_name = random_expression["name"]
            await vts_api.activate_expression(expression_file)
            logger.info(f"Activated expression: {expression_name}")
        else:
            logger.info("No expressions found for this model")

        await asyncio.sleep(5)  # 5秒間の待機

async def main():
    # VTube StudioのAPIエンドポイントとプラグイン情報を設定
    api_endpoint = "ws://host.docker.internal:8001"
    plugin_name = "ModelSwitcher"
    plugin_developer = "MakiMaki"

    # VTubeStudioAPIクラスのインスタンスを作成
    vts_api = VTubeStudioAPI(api_endpoint)
    await vts_api.connect()  # APIに接続
    await vts_api.authenticate(plugin_name, plugin_developer)  # プラグインの認証

    # モデルの切り替えとランダムな表情の適用を実行
    await switch_models_and_expressions(vts_api)

    await vts_api.close()  # APIとの接続を切断

# メイン関数の実行
asyncio.get_event_loop().run_until_complete(main())