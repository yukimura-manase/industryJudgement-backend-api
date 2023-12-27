# # Excel を CSV に変換する Module

# import pandas as pd
# import os

# excel_file_path = ''
# create_csv_file_path = ''

# excel_file = '業種分類.xlsx'
# csv_file = '業種分類.csv'

# # Excel は、カレントに Setしてある前提
# excel_file_path = os.getcwd() + excel_file
# create_csv_file_path = os.getcwd() + csv_file
# # 
# read_file = pd.read_excel(excel_file_path)
# read_file.to_csv(create_csv_file_path, index = None, header=True)