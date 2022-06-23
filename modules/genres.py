from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import modules.constants as const
import time


class GetWebtoonLinks:
    # Initialise the link collection class
    def __init__(self, driver:WebDriver):
        self.driver = driver
        self.genre_list = []
        self._g_list = []
        self.dict_of_webtoon_links = {}

    def get_genres(self):
        self.driver.find_element(By.XPATH, '//*[@class="NPI=a:genre,g:en_en"]').click() # Go to the genres tab

        time.sleep(2)

        # Wait for the main genre element to appear
        try:
            WebDriverWait(self.driver, const.DELAY).until(
                EC.presence_of_element_located((By.XPATH, '//*[@class="snb _genre"]' and '//*[@class="g_others"]'))
            )
        except TimeoutException:
            print("Genre element did not load")

        # Grab the name of all genres in the main section
        main_genres = self.driver.find_element(By.XPATH, '//*[@class="snb _genre"]')
        main_genre_lis = main_genres.find_elements(By.TAG_NAME, 'li')
        # Will be used for display purposes
        for li_1 in main_genre_lis:
            main_genre_name = li_1.find_element(By.TAG_NAME, 'a')
            if main_genre_name.get_attribute('class') == '':
                pass
            else:
                self.genre_list.append(main_genre_name.text)
        # Will be used to find certain elements in the future
        for _ in main_genre_lis:
            _main_name = _.get_attribute('data-genre')
            if _main_name == "OTHERS":
                pass
            else:
                self._g_list.append(_main_name)
            
            
        # Grab the name of all genres in the 'others' section
        other_button = self.driver.find_element(By.CLASS_NAME, 'g_others')
        other_button.find_element(By.TAG_NAME, 'a').click()

        other_genres = self.driver.find_element(By.XPATH, '//*[@class="ly_lst_genre as_genre"]')
        other_genre_lis = other_genres.find_elements(By.TAG_NAME, 'li')
        # Will be used for display purposes
        for li_2 in other_genre_lis:
            other_genre_name = li_2.find_element(By.TAG_NAME, 'a')
            self.genre_list.append(other_genre_name.text)
        # Will be used to find certain elements in the future
        for _ in main_genre_lis:
            _other_name = _.get_attribute('data-genre')
            if _other_name == "OTHERS":
                pass
            else:
                self._g_list.append(_other_name)

        return self.genre_list, self._g_list

    def get_webtoon_list(self):
        # Wait for the container element to appear
        try:
            WebDriverWait(self.driver, const.DELAY).until(
                EC.presence_of_element_located((By.XPATH, '//*[@class="card_wrap genre"]'))
            )
        except TimeoutException:
            print("Container did not load")

        genre_container = self.driver.find_element(
            By.XPATH, '//*[@class="card_wrap genre"]'
        )
        for genre in self._g_list:
            webtoon_container = genre_container.find_element(
                By.XPATH, f'//h2[@data-genre="{genre}"]/following-sibling::ul'
            )
            webtoons = webtoon_container.find_elements(By.TAG_NAME, 'li')
            all_links = self.get_all_webtoon_links(webtoons)
            self.dict_of_webtoon_links[genre] = all_links
        return self.dict_of_webtoon_links

    def get_all_webtoon_links(self, webtoons):
        list_of_links = []
        for webtoon in webtoons:
            link_tag = webtoon.find_element(By.TAG_NAME, 'a')
            webtoon_link = link_tag.get_attribute('href')
            list_of_links.append(webtoon_link)
        return list_of_links
