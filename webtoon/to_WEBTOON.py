from lib2to3.pgen2 import driver
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import webtoon.constants as const
from webtoon.get_webtoons import GetWebtoonLinks
from webtoon.single_webtoon import GetDetails
from webtoon.create_dirs import CreateDirs


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
        IDs_and_imgs = GetDetails(driver=self)
        webtoon_dict = self.scrape_genres_and_webtoon_urls()[1]
        drama = webtoon_dict.get('DRAMA')
        url = drama[0]
        IDs_and_imgs.get_basic_info(webtoon_url=url)
        # for webtoon in webtoon_dict:
        #     data_collection = GetDetails(driver=self)

    # def get_img_urls(self):
    #     pass

    # def scrape_image_data(self, src_list):
    #     with FuturesSession(executor=ThreadPoolExecutor, max_workers=100) as session:
    #         futures = [session.get(src, headers={'referer': src} for src in src_list)]
    #         if src.status_code == 200:
    #             # If the site loads up successfuly with status code 200, save the image
    #             image = Image.open(BytesIO(img_site.content))
    #             if image.mode != 'RGB':
    #                 image = image.convert('RGB')
    #             webtoon_ID = current_ep_url.split("/")[5]
    #             episode_ID = self.dict_of_friendly_ID[current_ep_url]
    #             path = f'/home/cisco/GitLocal/Web-Scraper/raw_data/{webtoon_ID}/{episode_ID}/images/{episode_ID}_{img_counter}'
    #             img_counter += 1
    #             # Open a file using the path generated and save the image as a JPEG file
    #             with open(path, "wb") as f:
    #                 image.save(f, "JPEG")
