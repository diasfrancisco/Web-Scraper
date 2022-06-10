from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
url = "https://www.webtoons.com/en/gdpr/ageGate"
driver.get(url)
time.sleep(2)

def index_html():
    print("PART 2")

def age_verification():
    day_path = driver.find_element(By.XPATH, "//*[@id='_day']")
    day_path.send_keys("24")

    month_path = driver.find_element(By.XPATH, "//*[@class='lk_month']").click()
    choose_month = driver.find_element(By.XPATH, "//a[text()='10']")
    choose_month.click()

    year_path = driver.find_element(By.XPATH, "//*[@class='year']")
    actual_year_path = year_path.find_element(By.XPATH, "./input")
    actual_year_path.send_keys("1998")

    time.sleep(1)

    continue_btn = driver.find_element(By.XPATH, "//*[@class='btn_type9 v2 _btn_enter NPI=a:enter']").click()

    index_html()

age_verification()

time.sleep(4)
driver.quit()