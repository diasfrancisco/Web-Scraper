import uuid
import nums_from_string
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
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

class GetDetails:
    def __init__(self, driver:WebDriver):
        self.driver = driver
        self.list_of_episodes = []
        
    def navigate_pages(self, webtoon_link):
        # Open a new tab with the given link
        self.driver.execute_script(f'''window.open({webtoon_link}, "_blank");''')
        navigation_container = self.driver.find_element(By.XPATH, '//*div[@class="paginate"]')
        current_pages = navigation_container.find_elements(By.TAG_NAME, 'a')
        all_page_links = []
        for page in current_pages:
            if page.get_attribute('href') not in all_page_links:
                all_page_links.append(page.get_attribute('href'))

    def get_episodes(self):
        # Wait for the container element to appear
        try:
            WebDriverWait(self.driver, const.DELAY).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="_listUl"]'))
            )
        except TimeoutException:
            print("Episode container did not load")
        
        ep_container = self.driver.find_element(By.XPATH, '//*[@id="_listUl"]')
        eps = ep_container.find_elements(By.TAG_NAME, 'li')

        for ep in eps:
            pass

    def get_popularity_stats(self):
        pass