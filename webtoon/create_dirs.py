import os

import webtoon.constants as const


class CreateDirs:
    def static_dirs(self):
        # Check if the following dirs exists and if not create one
        if os.path.isdir(const.RAW_DATA_DIR_PATH):
            pass
        else:
            os.mkdir(const.RAW_DATA_DIR_PATH)
        
        if os.path.isdir(const.GENRES_AND_WEBTOON_URLS_DIR_PATH):
            pass
        else:
            os.mkdir(const.GENRES_AND_WEBTOON_URLS_DIR_PATH)

        if os.path.isdir(const.ALL_WEBTOONS_DIR_PATH):
            pass
        else:
            os.mkdir(const.ALL_WEBTOONS_DIR_PATH)

    def webtoon_dir(self, webtoon_url):
        # Create a new directory for each webtoon and further children
        # directories if they do not exist
        webtoon_folder = webtoon_url.split("/")[5]
        if os.path.isdir(f'/home/cisco/GitLocal/Web-Scraper/raw_data/all_webtoons/{webtoon_folder}'):
            pass
        else:
            os.mkdir(f'/home/cisco/GitLocal/Web-Scraper/raw_data/all_webtoons/{webtoon_folder}')

    def episode_dir(self, current_ep_url, webtoon_folder):
        # Create a new directory for each webtoon and further children
        # directories if they do not exist
        episode_folder = self.dict_of_friendly_ID[current_ep_url]
        if os.path.isdir(f'/home/cisco/GitLocal/Web-Scraper/raw_data/{webtoon_folder}/{episode_folder}'):
            pass
        else:
            os.mkdir(f'/home/cisco/GitLocal/Web-Scraper/raw_data/{webtoon_folder}/{episode_folder}')

    def images_dir(self, webtoon_folder, episode_folder):
        # Creates an image directory if it doesn't exist
        if os.path.isdir(f'/home/cisco/GitLocal/Web-Scraper/raw_data/{webtoon_folder}/{episode_folder}/images'):
            pass
        else:
            os.mkdir(f'/home/cisco/GitLocal/Web-Scraper/raw_data/{webtoon_folder}/{episode_folder}/images')
