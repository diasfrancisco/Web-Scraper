from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

def Start():
    driver = webdriver.Chrome()
    url = 'https://www.webtoons.com/en/gdpr/ageGate'
    driver.get(url)
    driver.implicitly_wait(10)

    def get_genres():
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@class="NPI=a:genre,g:en_en"]').click() # Go to the genres tab
        time.sleep(1)

        # Grab the name of all genres in the main section
        genre_list = []

        main_genres = driver.find_element(By.XPATH, '//*[@class="snb _genre"]')
        main_genre_tags = main_genres.find_elements(By.TAG_NAME, 'li')
        for main_tag in main_genre_tags:
            main_genre_name = main_tag.find_element(By.TAG_NAME, 'a')
            if main_genre_name.get_attribute('class') == '':
                pass
            else:
                genre_list.append(main_genre_name.text)
            
        # Grab the name of all genres in the 'others' section
        other_button = driver.find_element(By.CLASS_NAME, 'g_others')
        other_button.find_element(By.TAG_NAME, 'a').click()

        other_genres = driver.find_element(By.XPATH, '//*[@class="ly_lst_genre as_genre"]')
        other_genre_tags = other_genres.find_elements(By.TAG_NAME, 'li')
        for other_tag in other_genre_tags:
            other_genre_name = other_tag.find_element(By.TAG_NAME, 'a')
            genre_list.append(other_genre_name.text)

        print(genre_list)

    def load_and_accept_cookies():
        delay = 10
        try:
            # Wait until the cookies frame appear and accept them
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@class="gdpr_ly_cookie _gdprCookieBanner on"]')))
            accept_cookies_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@class="link _agree N=a:ckb.agree"]'))).click()
            time.sleep(1)
        except TimeoutException:
            # If the cookies frame take longer than 10sec to load print out the following statement
            print("Took too long to load...")

        get_genres()

    def bypass_age_verification():
        # Enter the day
        day_path = driver.find_element(By.XPATH, '//*[@id="_day"]')
        day_path.send_keys("24")

        # Enter the month
        month_path = driver.find_element(By.XPATH, '//*[@class="lk_month"]').click()
        choose_month = driver.find_element(By.XPATH, '//a[text()="10"]').click()

        # Enter the year
        year_path = driver.find_element(By.XPATH, '//*[@class="year"]')
        actual_year_path = year_path.find_element(By.XPATH, './input')
        actual_year_path.send_keys("1998")

        time.sleep(1)

        # Press the continue button
        continue_btn = driver.find_element(By.XPATH, "//*[@class='btn_type9 v2 _btn_enter NPI=a:enter']").click()

        load_and_accept_cookies()

    bypass_age_verification()

    time.sleep(4)
    driver.quit()

Start()