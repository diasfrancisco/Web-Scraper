import uuid
import nums_from_string
from selenium.webdriver.remote.webdriver import WebDriver


class GetDetails:
    def __init__(self, driver:WebDriver):
        self.driver = driver

    def get_friendly_ID(self, webtoon_link):
        friendly_ID = nums_from_string.get_nums(webtoon_link)
        self.dict_of_friendly_ID[webtoon_link] = friendly_ID

    def generate_v4_UUID(self, webtoon_link):
        v4_UUID = str(uuid.uuid4())
        self.dict_of_v4_UUID[webtoon_link] = v4_UUID

    def get_episodes():
        pass