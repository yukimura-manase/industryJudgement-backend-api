### 業種を判定する Python Module ###

# 1. CSV を受け取る

# 2.

# 3.

########################################################################

## Import Block ##
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,  # システムメッセージ
    HumanMessage,  # 人間の質問
    AIMessage,  # ChatGPTの返答
)

import openai
import json
import pprint
import dotenv
import os

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
from selenium.webdriver.chrome.service import Service

## 環境変数 ##
dotenv.load_dotenv('.env')

print('個別・業種判定 Module Call')
print('ロボたま')

# 1. Project・Root Path
project_root = os.path.abspath("../")
print('project_root', project_root)

# 2. OPENAI_KEY を取得する
OPENAI_KEY = dotenv.get_key('.env', 'OPENAI_KEY')
print('OPENAI_KEY: ', OPENAI_KEY)
print('------------------------------------------------------------')


def industryJudge(industry_json_params):

    print('1つ1つ業種判定をする Python Script Start！')

    # print('industryJudge Start')

    ### 1. ChatGPTの設定(人格)・プロンプト作成 ###

    # 1-1. ChatGPTの設定(人格)・プロンプト
    prompt = '''
    あなたは、日本の会社に詳しいChatbotとして、質問に対して、必ずJSONの形で回答します。
    また、あなたは、以下の制約条件と回答条件を厳密に守る必要があります。

    制約条件: 
    * あなたは、日本の会社に詳しいChatbotで、必ずJSONの形で回答します。
    * 「業種」を判断する際の参考情報として、あなたの知識と合わせて、以下の「事業内容・業種」の情報(説明文)も参考にしてください。
    
    「事業内容・業種」の情報(説明文):
    '''

    # CSV の Column・Row List を取得する
    column_row = industry_json_params['colmunRow']

    # 会社名, 業種, 電話番号 の Index を取得する
    company_idx = column_row.index("会社名")
    industry_idx = column_row.index("業種")
    phone_idx = column_row.index("電話番号")

    # Table の Target Row を取得する
    target_row = industry_json_params['targetRow']
    # 会社名
    company_name = target_row[company_idx]
    # 電話番号
    phone_number = target_row[phone_idx]

    print('company_name')
    print(company_name)
    print('phone_number')
    print(phone_number)
    print('----------------------------------------------------')

    # 2. 電話番号(会社の代表番号: 固定電話)と会社名から「事業内容・業種」の情報(説明文)を取得する
    scraping_results = industry_info_scraping(company_name, phone_number)
    print('Webスクレイピングの結果()')
    print(scraping_results)
    print('----------------------------------------------------')
    # 質問文に、事業内容・業種の情報(説明文)を追加して、質問する

    # 3. プロンプトに、事業内容・業種の情報(説明文)を追加する
    for description in scraping_results:
        print('description')
        print(description)
        prompt = f'{prompt}\n * {description}'

    print('作成された質問文(「 会社名 電話番号 事業内容・業種 」で検索)')
    print(prompt)
    print('----------------------------------------------------')

    # 業種の一覧・JSONデータを読み込む
    industry_json_path = f'{os.getcwd()}/industry.json'
    industry_json_file = open(industry_json_path, 'r', encoding="utf-8")
    industry_json_data = json.load(industry_json_file)

    # 4. 業種に対する回答の事例
    industry_answer_text = '''
    回答条件:
    * あなたは、「業種」に対する回答の事例の中から、最適な「業種」を選んで、JSONデータを作成する必要があります。
    * 回答の JSONフォーマットは、回答フォーマットにあるような industry という key に回答が紐づいている形です。

    回答フォーマット:
    {"industry":"回答"}

    「業種」に対する回答の事例:
    '''

    # 5. 業種に対する回答の事例に、業種情報を追加する
    for value in industry_json_data:
        industry_answer_text = f'{industry_answer_text}\n * {value["industry"]}'

    # print('industry_answer_text')
    # print(industry_answer_text)
    # print('----------------------------------------------------')

    # 6. 設定・プロンプト に 業種に対する回答の事例を結合する
    prompt = f'{prompt}\n {industry_answer_text}'

    print('最終的に完成したプロンプト')
    print('----------------------------------------------------')
    print(prompt)
    print('----------------------------------------------------')

    # 7. 質問文
    question = f'''
    質問：{company_name}の「業種」は何ですか？ 回答は、「業種」に対する回答の事例の中から選んでください。
    '''

    # ChatGPT・Instance ##
    llm = ChatOpenAI(
        openai_api_key=OPENAI_KEY,
        # model="gpt-3.5-turbo",
        model="gpt-4",
        temperature=0,  # 精度をできるだけ高くする
    )

    # 8. LLM に渡すための Messageを作成する
    messages = [
        SystemMessage(content=prompt),  # System Message = AIの「キャラ設定」のようなもの
        HumanMessage(content=question)  # 提案する内容
    ]
    response = llm(messages)
    json_string = response.content

    try:
        # Pythonで、文字列として、渡された JSONデータの形をJSONデータにする
        json_data = json.loads(json_string)

        # 業種
        industry = json_data['industry']

        print('industry: ', industry)
        print(f'[判定・成功] {company_name}:{industry}')
        print('----------------------------------------------------')

        target_row[industry_idx] = industry

        print('target_row')
        print(target_row)
        print('----------------------------------------------------')

    except Exception as error:
        # traceback.format_exc() で例外の詳細情報を取得する
        error_msg: str = traceback.format_exc()
        print(error_msg)
        target_row[industry_idx] = '業種判定エラー'

        # 例外を無視したい場合は、pass を使用する
        pass

    # finally-ブロック => 必ず最後に実行される処理
    finally:
        json_encode = json.dumps(target_row, ensure_ascii=False, indent=2)
        print('json_encode')
        print(json_encode)
        print('----------------------------------------------------')

        print('必ず最後に実行したり処理を実行するブロック')
        return json_encode


### industry_info_scraping ###############################################

# 1. 会社名と電話番号(会社の代表番号: 固定電話)から「事業内容・業種」の情報を取得する

##########################################################################

def industry_info_scraping(company_name, tell):

    print('Webスクレイピングの Python Script Start！')

    # webdriver.Remote() で Selenium Container を指定して、接続する。
    browser = webdriver.Remote(
        command_executor=os.environ["SELENIUM_URL"],
        options=webdriver.ChromeOptions()
    )

    try:
        browser.get('https://www.google.com/')

        # 検索ボックスを見つける
        search_box = browser.find_element(By.ID, 'APjFqb')

        # 検索キーワード
        search_word = f'{company_name} {tell} 事業内容・業種'
        print(search_word)

        # 検索キーワードを入力
        search_box.send_keys(search_word)

        # 検索を実行する(Enterキーを送信して検索を実行)
        search_box.send_keys(Keys.RETURN)

        # submit() でも検索できる
        # search_box.submit()

        # 検索結果画面が表示されるまで待機
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, 'search'))
        )

        # description (説明文)のTextを格納する List
        search_result_list = []

        # 上から、3つまでの description (説明文)を取得する
        target_max = 3

        # find_elements で、検索結果の description (説明文)をすべて取得する
        description_lists = browser.find_elements(By.CLASS_NAME, 'VwiC3b')
        # print(description_lists)

        # 各要素の中の <span> タグからテキストを取得する (上から、3つまで)
        for index in range(len(description_lists)):
            try:
                if index + 1 > target_max:
                    break
                else:
                    element = description_lists[index]

                    span_text = element.find_element(By.TAG_NAME, 'span').text
                    print(span_text)
                    print('-------------------------------------------------------------')
                    search_result_list.append(span_text)

            except Exception as error:
                # 例外を無視したい場合は、pass を使用する
                pass

    except Exception as error:
        # traceback.format_exc() で例外の詳細情報を取得する
        error_msg: str = traceback.format_exc()
        print(error_msg)
        pass

    finally:
        # ブラウザを閉じる (エラーが発生しても必ず実行)
        browser.quit()
        print('取得した説明文・Text の List')
        print(search_result_list)

        return search_result_list
