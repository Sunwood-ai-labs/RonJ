import asyncio
import json
import websockets

class VTubeStudioAPI:
    def __init__(self, api_endpoint):
        # VTube StudioのAPIエンドポイントを設定
        self.api_endpoint = api_endpoint
        self.websocket = None
        self.auth_token = None

    async def connect(self):
        # WebSocketに接続
        self.websocket = await websockets.connect(self.api_endpoint)

    async def close(self):
        # WebSocketを閉じる
        await self.websocket.close()

    async def send_request(self, payload):
        # リクエストを送信し、レスポンスを受信
        await self.websocket.send(json.dumps(payload))
        response = await self.websocket.recv()
        return json.loads(response)

    async def authenticate(self, plugin_name, plugin_developer):
        # 認証トークンを取得するためのリクエストを作成
        auth_token_payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "AuthenticationTokenRequest",
            "messageType": "AuthenticationTokenRequest",
            "data": {
                "pluginName": plugin_name,
                "pluginDeveloper": plugin_developer
            }
        }
        response = await self.send_request(auth_token_payload)
        self.auth_token = response["data"]["authenticationToken"]

        # 認証リクエストを作成し、送信
        auth_payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "AuthenticationRequest",
            "messageType": "AuthenticationRequest",
            "data": {
                "pluginName": plugin_name,
                "pluginDeveloper": plugin_developer,
                "authenticationToken": self.auth_token
            }
        }
        await self.send_request(auth_payload)

    async def get_available_models(self):
        # 利用可能なモデルの一覧を取得するリクエストを作成
        payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "AvailableModelsRequest",
            "messageType": "AvailableModelsRequest"
        }
        response = await self.send_request(payload)
        return response["data"]["availableModels"]

    async def load_model(self, model_id):
        # モデルを読み込むリクエストを作成
        payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "ModelLoadRequest",
            "messageType": "ModelLoadRequest",
            "data": {
                "modelID": model_id
            }
        }
        await self.send_request(payload)

    async def get_expressions(self):
        # 表情の一覧を取得するリクエストを作成
        payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "ExpressionStateRequest",
            "messageType": "ExpressionStateRequest",
            "data": {
                "details": True,
                "expressionFile": ""
            }
        }
        response = await self.send_request(payload)
        return response["data"]["expressions"]

    async def activate_expression(self, expression_file):
        # 表情を適用するリクエストを作成
        payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "ExpressionActivationRequest",
            "messageType": "ExpressionActivationRequest",
            "data": {
                "expressionFile": expression_file,
                "active": True
            }
        }
        await self.send_request(payload)