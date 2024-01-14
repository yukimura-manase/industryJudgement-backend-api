# Router & Template_Render
from flask import Blueprint, render_template, jsonify
# 「.env」で設定した環境変数を使用する
import settings
# ログ出力のために、loggerをimportする
from logoutput import logger
import traceback
# Post受信をするためにFlask_requestをimportする
from flask import request, jsonify

# import requests
import pprint

import pandas as pd

import modules

# PythonからPythonScriptを呼び出すためのモジュール！ => プログラム内でコマンド実行！
# import subprocess

# Generate Router Instance => Base_URLの設定はここ！
router = Blueprint('router', __name__)


# ルート, Method: GET
@router.route('/', methods=['GET'])
def index():
    try:
        logger.debug('Flask-API-ルート起動！')
        return render_template('index.html')
    except Exception as error:
        error_msg: str = traceback.format_exc()
        logger.error(f"APIルート: Error:  {error_msg}")

# Robotama_エンドポイント, Method: GET


@router.route('/robotama', methods=['GET'])
def robotama():
    return 'Robotamaなのだ！！'

# FrontAppの情報を確認するためのエンドポイント, Method: GET


@router.route('/front_info', methods=['GET'])
def front_info():
    logger.debug('FrontApp-Info-アクセス！')
    front_end_url = settings.FRONT_APP_URL
    msg = f"FrontAppのURLは: {front_end_url}"
    return msg

# CSVの中身の情報、ColumnやRow_Dataを表示するためのエンドポイント, Method: POST


@router.route('/create_csv_info', methods=['POST'])
def create_csv_info():
    logger.debug('create_csv_info-アクセス！')
    logger.debug(request.files['file'])
    file = request.files['file']

    if file:
        # CSVファイルの読み込み
        df = pd.read_csv(file, encoding='utf-8')
        pprint.pprint(df)
        # DataFrameをJSON形式に変換
        json_data = df.to_json(orient='records')
        logger.debug(json_data)
        return json_data

    else:
        responseData = {
            'error_msg': 'Fileが存在しません！'
        }
        return jsonify(responseData)


# 「業種」情報を記入した CSVファイルを作成する
@router.route('/create_industry_csv', methods=['POST'])
def create_industry_csv():

    logger.debug('「業種」CSVファイル処理・Start')
    logger.debug(request.files['file'])
    file = request.files['file']
    result = modules.industryJudge.industryJudge(file)
    return result

# 「業種」情報を記入した 情報を CSV に逐次・書き込む処理をする


@router.route('/output_industry_csv', methods=['POST'])
def output_industry_csv():

    logger.debug('「業種」判定 JSON処理・Start')

    json_data = request.json

    print('json_data', json_data)

    result = modules.oneIndustry.industryJudge(json_data)

    return result

    # jsonify({
    #     "status": 200,
    #     "result": result,
    # })


# 「電話番号(会社の代表番号: 固定電話)から、会社名を判定したCSVファイルを作成する処理のエンドポイント」
@router.route('/phone_serch_company', methods=['POST'])
def phone_serch_company():

    file = request.files['file']

    if file:
        # CSVファイルの読み込み
        df = pd.read_csv(file, encoding='utf-8')
        pprint.pprint(df)
        # DataFrameをJSON形式に変換
        json_data = df.to_json(orient='records')
        logger.debug(json_data)
        return json_data

    else:
        responseData = {
            'error_msg': 'Fileが存在しません！'
        }
        return jsonify(responseData)


@router.route('/selenium_test', methods=['GET'])
def selenium_test():
    print('selenium_test ルーター・アクセス')
    result = modules.seleniumTest.seleniumTest()
    return jsonify({
        result: result,
    })

# @router.before_request
# def before_request(response):
#   response.headers.add('Access-Control-Allow-Origin', '*')
#   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#   return response


# Requestの後処理
@router.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
