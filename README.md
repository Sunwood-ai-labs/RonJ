<p align="center">
  <img alt="OpenDevin Logo" src="./docs/icon.png" width="400" />
</p>


# ろんJ - 論文を面白おかしく理解するツール

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-available-blue)](https://www.docker.com/)

論文は難しそうで読むのが億劫だと感じたことはありませんか？でもそんな人でも、「ろんJ」を使えば論文の内容が面白おかしく理解できるかもしれません。

「ろんJ」は、アップロードした論文の内容を、あの有名な２ちゃんねるの「なんでも実況J」（通称：なんJ）のスレッド風に解説・実況してくれる画期的なサービスです。難解な論文の内容を、親しみやすいなんJのノリで楽しく理解することができます。

## 特徴

- 論文の内容をなんJスレッド風に自動解説
- 音声合成による臨場感あふれる実況
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

3. セットアップが完了したら、ブラウザで `http://localhost:8502/` にアクセスしてください。

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

## 連絡先

質問やフィードバックがある場合は、[メールアドレス]までお気軽にお問い合わせください。

---

ろんJで、論文の理解が楽しくなること間違いなし！さっそく使ってみましょう！