import io
import os
import uuid
import time
import requests
import nums_from_string
from PIL import Image
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import webtoon.constants as const


class GenerateIDs:
    def __init__(self, driver:WebDriver):
        self.driver = driver

    def get_friendly_ID(self, webtoon_link):
        # Obtain a friendly ID using the numbers in the 'title no='
        # section of the current url
        friendly_ID = nums_from_string.get_nums(webtoon_link)
        self.dict_of_friendly_ID[webtoon_link] = friendly_ID

    def generate_v4_UUID(self, webtoon_link):
        # Generate a unique v4 UUID using the uuid library and save it to
        # a dictionary
        v4_UUID = str(uuid.uuid4())
        self.dict_of_v4_UUID[webtoon_link] = v4_UUID

class GetDetails():
    def __init__(self, driver:WebDriver):
        self.driver = driver

    def get_episodes(self, webtoon_link):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(webtoon_link)
        
        # Wait for the episode container to appear
        try:
            WebDriverWait(self.driver, const.DELAY).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="_listUl"]'))
            )
        except TimeoutException:
            print("Episode container did not load")
        
        GetDetails.get_webtoon_info(self, webtoon_link)
        # Go to latest episode of the webtoon
        ep_container = self.driver.find_element(By.XPATH, '//*[@id="_listUl"]')
        latest_ep = ep_container.find_element(By.TAG_NAME, 'li')
        ep_tag = latest_ep.find_element(By.TAG_NAME, 'a')
        ep_link = ep_tag.get_attribute('href')
        self.driver.get(ep_link)

        GetDetails.bypass_maturity_notice(self)
        GetDetails.scrape_image_data(self, webtoon_link)
        self.driver.close()

    def bypass_maturity_notice(self):
        # Wait for the maturity notice to appear
        try:
            WebDriverWait(self.driver, const.DELAY).until(
                EC.presence_of_element_located((By.XPATH, '//*[@class="ly_adult"]'))
            )
            notice_container = self.driver.find_element(By.XPATH, '//*[@class="ly_adult"]')
            btn_area = notice_container.find_element(By.CLASS_NAME, 'btnarea')
            time.sleep(5)
            ok_btn = btn_area.find_element(By.CLASS_NAME, 'btn1_cancel')
            time.sleep(1)
            ok_btn.click()
        except TimeoutException:
            pass

    def get_webtoon_info(self, webtoon_link):
        info_dict = {}
        info_container = self.driver.find_element(By.CLASS_NAME, 'info')
        # Get info on genre, title and author
        genre = info_container.find_element(By.XPATH, '//h2')
        info_dict["Genre"] = [genre.text]
        title = info_container.find_element(By.XPATH, '//h1')
        info_dict["Title"] = [title.text]
        author = info_container.find_element(By.CLASS_NAME, 'author_area')
        info_dict["Author"] = [author.text]

        stats_container = self.driver.find_element(By.CLASS_NAME, 'grade_area')
        # Get all stat details (views, subscribers, rating)
        try:
            WebDriverWait(self.driver, const.DELAY).until(
                EC.presence_of_element_located((By.XPATH, '//span[@class="ico_view"]/following-sibling::em'))
            )
            WebDriverWait(self.driver, const.DELAY).until(
                EC.presence_of_element_located((By.XPATH, '//span[@class="ico_subscribe"]/following-sibling::em'))
            )
            WebDriverWait(self.driver, const.DELAY).until(
                EC.presence_of_element_located((By.XPATH, '//span[@class="ico_grade5"]/following-sibling::em'))
            )
        except TimeoutException:
            print("Stats did not load")
        views = stats_container.find_element(
            By.XPATH, '//*[@class="ico_view"]/following-sibling::em'
        )
        info_dict["Views"] = [views]
        subscribers = stats_container.find_element(
            By.XPATH, '//*[@class="ico_subscribe"]/following-sibling::em'
        )
        info_dict["Subscribers"] = [subscribers]
        rating = stats_container.find_element(
            By.XPATH, '//*[@class="ico_grade5"]/following-sibling::em'
        )
        info_dict["Rating"] = [rating]

        self.dict_of_webtoon_info[webtoon_link] = [info_dict]

        return self.dict_of_webtoon_info

    def scrape_image_data(self, webtoon_link):
        image_container = self.driver.find_element(By.ID, '_imageList')
        all_images = image_container.find_elements(By.TAG_NAME, 'img')
        img_counter = 1
        for img in all_images:
            source = img.get_attribute('src')
            img_content = requests.get(source)
            image = Image.open(io.BytesIO(img_content.content))
            path_instance = GetDetails.get_download_path(webtoon_link, img_counter)
            
            with open(path_instance, "wb") as f:
                image.save(f, "JPEG")
    
    def get_download_path(self, webtoon_link, img_counter):
        ID_for_path = self.dict_of_friendly_ID.get(webtoon_link, default=None)
        path = f'/home/diasfrancisco/GitLocal/Web-Scraper/raw_data/{ID_for_path[0]}/images/{ID_for_path}_{img_counter}'
        img_counter += 1
        return path, img_counter

    def webtoon_dir(self):
        # Create a new directory for each webtoon and further children
        # directories if they do not exist
        for key, value in self.dict_of_friendly_ID.items():
            if os.path.isdir(f'/home/diasfrancisco/GitLocal/Web-Scraper/raw_data/{value[0]}'):
                pass
            else:
                os.mkdir(f'/home/diasfrancisco/GitLocal/Web-Scraper/raw_data/{value[0]}')
            GetDetails.images_dir(value)

    def images_dir(self, value):
        # Creates an image directory if it doesn't exist
        if os.path.isdir(f'/home/diasfrancisco/GitLocal/Web-Scraper/raw_data/{value[0]}/images'):
            pass
        else:
            os.mkdir(f'/home/diasfrancisco/GitLocal/Web-Scraper/raw_data/{value[0]}/images')
            