from selenium import webdriver
from selenium.webdriver.common.by import By
import traceback
import os


### 作成・Module ########################################################

# 1. 電話番号(会社の代表番号: 固定電話)から、会社名を判定したCSVファイルを作成する

########################################################################


def seleniumTest():

    print('seleniumTest Call')

    # 電話番号
    tell = '019-625-5205'

    # 検索パラメーター付きの URL
    phone_number_search_web_url = f'https://www.jpnumber.com/searchnumber.do?number={tell}'
    print('検索パラメーター付きの URL')
    print(phone_number_search_web_url)

    # webdriver.Remote() で Selenium Container を指定して、接続する。
    browser = webdriver.Remote(
        command_executor=os.environ["SELENIUM_URL"],
        options=webdriver.ChromeOptions()
    )

    result = ''
    print('ブラウザ・インスタンス')
    print(browser)
    browser.get(phone_number_search_web_url)

    try:
        result_element = browser.find_element(By.XPATH, '//*[@id="result-main-right"]/div[2]/table/tbody/tr/td[1]/div/dt[2]/strong/a')
        print('電話番号検索結果')
        print(result_element)
        print(result_element.text)

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

        print('--------------------------------------------------------------')

        # 会社名を返す
        return result
