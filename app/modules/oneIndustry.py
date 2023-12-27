### 業種を判定する Python Module ###

# 1. CSV を受け取る

# 2. 

# 3. 

# src/global/pqueue

######################################################################## 

## Import Block ##
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage, # システムメッセージ 
    HumanMessage, # 人間の質問 
    AIMessage, # ChatGPTの返答
)

import openai
import json
import pprint
import dotenv
import os

import pandas as pd
import traceback

OPENAI_KEY='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'


def industryJudge(industry_json_params) :

  print('1つ1つ業種判定をする Python Script Start！')

  # print('industryJudge Start')

  ### 1. ChatGPTの設定(人格)・プロンプト作成 ###

  # 1-1. 設定・プロンプト
  prompt = '''
    あなたは、日本の会社に詳しいChatbotとして、質問に対して、必ずJSONの形で回答します。
    また、あなたは、以下の制約条件を厳密に守る必要があります。

    制約条件: 
    * あなたは、日本の会社に詳しいChatbotで、必ずJSONの形で回答します。
    * あなたは、「業種」に対する回答の事例の中から、最適な「業種」を選んで、JSONデータを作成する必要があります。
    * 回答の JSONフォーマットは、回答フォーマットにあるような industry という key に回答が紐づいている形です。

    回答フォーマット: 
    {"industry":"回答"}
  '''

  # 1-2. 業種の一覧・JSONデータを読み込む
  industry_json_path = f'{os.getcwd()}/industry.json'
  industry_json_file = open(industry_json_path, 'r', encoding="utf-8")
  industry_json_data = json.load(industry_json_file)

  # 1-3. 業種に対する回答の事例
  industry_answer_text = f'''
    「業種」に対する回答の事例: 
  '''

  # 1-4. 業種に対する回答の事例に、業種情報を追加する
  for value in industry_json_data:
    industry_answer_text = f'{industry_answer_text}\n * {value["industry"]}'

  # print('industry_answer_text')
  # print(industry_answer_text)
  # print('----------------------------------------------------')

  # 1-5. 設定・プロンプト に 業種に対する回答の事例を結合する
  prompt = f'{prompt}\n {industry_answer_text}'

  # print('prompt')
  # print(prompt)
  # print('----------------------------------------------------')

  column_row = industry_json_params['colmunRow']

  target_row = industry_json_params['targetRow']

  # 会社名
  company_name = target_row[1]

  print('company_name')
  print(company_name)
  print('----------------------------------------------------')

  # 2-2. 質問文
  question = f'''
    質問：{company_name}の「業種」は何ですか？ 回答は、「業種」に対する回答の事例の中から選んでください。
  '''

  # ChatGPT・Instance ##
  llm = ChatOpenAI(
    openai_api_key=OPENAI_KEY,
    # model="gpt-3.5-turbo",
    model="gpt-4",
    temperature=0, # 精度をできるだけ高くする
  )

  ## LLM に渡すための Messageを作成する
  messages = [
    SystemMessage(content=prompt), # System Message = AIの「キャラ設定」のようなもの 
    HumanMessage(content=question) # 提案する内容 
  ]
  response = llm(messages)
  json_string = response.content

  # Pythonで、文字列として、渡された JSONデータの形をJSONデータにする 
  json_data = json.loads(json_string)

  # 業種
  industry = json_data['industry']

  print('industry: ', industry)
  print(f'[判定・成功] {company_name}:{industry}')
  print('----------------------------------------------------')

  target_row[9] = industry


  print('target_row')
  print(target_row)
  print('----------------------------------------------------')

  # return target_row

  json_encode = json.dumps(target_row, ensure_ascii=False, indent=2)
  print('json_encode')
  print(json_encode)
  print('----------------------------------------------------')

  return json_encode


  ### 2. 質問文・プロンプトを作成する ###

  # 2-1. 「業種」を書き込みたい(Update Target) CSV を DataFlameに変換する
  # target_file = 'hubspot-crm-exports--2023-11-15.csv'
  # target_file_path = f'{os.getcwd()}/{target_file}'
  
  # target_file_df = pd.read_csv(target_file, encoding="utf-8")

  

  # # 2-2. 業種判定のResultList
  # industry_answer_list = []

  # try: 
  #   # 2-3. DataFrame から 業種の Recode を1つ1つ取得する & ChatGPTで質問する
  #   for company_name in target_file_df['会社名']:
  #     # 2-2. 質問文
  #     question = f'''
  #       質問：{company_name}の「業種」は何ですか？ 回答は、「業種」に対する回答の事例の中から選んでください。
  #     '''

  #     # ChatGPT・Instance ##
  #     llm = ChatOpenAI(
  #       openai_api_key=OPENAI_KEY,
  #       # model="gpt-3.5-turbo",
  #       model="gpt-4",
  #       temperature=0, # 精度をできるだけ高くする
  #     )

  #     ## LLM に渡すための Messageを作成する
  #     messages = [
  #       SystemMessage(content=prompt), # System Message = AIの「キャラ設定」のようなもの 
  #       HumanMessage(content=question) # 提案する内容 
  #     ]
  #     response = llm(messages)
  #     json_string = response.content

  #     # Pythonで、文字列として、渡された JSONデータの形をJSONデータにする 
  #     json_data = json.loads(json_string)
  #     industry = json_data['industry']

  #     # 業種 Data を List に追加する
  #     industry_answer_list.append(industry)

  #     print(f'[判定・成功] {company_name}:{industry}')



  # except Exception as error :
  #   # traceback.format_exc() で例外の詳細情報を取得する
  #   error_msg:str = traceback.format_exc()
  #   print(error_msg)
  #   print(f'[判定・失敗] {company_name}')

  #   # ChatGPT での判定・処理中に Error が起こったら、業種判定は空白のままにする
  #   industry_answer_list.append("")

  # print('industry_answer_list')
  # print(industry_answer_list)
  # print('----------------------------------------------------')


  # # 3. 業種 Column を DataFlame に追加する
  # target_file_df['業種'] = industry_answer_list

  # # new_csv_file = 'result.csv'
  # # create_csv_file_path = f'{os.getcwd()}/{new_csv_file}'

  # # # 4. DataFlame を CSV に変換して Export する
  # # result = target_file_df.to_csv(create_csv_file_path, index = None, header=True)

  # # print('最終結果')
  # # print(result)
  # # print('----------------------------------------------------')


  # # 5. JSON データにする場合
  # json_data = target_file_df.to_json(orient='records', force_ascii=False)

  # print('json_data')
  # print(json_data)
  # print('----------------------------------------------------')

  # return {
  #   'result': json_data,
  # }
