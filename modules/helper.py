from selenium import webdriver

from selenium.webdriver.support import expected_conditions as EC

import time
from selenium.webdriver.common.keys import Keys

from dotenv import load_dotenv
import os

load_dotenv()


def login_in_instagram():
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    driver = webdriver.Safari()

    print(f"login start")

    login_url = "https://www.instagram.com/accounts/login/"
    driver.get(login_url)
    time.sleep(10)

    instagram_id_form = driver.find_element('name', 'username')
    instagram_id_form.send_keys(username)
    time.sleep(0.2)

    # Looping login to avoid bot detection
    for char in password:
        password_field = driver.find_element('name', "password")
        password_field.send_keys(char)
        time.sleep(0.2)

    # instagram_login_btn = ".sqdOP.L3NKy.y3zKF     "
    instagram_id_form.send_keys(Keys.ENTER)
    time.sleep(10)

    print(f"login end")

    return driver
