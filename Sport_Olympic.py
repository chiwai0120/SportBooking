from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.expected_conditions import *
import time

USERNAME = 'USERNAME'
PASSWORD = 'PASSWORD'
VENUE = '奧林匹克體育中心(羽毛球場)'
SPORT = '羽毛球'
VENUE_NO = ['11', '10', '9', '8', '7', '6']
DATE = '2022-11-12'
TIME = [8, 9]

driver = webdriver.Chrome('.\chromedriver')
driver.maximize_window()
wait_short = WebDriverWait(driver, 1)
wait_long = WebDriverWait(driver, 60)

driver.get('https://www.sport.gov.mo/zh/vbs')

print('Trying for login')
login = wait_short.until(presence_of_element_located((By.ID, 'username')))
login.send_keys(USERNAME)
login.send_keys(Keys.TAB + PASSWORD)
login.send_keys(Keys.ENTER)
wait_long.until(presence_of_element_located((By.CLASS_NAME, 'bt-top-menu')))
print('Login success')

for i in TIME:

    while True:
        try:
            driver.get('https://booking.sport.gov.mo/ob/zh/booking.php')
            form = wait_short.until(presence_of_element_located((By.ID, 'select_venue')))
            break
        except:
            time.sleep(1)

    Select(form.find_element(By.ID, 'venue')).select_by_visible_text(VENUE)
    Select(form.find_element(By.ID, 'sport_type')).select_by_visible_text(SPORT)
    Select(form.find_element(By.ID, 'no')).select_by_visible_text(VENUE_NO[0])
    Select(form.find_element(By.ID, 'sel_book_date')).select_by_value(DATE)
    form.find_element(By.NAME, 'Submit').click()
    wait_short.until(presence_of_element_located((By.CLASS_NAME, 'ui-button'))).click()

    try:
        print(f'Trying for {VENUE} - {SPORT}-{i} - {DATE} - {VENUE_NO[0]}')
        wait_short.until(presence_of_element_located((By.CSS_SELECTOR, f'input[name="book_time"][type="radio"][value^="{i},"]'))).click()
        driver.find_element(By.ID, 'buttonSubmit').click()
    except:
        for j in VENUE_NO[1:]:
            wait_short.until(presence_of_element_located((By.LINK_TEXT, j))).click()
            try:
                print(f'Trying for {VENUE} - {SPORT}-{i} - {DATE} - {j}')
                wait_short.until(presence_of_element_located((By.CSS_SELECTOR, f'input[name="book_time"][type="radio"][value^="{i},"]'))).click()
                driver.find_element(By.ID, 'buttonSubmit').click()
                break
            except:
                pass

    wait_long.until(presence_of_element_located((By.XPATH, '//*[@id="divContent"]/table[2]/tbody/tr/td/table/tbody/tr[3]/td/input'))).click()
    wait_short.until(presence_of_element_located((By.CSS_SELECTOR, 'input[name="payment_type"][type="radio"][value="boc"]'))).click()
    driver.find_element(By.ID, 'sendSMS').click()
    print(f'Booking for {VENUE} - {SPORT}-{i} - {DATE} success')

driver.close()


