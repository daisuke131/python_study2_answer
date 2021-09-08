import logging
import os
from datetime import datetime
from pathlib import Path

LOG_FORMAT = (
    "%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s"
)
LOG_DIR_NAME = "logs"


def set_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # LOGフォルダがない場合は作成
    log_folder_path = os.path.join(os.getcwd(), LOG_DIR_NAME)
    dir = Path(log_folder_path)
    dir.mkdir(parents=True, exist_ok=True)

    # ログの設定
    now_time = datetime.now()
    formatter = logging.Formatter(LOG_FORMAT)

    # ファイル出力用のHandlerを設定
    fh = logging.FileHandler(
        filename=f"{log_folder_path}/{now_time:log_%Y%m%d%H%M%S}.log", encoding="utf-8"
    )
    fh.setFormatter(formatter)
    fh.setLevel = logging.INFO

    # コンソール出力用のHandlerを設定
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    sh.setLevel = logging.INFO

    # Logerに登録
    logger.addHandler(fh)
    logger.addHandler(sh)

    return logger
