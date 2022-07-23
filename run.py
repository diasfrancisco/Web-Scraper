from tracemalloc import start
from webtoon.to_WEBTOONS import Webtoon
import time


def main():
    with Webtoon(collapse=True) as bot:
        start_time = time.time()
        bot.get_main_page()
        bot.bypass_age_gate()
        bot.load_and_accept_cookies()
        bot.create_raw_data_dir()
        print(time.time() - start_time)
        bot.scrape_genres_and_webtoon_urls()
        bot.scrape_data()
        print(time.time() - start_time)

if __name__=="__main__":
    main()