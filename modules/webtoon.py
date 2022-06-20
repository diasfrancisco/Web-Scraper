import os
import time
from unicodedata import name
import modules.constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class Webtoon(webdriver.Chrome):
    def __init__(self, executable_path=r"/usr/local/bin", collapse=False):
        # Initialise the web driver
        self.executable_path = executable_path
        self.collapse = collapse
        self.genre_list = []
        self.links = []
        self.dict_of_webtoon_link = {}
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
        continue_btn = self.find_element(By.XPATH, "//*[@class='btn_type9 v2 _btn_enter NPI=a:enter']").click()

    def load_and_accept_cookies(self):
        try:
            # Wait until the cookies frame appear and accept them
            WebDriverWait(self, const.COOKIE_FRAME_DELAY).until(EC.presence_of_element_located((By.XPATH, '//*[@class="gdpr_ly_cookie _gdprCookieBanner on"]')))
            accept_cookies_button = WebDriverWait(self, const.COOKIE_FRAME_DELAY).until(EC.presence_of_element_located((By.XPATH, '//*[@class="link _agree N=a:ckb.agree"]'))).click()
            time.sleep(1)
        except TimeoutException:
            # If the cookies frame take longer than 10sec to load print out the following statement
            print("Took too long to load...")

    def get_genres(self):
        genre_button = self.find_element(By.XPATH, '//*[@class="NPI=a:genre,g:en_en"]').click() # Go to the genres tab
        
        time.sleep(1)

        # Grab the name of all genres in the main section
        main_genres = self.find_element(By.XPATH, '//*[@class="snb _genre"]')
        main_genre_tags = main_genres.find_elements(By.TAG_NAME, 'li')
        for main_tag in main_genre_tags:
            main_genre_name = main_tag.find_element(By.TAG_NAME, 'a')
            if main_genre_name.get_attribute('class') == '':
                pass
            else:
                self.genre_list.append(main_genre_name.text)
            
        # Grab the name of all genres in the 'others' section
        other_button = self.find_element(By.CLASS_NAME, 'g_others')
        other_button.find_element(By.TAG_NAME, 'a').click()

        other_genres = self.find_element(By.XPATH, '//*[@class="ly_lst_genre as_genre"]')
        other_genre_tags = other_genres.find_elements(By.TAG_NAME, 'li')
        for other_tag in other_genre_tags:
            other_genre_name = other_tag.find_element(By.TAG_NAME, 'a')
            self.genre_list.append(other_genre_name.text)

        print(self.genre_list)

    def get_all_webtoons(self):
        time.sleep(5)
        for genre in self.genre_list:
            genre_container = self.find_element(By.XPATH, '//*h2[contains(text(), "sub_title g_")]/following-sibling::ul')
            webtoons = genre_container.find_elements(By.TAG_NAME, 'li')
        
        print(webtoons)
            #for webtoon in webtoons:
                #link_tag = webtoon.find_element(By.TAG_NAME, 'a')
                #webtoon_link = link_tag.get_attribute('href')
                #self.links.append(webtoon_link)
