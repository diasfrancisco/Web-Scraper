from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

driver = webdriver.Chrome()
url = 'https://www.webtoons.com/en/gdpr/ageGate'
driver.get(url)
time.sleep(2)

def index_html():
    print("PART 2")

def load_and_accept_cookies():
    delay = 10
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@class="gdpr_ly_cookie _gdprCookieBanner on"]')))
        accept_cookies_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@class="link _agree N=a:ckb.agree"]'))).click()
        time.sleep(1)
    except TimeoutException:
        print("Took too long to load...")

    index_html()

def age_verification():
    day_path = driver.find_element(By.XPATH, '//*[@id="_day"]')
    day_path.send_keys("24")

    month_path = driver.find_element(By.XPATH, '//*[@class="lk_month"]').click()
    choose_month = driver.find_element(By.XPATH, '//a[text()="10"]')
    choose_month.click()

    year_path = driver.find_element(By.XPATH, '//*[@class="year"]')
    actual_year_path = year_path.find_element(By.XPATH, './input')
    actual_year_path.send_keys("1998")

    time.sleep(1)

    continue_btn = driver.find_element(By.XPATH, "//*[@class='btn_type9 v2 _btn_enter NPI=a:enter']").click()

    load_and_accept_cookies()

age_verification()

time.sleep(4)
driver.quit()