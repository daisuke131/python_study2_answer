from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager


class Driver:
    def __init__(self, is_headless: bool = True):
        self.driver: WebDriver = self.setting_driver(is_headless)

    def setting_driver(self, is_headless: bool) -> WebDriver:
        # ドライバーの読み込み
        options = webdriver.ChromeOptions()
        if is_headless:
            options.add_argument("--headless")  # ヘッドレスモードの設定
        # options.add_argument("--user-agent=ここにUA情報記入") # UA情報指定
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--incognito")  # シークレットモードの設定を付与
        options.add_argument("disable-infobars")  # AmazonLinux用
        # options.add_argument("--start-maximized")  # 画面最大化
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("log-level=3")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-desktop-notifications")
        options.add_argument("--disable-application-cache")
        options.add_argument("--lang=ja")

        try:
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            return driver
        except Exception:
            return None

    def get(self, url: str) -> bool:
        try:
            self.driver.get(url)
            return True
        except Exception:
            return False

    def find_element_by_css_selector(self, s: str):
        return self.driver.find_element_by_css_selector(s)

    def find_elements_by_css_selector(self, s: str):
        return self.driver.find_elements_by_css_selector(s)

    def find_element_by_id(self, s: str):
        return self.driver.find_element_by_id(s)

    def find_elements_by_id(self, s: str):
        return self.driver.find_elements_by_id(s)

    def find_element_by_class_name(self, s: str):
        return self.driver.find_element_by_class_name(s)

    def find_elements_by_class_name(self, s: str):
        return self.driver.find_elements_by_class_name(s)

    def find_element_by_xpath(self, s: str):
        return self.driver.find_element_by_xpath(s)

    def find_elements_by_xpath(self, s: str):
        return self.driver.find_elements_by_xpath(s)

    def quit(self) -> None:
        self.driver.quit()
