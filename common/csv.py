from datetime import datetime
from pathlib import Path

CSV_FILE_PATH = "./csv/{file_name}_{datetime}_data.csv"


def write_csv(file_name: str, df) -> bool:
    # csvフォルダがなければ作成
    dir = Path("./csv")
    dir.mkdir(parents=True, exist_ok=True)
    # path作成
    csv_path = CSV_FILE_PATH.format(
        file_name=file_name, datetime=datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    )
    # 行番号なしで出力
    try:
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        return True
    except Exception:
        return False
