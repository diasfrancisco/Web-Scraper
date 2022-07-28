import uuid
from io import BytesIO
from PIL import Image

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


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

class ScrapeImages:
    pass
    #     # Go to latest episode of the webtoon
    #     ep_container = self.driver.find_element(By.XPATH, '//*[@id="_listUl"]')
    #     latest_ep = ep_container.find_element(By.TAG_NAME, 'li')
    #     ep_tag = latest_ep.find_element(By.TAG_NAME, 'a')
    #     latest_ep_link = ep_tag.get_attribute('href')
    #     self.driver.get(latest_ep_link)
    #     # Bypass maturity barrier
    #     self.bypass_maturity_notice(self)

    #      # Check if previous episode button is available
    #     while len(self.driver.find_elements(By.CLASS_NAME, '_prevEpisode')) > 0:
    #         # Generate IDs for the episode and scrape image data
    #         current_ep_url = self.driver.current_url
    #         GenerateIDs.get_friendly_ID(self, current_ep_url)
    #         GenerateIDs.generate_v4_UUID(self, current_ep_url)
    #         GetDetails.webtoon_dir(self, current_ep_url)
    #         GetDetails.scrape_image_data(self, current_ep_url)
    #         # Find and click the previous button
    #         try:
    #             WebDriverWait(self.driver, const.DELAY).until(
    #                 EC.presence_of_element_located((By.CLASS_NAME, '_prevEpisode'))
    #             )
    #         except TimeoutException:
    #             print("Previous episode button did not load")
    #         prev_ep_btn = self.driver.find_element(By.CLASS_NAME, '_prevEpisode')
    #         prev_ep_btn_link = prev_ep_btn.get_attribute('href')
    #         self.driver.get(prev_ep_btn_link)
    #         time.sleep(2)
    #     GenerateIDs.get_friendly_ID(self, current_ep_url)
    #     GenerateIDs.generate_v4_UUID(self, current_ep_url)
    #     GetDetails.webtoon_dir(self, current_ep_url)
    #     GetDetails.scrape_image_data(self, current_ep_url)
    #     self.driver.close()
    #     self.driver.switch_to.window(self.driver.window_handles[0])

    # def bypass_maturity_notice(self):
    #     # Wait for the maturity notice to appear
    #     try:
    #         WebDriverWait(self.driver, const.DELAY).until(
    #             EC.presence_of_element_located((By.XPATH, '//*[@class="ly_adult"]'))
    #         )
    #         WebDriverWait(self.driver, const.DELAY).until(
    #             EC.presence_of_element_located((By.CLASS_NAME, '_ok'))
    #         )
    #         notice_container = self.driver.find_element(By.XPATH, '//*[@class="ly_adult"]')
    #         ok_btn = notice_container.find_element(By.CLASS_NAME, '_ok')
    #         ok_btn.click()
    #     except TimeoutException:
    #         pass

    # def img_urls(self):
    #     # Get all image links
    #     image_container = self.driver.find_element(By.ID, '_imageList')
    #     all_images = image_container.find_elements(By.TAG_NAME, 'img')
    #     src_list = []
    #     for img in all_images:
    #         src_list.append(img.get_attribute('src'))
    #     GetDetails.scrape_image_data(self, src_list)

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