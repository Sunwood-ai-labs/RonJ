import asyncio
import aiohttp
import time
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

async def main():
    # モデルのリストの番号を指定してモデルを切り替える
    await switch_model(model_index=3, random_expression=True)
    
    time.sleep(3)
    # ランダムな表情を適用してモデルを切り替える
    await switch_model(random_expression=True)

    time.sleep(3)
    # モデルのリストの番号を指定せずにモデルを切り替える（ランダムなモデルが選択される）
    await switch_model()

if __name__ == "__main__":
    asyncio.run(main())