import os, logging, time, random
from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pysentimiento.preprocessing import preprocess_tweet

#options = Options()

#options.add_argument("--headless")
#options.add_argument("--start-maximized")
#options.add_experimental_option("excludeSwitches", ["enable-automation"])
#options.add_experimental_option('useAutomationExtension', False)

#DRIVER_OPTIONS = options

env_vars = dotenv_values(".env")

def login_in_instagram():

    try:
        username = env_vars.get("USERNAME")
        password = env_vars.get("PASSWORD")

    except:
        raise Exception("Please set your username and password in the .env file")

    driver = webdriver.Chrome()
    #driver = webdriver.Safari()

    logging.info(f"login start")

    login_url = "https://www.instagram.com/accounts/login/"
    driver.get(login_url)
    time.sleep(10)

    instagram_id_form = driver.find_element('name', 'username')
    #instagram_id_form = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
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

    logging.info(f"login end")

    return driver

def preprocess(comment_string):
    try:
        return preprocess_tweet(comment_string)
    except:
        return ''
    
def timer_load_comment():
     return random.randint(5,10)

def timer_load_page():
     return random.randint(10,15)

def getXPaths():
    xpath_express_base = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[2]/div["
    xpath_title = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div/span/div/span"
    rest_of_xpath_comment = "]/div[1]/div/div[2]/div[1]/div[1]/div/div[2]/span"
    rest_of_xpath_likes = "]/div[1]/div/div[2]/div[1]/div[2]/div[1]/span/span"

    return xpath_express_base, xpath_title, rest_of_xpath_comment, rest_of_xpath_likes

def scroll_comments(driver):
    comments_section_xpath = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[2]'
    comments_section = driver.find_element(By.XPATH, comments_section_xpath)
    driver.execute_script("arguments[0].scrollIntoView(false);", comments_section)
    time.sleep(timer_load_comment())