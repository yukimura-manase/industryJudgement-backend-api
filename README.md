# Industry Judgement App BackEnd API

## App 概要

- 会社名と電話番号から、業種を判定するツールの BackEnd-API

- Flask-API と Selenium の 2 つの Container を動かします。

## 環境構築方法(初期 setup)

<br>

### 0. DockerNetwork を作成する

[F-E] と [B-E]の Docker Compose 間で、通信するための共通の Network を作成しておきます。  
`docker network create` コマンドで、独自の Network を作成することができます。

```bash
docker network create industry_judgement_app_network
```

`docker network ls` コマンドで、Docker Network の一覧を確認することができます。

```bash
docker network ls
```

### 1. プロジェクトを Clone

```bash
git clone git@github.com:yukimura-manase/industryJudgement-backend-api.git
```

## 2. 環境によって、docker-compose.yml の使用イメージを変える

- 注意事項、M1 Mac など ARM で動作する環境かどうかで、使用するイメージが変わります。

- ARM 対応の Selenium Docker Image を使わないと M1 Mac などでは動きません。

  - 詳細は、[Python Selenium について](https://zenn.dev/manase/scraps/28fe7b34824e79)をご参照ください。

  - ちなみに、ARM 対応の Image 名は、docker-selenium ではなく、 docker-seleniarm になっている。。。芸が細かい。。。

- 環境に応じて、`docker-compose.yml`の編集をお願いします。

### 3. docker-compose で Dockerfile から image をビルドする

プロジェクトルートに移動します。

```bash
cd industryJudgement-backend-api
```

続いて、Dockerfile から Docker Image を作成します。  
docker-compose build コマンドは、Dockerfile から image を作成してくれるコマンドです。

```bash
docker-compose build
```

このコマンドを実行すると、Dockerfile に従って各サービスの Docker イメージがビルドされ、
<br/>
イメージ名とタグ名が作成されます。

### 4. Docker Image の ビルドを確認する

docker image ls で、build された image を確認しておきます。

```bash
docker image ls
```

### 5. docker-compose で Docker コンテナを実行する

次のコマンドで、Docker Compose ファイルに定義されたサービスをバックグラウンドで起動できます。

```bash
docker-compose up -d
```

Docker Image の Build と Container の実行を同時に実施する場合は、次のコマンドです。

```bash
docker-compose up --build
```

### 6. docker-compose で コンテナの起動状況を確認する

Docker コンテナの起動状況は、`docker container ps` コマンドで確認できます。

```bash
docker container ps
```

### 7. Web ブラウザからアクセスする

http://localhost:5001/api/ にアクセスして、BackEnd-API の起動を確認します。

### 8. Docker コンテナの停止 & 削除

docker-compose down コマンドを使用して、すべてのコンテナを停止し、削除することができます。

```bash
docker-compose down
```

## 参考・引用

1. [Python Selenium について](https://zenn.dev/manase/scraps/28fe7b34824e79)
