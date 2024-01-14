from selenium import webdriver
from selenium.webdriver.common.by import By
import traceback
import os

### Module 説明 ########################################################

# 1. 電話番号(会社の代表番号: 固定電話)から、会社名を判定したCSVファイルを作成する

########################################################################

# 電話番号から、会社名を判定する処理


def phoneSearchCompany(tell):

    # 電話番号検索の Web サイト URL に 検索パラメーターを付ける
    phone_number_search_web_url = f'https://www.jpnumber.com/searchnumber.do?number={tell}'
    print('検索パラメーター付きの URL')
    print(phone_number_search_web_url)

    # 会社名: 会社名を発見できない場合は、空文字を返す
    result = ''

    try:
        # webdriver.Remote() で Selenium Container を指定して、接続する。
        browser = webdriver.Remote(
            command_executor=os.environ["SELENIUM_URL"],
            options=webdriver.ChromeOptions()
        )

        browser.get(phone_number_search_web_url)

        # 会社名・Elementを取得する
        result_element = browser.find_element(By.XPATH, '//*[@id="result-main-right"]/div[2]/table/tbody/tr/td[1]/div/dt[2]/strong/a')
        result = result_element.text

    except Exception as error:
        # traceback.format_exc() で例外の詳細情報を取得する
        error_msg: str = traceback.format_exc()
        print(error_msg)
        # 例外を無視したい場合は、pass を使用する
        pass

    finally:
        # ブラウザを閉じる (エラーが発生しても必ず実行)
        browser.quit()

        # 会社名を返す
        return result

# 電話番号のリストから、会社名を判定したCSVファイルを作成する処理


def createNewCsvFromPhoneList(industry_json_params):
    print('電話番号のリストから、会社名を判定して、CSVファイルを作成する処理')

    # JSONファイル

    # CSV の Column・Row List を取得する
    column_row = industry_json_params['colmunRow']

    # 会社名, 業種, 電話番号 の Index を取得する
    company_idx = column_row.index("会社名")
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
