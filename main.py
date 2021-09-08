from time import sleep

import pandas as pd

from common.csv import write_csv
from common.driver import Driver
from common.logger import set_logger

MYNAVI_URL = "https://tenshoku.mynavi.jp/list/"
log = set_logger()


class Scrape:
    def __init__(self, search_word: str) -> None:
        self.driver = Driver()
        self.search_word: str = search_word
        self.query_word: str = self.formatting_query_word(self.search_word)
        self.query_url: str = MYNAVI_URL + self.query_word
        self.df = pd.DataFrame()

    def formatting_query_word(self, search_word: str) -> str:
        # クエリパラメータの形に整形
        search_words = search_word.split()
        query_words = []
        for word in search_words:
            query_words.append("kw" + word)
        return "_".join(query_words)

    def start_scraping(self):
        log.info("========スクレイピング開始========")
        if self.driver.get(self.query_url):
            log.info("========1ページ目読み込み完了========")
        sleep(3)
        try:
            # ポップアップを閉じる
            self.driver.execute_script('document.querySelector(".karte-close").click()')
            sleep(1)
            self.driver.execute_script('document.querySelector(".karte-close").click()')
        except Exception:
            pass
        self.fetch_scraping_data()

    def fetch_scraping_data(self):
        data_count: int = 1
        page_count: int = 2
        while True:
            corps_list = self.driver.find_elements_by_class_name(
                "cassetteRecruit__content"
            )
            for corp in corps_list:
                try:
                    self.df = self.df.append(
                        {
                            "会社名": self.fetch_corp_name(corp),
                            "勤務地": self.find_table_target_word(corp, "勤務地"),
                            "給与": self.find_table_target_word(corp, "給与"),
                        },
                        ignore_index=True,
                    )
                    log.info(f"{data_count}件目完了")
                except Exception:
                    log.error(f"{data_count}件目失敗")
                data_count += 1

            # 次のページへ
            next_page_links = self.driver.find_elements_by_class_name(
                "iconFont--arrowLeft"
            )
            if len(next_page_links) > 0:
                try:
                    next_page_link = next_page_links[0].get_attribute("href")
                    self.driver.get(next_page_link)
                    sleep(3)
                    log.info(f"========{page_count}ページ目読み込み完了========")
                    page_count += 1
                except Exception:
                    log.error(f"========{page_count}ページ目読み込み失敗========")
            else:
                break
        self.driver.quit()
        log.info("========スクレイピング終了========")

    def fetch_corp_name(self, driver):
        try:
            return driver.find_element_by_css_selector("h3").text
        except Exception:
            # データ取得できない場合はスルー
            pass

    # テーブルからヘッダーで指定した内容を取得
    def find_table_target_word(self, driver, target: str):
        try:
            table_headers = driver.find_elements_by_class_name("tableCondition__head")
            table_bodies = driver.find_elements_by_class_name("tableCondition__body")
            for table_header, table_body in zip(table_headers, table_bodies):
                if table_header.text == target:
                    return table_body.text
        except Exception:
            pass

    def write_csv(self):
        # CSVに書き込み
        if len(self.df) > 0:
            file_name = self.query_word.replace("kw", "")
            if write_csv(file_name, self.df):
                log.info(f"{len(self.df)}件出力しました。")
            else:
                log.error("csv出力失敗しました。")
        else:
            log.info("検索結果は0件です。")


def main():
    # 検索ワード入力
    search_word: str = input("検索ワード>>")
    scrape = Scrape(search_word)
    scrape.start_scraping()
    scrape.write_csv()


if __name__ == "__main__":
    main()
