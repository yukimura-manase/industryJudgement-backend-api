import logging
from logging.handlers import TimedRotatingFileHandler

# LogLevelを読み込むため。
import settings

loglevel = settings.LOG_LEVEL_CONF
logging.basicConfig(level=loglevel)

logger = logging.getLogger('log_test.py')

# ログフォーマットを設定する
# 実行時間(年-月-日 時-分-秒,ミリ秒): ファイル名: 行番号 : ログレベル名 : メッセージ文字列
formatter = logging.Formatter(
  '%(asctime)s: %(filename)s: %(lineno)d: %(levelname)s: %(message)s'
)

# 2. TimedRotatingFileHandler => ファイルに対するログ出力をローテーションできる
# ログファイルのローテート設定(Ver.日時)

# 2-1. 1日ごとにログファイルがローテーションされ、バックアップファイルは20ファイル(20日分)まで保存されます。
day_rotaite_handler = TimedRotatingFileHandler(
  filename='./logs/day.log', 
  when='D', 
  interval=1, 
  backupCount=20, 
  encoding='utf-8'
)

# 2-2. 作成されるログファイル名には、ローテーション時に年月日が付加されます
day_rotaite_handler.suffix = "%Y%m%d"
day_rotaite_handler.setFormatter(formatter)
logger.addHandler(day_rotaite_handler)

# 標準出力に出力する
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)

