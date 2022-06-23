import os
import time
import modules.constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from modules.genres import GetWebtoonLinks


class Webtoon(webdriver.Chrome):
    def __init__(self, executable_path=r"/usr/local/bin", collapse=False):
        # Initialise the navigation class
        self.executable_path = executable_path
        self.collapse = collapse
        os.environ['PATH'] += self.executable_path
        super(Webtoon, self).__init__()
        self.maximize_window()

    def __exit__(self, *args):
        # Exit the webpage
        if self.collapse:
            return super().__exit__(*args)

    def get_main_page(self):
        # Load the base url
        self.get(const.BASE_URL)

    def bypass_age_gate(self):
        # Enter the day
        day_path = self.find_element(By.XPATH, '//*[@id="_day"]')
        day_path.send_keys(const.DOB_DAY)

        time.sleep(1)

        # Enter the month
        month_path = self.find_element(By.XPATH, '//*[@class="lk_month"]').click()
        choose_month = self.find_element(By.XPATH, '//a[text()="10"]').click()

        time.sleep(1)

        # Enter the year
        year_path = self.find_element(By.XPATH, '//*[@class="year"]')
        actual_year_path = year_path.find_element(By.XPATH, './input')
        actual_year_path.send_keys(const.DOB_YEAR)

        time.sleep(1)

        # Press the continue button
        continue_btn = self.find_element(
            By.XPATH, "//*[@class='btn_type9 v2 _btn_enter NPI=a:enter']"
        ).click()

    def load_and_accept_cookies(self):
        try:
            # Wait until the cookies frame appear and accept them
            WebDriverWait(
                self, const.DELAY).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@class="gdpr_ly_cookie _gdprCookieBanner on"]')
                )
            )
            accept_cookies_button = WebDriverWait(
                self, const.DELAY).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@class="link _agree N=a:ckb.agree"]')
                )
            ).click()
            time.sleep(1)
        except TimeoutException:
            # If the cookies frame take longer than 10sec to load print out the following statement
            print("Took too long to load...")

    def collect_genres(self):
        genre_instance = GetWebtoonLinks(driver=self)
        genre_instance.get_genres()
        genre_instance.get_webtoon_list()