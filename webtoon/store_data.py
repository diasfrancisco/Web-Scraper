import os
import webtoon.constants as const
from selenium.webdriver.remote.webdriver import WebDriver
from webtoon.get_webtoons import GetWebtoonLinks


class StoreRawData(GetWebtoonLinks):
    def __init__(self, driver:WebDriver):
        super(StoreRawData, self).__init__(self.dict_of_friendly_ID)
        self.driver = driver

    def create_dir(self):
        # Check if a dir called 'raw_data' exists and if not create one
        if os.path.isdir(const.DATA_DIR_PATH):
            pass
        else:
            os.mkdir(const.DATA_DIR_PATH)

    def webtoon_dir(self):
        for key, value in self.dict_of_friendly_ID.items():
            if os.path.isdir(f'/home/diasfrancisco/GitLocal/Web-Scraper/raw_data/{value[0]}'):
                pass
            else:
                os.mkdir(f'/home/diasfrancisco/GitLocal/Web-Scraper/raw_data/{value[0]}')
