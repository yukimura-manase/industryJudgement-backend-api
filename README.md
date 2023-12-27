# Industry Judgement App BackEnd API

- 会社名と電話番号から、業種を判定するツールのBackEnd-API

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
git clone 
```

### 2. docker-compose で Dockerfile から image をビルドする

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

### 3. Docker Image の ビルドを確認する

docker image ls で、build された image を確認しておきます。

```bash
docker image ls
```

### 4. docker-compose で Docker コンテナを実行する

次のコマンドで、Docker Compose ファイルに定義されたサービスをバックグラウンドで起動できます。

```bash
docker-compose up -d
```

### 5. docker-compose で コンテナの起動状況を確認する

Docker コンテナの起動状況は、`docker container ps` コマンドで確認できます。

```bash
docker container ps
```

### 6. Web ブラウザからアクセスする

http://localhost:5001/api/ にアクセスして、BackEnd-API の起動を確認します。

### 7. Docker コンテナの停止 & 削除

docker-compose down コマンドを使用して、すべてのコンテナを停止し、削除することができます。

```bash
docker-compose down
```

---

## 【 関連記事・学習用の記事 】

<br>

### 1. Docker で Python・Flask 環境を構築する方法

[Docker で Python・Flask 環境を構築する方法(ハンズオン講座)](https://masanyon.com/docker-python-flask-env-dockerfile-dockercompose/)

### 2. Docker コンテナの中に入って標準出力を実行する方法: Log 確認\_Develop_Debug_Skill

[Docker コンテナの中に入って標準出力を実行する方法・確認する方法](https://masanyon.com/docker-container-exec-it-logs-inside/)

### 3. 別々の docker-compose.yml で作成された Docker コンテナを Network 接続する方法

[別々の docker-compose.yml で作成された Docker コンテナを Network 接続する方法](https://masanyon.com/docker-docker-compose-yml-container-network-share/)
