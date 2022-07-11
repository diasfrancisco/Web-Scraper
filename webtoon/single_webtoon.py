import os
import uuid
import time
import requests
from io import BytesIO
from PIL import Image

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import webtoon.constants as const


class GenerateIDs:
    def __init__(self, driver:WebDriver):
        self.driver = driver

    def get_friendly_ID(self, current_ep_url):
        # Obtain a friendly ID using the numbers in the 'title no='
        # section of the current url
        split_url = current_ep_url.split("/")[5:7]
        friendly_ID = "-".join(split_url)
        self.dict_of_friendly_ID[current_ep_url] = friendly_ID

    def generate_v4_UUID(self, current_ep_url):
        # Generate a unique v4 UUID using the uuid library and save it to
        # a dictionary
        v4_UUID = str(uuid.uuid4())
        self.dict_of_v4_UUID[current_ep_url] = v4_UUID

class GetDetails:
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
        latest_ep_link = ep_tag.get_attribute('href')
        self.driver.get(latest_ep_link)
        # Bypass maturity barrier
        GetDetails.bypass_maturity_notice(self)

        # Check if previous episode button is available
        while len(self.driver.find_elements(By.CLASS_NAME, '_prevEpisode')) > 0:
            # Generate IDs for the episode and scrape image data
            current_ep_url = self.driver.current_url
            GenerateIDs.get_friendly_ID(self, current_ep_url)
            GenerateIDs.generate_v4_UUID(self, current_ep_url)
            GetDetails.webtoon_dir(self, current_ep_url)
            GetDetails.scrape_image_data(self, current_ep_url)
            # Find and click the previous button
            try:
                WebDriverWait(self.driver, const.DELAY).until(
                    EC.presence_of_element_located((By.CLASS_NAME, '_prevEpisode'))
                )
            except TimeoutException:
                print("Previous episode button did not load")
            prev_ep_btn = self.driver.find_element(By.CLASS_NAME, '_prevEpisode')
            prev_ep_btn_link = prev_ep_btn.get_attribute('href')
            self.driver.get(prev_ep_btn_link)
            time.sleep(2)
        GenerateIDs.get_friendly_ID(self, current_ep_url)
        GenerateIDs.generate_v4_UUID(self, current_ep_url)
        GetDetails.webtoon_dir(self, current_ep_url)
        GetDetails.scrape_image_data(self, current_ep_url)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def bypass_maturity_notice(self):
        # Wait for the maturity notice to appear
        try:
            WebDriverWait(self.driver, const.DELAY).until(
                EC.presence_of_element_located((By.XPATH, '//*[@class="ly_adult"]'))
            )
            WebDriverWait(self.driver, const.DELAY).until(
                EC.presence_of_element_located((By.CLASS_NAME, '_ok'))
            )
            notice_container = self.driver.find_element(By.XPATH, '//*[@class="ly_adult"]')
            ok_btn = notice_container.find_element(By.CLASS_NAME, '_ok')
            ok_btn.click()
        except TimeoutException:
            pass

    def get_webtoon_info(self, webtoon_link):
        info_dict = {}
        # Wait for the episode container to appear
        try:
            WebDriverWait(self.driver, const.DELAY).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'info'))
            )
            info_container = self.driver.find_element(By.CLASS_NAME, 'info')
            time.sleep(2)
        except TimeoutException:
            print("Episode container did not load")
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

    def scrape_image_data(self, current_ep_url):
        # Get all image links
        image_container = self.driver.find_element(By.ID, '_imageList')
        all_images = image_container.find_elements(By.TAG_NAME, 'img')
        img_counter = 1
        for img in all_images:
            # Get the link to a single image and go to the website using the ep_link
            # as a referer
            source = img.get_attribute('src')
            img_site = requests.get(source, headers={'referer': current_ep_url})
            if img_site.status_code == 200:
                # If the site loads up successfuly with status code 200, save the image
                image = Image.open(BytesIO(img_site.content))
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                webtoon_ID = current_ep_url.split("/")[5]
                episode_ID = self.dict_of_friendly_ID[current_ep_url]
                path = f'/home/cisco/GitLocal/Web-Scraper/raw_data/{webtoon_ID}/{episode_ID}/images/{episode_ID}_{img_counter}'
                img_counter += 1
                # Open a file using the path generated and save the image as a JPEG file
                with open(path, "wb") as f:
                    image.save(f, "JPEG")

    def webtoon_dir(self, current_ep_url):
        # Create a new directory for each webtoon and further children
        # directories if they do not exist
        webtoon_folder = current_ep_url.split("/")[5]
        if os.path.isdir(f'/home/cisco/GitLocal/Web-Scraper/raw_data/{webtoon_folder}'):
            pass
        else:
            os.mkdir(f'/home/cisco/GitLocal/Web-Scraper/raw_data/{webtoon_folder}')
        GetDetails.episode_dir(self, current_ep_url, webtoon_folder)

    def episode_dir(self, current_ep_url, webtoon_folder):
        # Create a new directory for each webtoon and further children
        # directories if they do not exist
        episode_folder = self.dict_of_friendly_ID[current_ep_url]
        if os.path.isdir(f'/home/cisco/GitLocal/Web-Scraper/raw_data/{webtoon_folder}/{episode_folder}'):
            pass
        else:
            os.mkdir(f'/home/cisco/GitLocal/Web-Scraper/raw_data/{webtoon_folder}/{episode_folder}')
        GetDetails.images_dir(self, webtoon_folder, episode_folder)

    def images_dir(self, webtoon_folder, episode_folder):
        # Creates an image directory if it doesn't exist
        if os.path.isdir(f'/home/cisco/GitLocal/Web-Scraper/raw_data/{webtoon_folder}/{episode_folder}/images'):
            pass
        else:
            os.mkdir(f'/home/cisco/GitLocal/Web-Scraper/raw_data/{webtoon_folder}/{episode_folder}/images')