import os
import random
import sys
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# モジュールディレクトリをシステムパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# VTubeStudioAPIモジュールをインポート
from modules.VTubeStudioAPI import VTubeStudioAPI

app = FastAPI()

class ModelRequest(BaseModel):
    model_index: Optional[int] = None
    random_expression: Optional[bool] = False

# VTube StudioのAPIエンドポイントとプラグイン情報を設定
api_endpoint = "ws://host.docker.internal:8001"
plugin_name = "ModelSwitcher"
plugin_developer = "MakiMaki"

# VTubeStudioAPIクラスのインスタンスを作成
vts_api = VTubeStudioAPI(api_endpoint)

@app.on_event("startup")
async def startup_event():
    await vts_api.connect()  # APIに接続
    await vts_api.authenticate(plugin_name, plugin_developer)  # プラグインの認証

@app.post("/switch_model")
async def switch_model(request: ModelRequest):
    # 利用可能なモデルの一覧を取得
    models = await vts_api.get_available_models()

    if request.model_index is not None:
        # 指定されたモデルのインデックスが有効か確認
        if 0 <= request.model_index < len(models):
            model = models[request.model_index]
            await vts_api.load_model(model["modelID"])
        else:
            raise HTTPException(status_code=400, detail="Invalid model index")
    else:
        # モデルのインデックスが指定されていない場合、ランダムにモデルを選択
        model = random.choice(models)
        await vts_api.load_model(model["modelID"])

    # ランダムな表情の適用が指定されている場合
    if request.random_expression:
        # 表情の一覧を取得
        expressions = await vts_api.get_expressions()

        # 表情が存在する場合、ランダムに選択して適用
        if expressions:
            random_expression = random.choice(expressions)
            expression_file = random_expression["file"]
            await vts_api.activate_expression(expression_file)

    return {"message": "Model switched successfully"}

@app.on_event("shutdown")
async def shutdown_event():
    await vts_api.close()  # APIとの接続を切断

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)