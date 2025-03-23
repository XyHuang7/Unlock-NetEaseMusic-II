# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00A19BF17463CBE190C7CED4D4781A7F6CB654D353350FB0C212EC24B919DCC99ED0B34DD0AE9ABA6AE6CD3A4C45EA8E6B6DD68DF42DD1E510BCAF1B15D138082F31A82E9E816E4F1D9F3D7A20F8CA1B2A1B407B7FA89CC56CEF0D7C3B3A6C1D1C52A765C7E8A7770E1CC1575C9F8BA227C1902283278A69F1F59A5B72CC3D07E1EF5205C54DB33FA493834B5A6E0C75A7B0628AA9E102AC6458AD04DF004BE0B0D34620A4863DBAF1E74398ADB8629899FC492ECB17607C1E2BAD9C3312359F0D184ED332529909B63220686ED28971055C8E81296E2E80782148021031B01F3B99DBCB8EE7E1927A0FDCA793ADD5B2C0B524CF1479C6543DABE16BBB7EF9F1592C889F08FC4749A7F03FACE209AEAF333054272CA111E4F6378262A043D65B4B74B55FC8FEB2A740B35FC05F7CA2833533B15466B6D17525A3D700802F3CB0C65DCDED7D0CFEC4EEC664A1E781F7FD02534E20672E603DF33ED210A85C20BE2A"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
