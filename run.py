from webtoon.to_WEBTOON import Webtoon
import time


def main():
    with Webtoon(collapse=True) as bot:
        start_time = time.time()
        bot.get_main_page()
        bot.bypass_age_gate()
        bot.load_and_accept_cookies()
        bot.create_main_dirs()
        bot.scrape_genres_and_webtoon_urls()
        print(f'Completed genre and webtoon url collection in {time.time() - start_time} seconds')
        bot.get_webtoon_info()
        print(f'Gathered all webtoon info in {time.time() - start_time} seconds')

if __name__=="__main__":
    main()