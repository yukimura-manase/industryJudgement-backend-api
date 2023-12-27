FROM python:3.8-slim-buster

# Docker Image内で実行される作業ディレクトリ(Path)を指定する: ない場合は作ってくれます。
WORKDIR /usr/src/app

# Flask環境変数: Dockerコンテナ内で、Flaskがアプリケーションを正しく検出し、起動できるようになります。
ENV FLASK_APP=app

# Hostマシンの appディレクトリ を Container側のPath(/usr/src/app)に COPY(追加)する
COPY ./app ./

# Docker Imageを作成する際に、コマンドが実行される: Imageにパッケージを追加している。
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt