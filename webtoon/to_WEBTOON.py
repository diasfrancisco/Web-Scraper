from concurrent.futures import ProcessPoolExecutor
from lib2to3.pgen2 import driver
import os
import time
import json
import asyncio

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import webtoon.constants as const
from webtoon.get_webtoons import GetWebtoonLinks
from webtoon.single_webtoon import GetDetails
from webtoon.create_dirs import CreateDirs
from webtoon.single_episode import ScrapeImages


class Webtoon(webdriver.Chrome):
    def __init__(self, executable_path=r"/usr/local/bin", collapse=False):
        # Initialise the navigation class
        self.executable_path = executable_path
        self.collapse = collapse
        os.environ['PATH'] += self.executable_path
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        super(Webtoon, self).__init__(options=options)

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
        self.find_element(By.XPATH, '//*[@class="lk_month"]').click()
        self.find_element(By.XPATH, '//a[text()="10"]').click()

        time.sleep(1)

        # Enter the year
        year_path = self.find_element(By.XPATH, '//*[@class="year"]')
        actual_year_path = year_path.find_element(By.XPATH, './input')
        actual_year_path.send_keys(const.DOB_YEAR)

        time.sleep(1)

        # Press the continue button
        self.find_element(
            By.XPATH, "//*[@class='btn_type9 v2 _btn_enter NPI=a:enter']"
        ).click()

    def load_and_accept_cookies(self):
        try:
            # Wait until the cookies frame appear and accept them
            WebDriverWait(
                self, const.DELAY).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@class="gdpr_ly_cookie _gdprCookieBanner on"]' and '//*[@class="link _agree N=a:ckb.agree"]')
                )
            )
        except TimeoutException:
            # If the cookies frame take longer than 10sec to load print out the following statement
            print("Took too long to load...")
        accept_cookies_button = self.find_element(By.XPATH, '//*[@class="link _agree N=a:ckb.agree"]')
        accept_cookies_button.click()
 
    def create_main_dirs(self):
        main_dirs = CreateDirs()
        main_dirs.static_dirs()

    def scrape_genres_and_webtoon_urls(self):
        # Calls the class and methods needed to get genres and webtoon urls
        genres_and_webtoon_urls = GetWebtoonLinks(driver=self)
        genres_and_webtoon_urls.get_genres()
        genres_and_webtoon_urls.get_webtoon_list()

    def get_webtoon_info(self):
        with open(const.GENRES_AND_WEBTOON_URLS_DIR_PATH + '/webtoon_urls.json', 'r') as f:
            dict_of_webtoon_links = json.load(f)

        info = GetDetails(driver=self)
        for webtoon_list in dict_of_webtoon_links.values():
            info.get_basic_info(webtoon_list)

    def get_IDs_and_imgs(self):
        scrape_imgs = ScrapeImages(driver=self)
        pass
