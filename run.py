from webtoon.to_WEBTOONS import Webtoon


def main():
    with Webtoon(collapse=True) as bot:
        bot.get_main_page()
        bot.bypass_age_gate()
        bot.load_and_accept_cookies()
        bot.create_raw_data_dir()
        bot.scrape_webtoon()

if __name__=="__main__":
    main()