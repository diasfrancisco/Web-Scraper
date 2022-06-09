from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
url = "https://www.webtoons.com/en/gdpr/ageGate"
driver.get(url)
time.sleep(2)

def age_verification():
    day_path = driver.find_element(By.XPATH, "//*[@id='_day']")
    day_path.send_keys("24")

    month_path = driver.find_element(By.XPATH, "//*[@class='lk_month']").click()
    choose_month = driver.find_element(By.XPATH, "//*[@class='link']")
    print(choose_month)

    year_path = driver.find_element(By.XPATH, "//*[@class='year']")
    actual_year_path = year_path.find_element(By.XPATH, "./input")
    actual_year_path.send_keys("1998")

age_verification()

time.sleep(4)
driver.quit()