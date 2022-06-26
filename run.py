from webtoon.to_WEBTOONS import Webtoon


def main():
    with Webtoon(collapse=False) as bot:
        bot.get_main_page()
        bot.bypass_age_gate()
        bot.load_and_accept_cookies()
        bot.check_if_dir_exists()
        bot.collect_genres()
        #bot.scrape_webtoon()

if __name__=="__main__":
    main()