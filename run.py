from os import link
from modules.navigate import Webtoon


def main():
    with Webtoon(collapse=False) as bot:
        bot.get_main_page()
        bot.bypass_age_gate()
        bot.load_and_accept_cookies()
        bot.collect_genres()

if __name__=="__main__":
    main()