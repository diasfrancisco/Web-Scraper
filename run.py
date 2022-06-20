from modules.webtoon import Webtoon

with Webtoon(collapse=True) as web_scraper:
    web_scraper.get_main_page()
    web_scraper.bypass_age_gate()
    web_scraper.load_and_accept_cookies()
    web_scraper.get_genres()
    web_scraper.get_all_webtoons()