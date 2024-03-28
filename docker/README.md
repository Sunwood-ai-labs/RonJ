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