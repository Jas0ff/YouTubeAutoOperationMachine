import os

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import time


def guise_chrome():
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")  # 關閉自動測試提示
    options.add_argument("--headless")  # 無視窗模式
    options.add_argument("--incognito")  # 無痕
    options.add_argument("--mute-audio")  # 靜音

    path = os.getcwd()+'\\videos'
    prefs = {"download.default_directory": path}
    options.add_experimental_option("prefs", prefs)

    ua = 'Mozilla/5.0 ' \
         '(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    options.add_argument("user-agent={}".format(ua))

    chrome = webdriver.Chrome('./chromedriver.exe', options=options)

    chrome.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    # chrome.minimize_window()

    return chrome


def show_chrome():
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")  # 關閉自動測試提示
    # options.add_argument("--headless")  # 無視窗模式
    options.add_argument("--incognito")  # 無痕
    options.add_argument("--mute-audio")  # 靜音

    path = os.getcwd()+'\\videos'
    prefs = {"download.default_directory": path}
    options.add_experimental_option("prefs", prefs)

    ua = 'Mozilla/5.0 ' \
         '(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    options.add_argument("user-agent={}".format(ua))

    chrome = webdriver.Chrome('./chromedriver.exe', options=options)

    chrome.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    # chrome.minimize_window()

    return chrome


def searchbar(item, chrome):
    action = ActionChains(chrome)

    search = WebDriverWait(chrome, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div/form/input'))
    )
    action.move_to_element(search)
    action.click()
    action.send_keys(item)

    button = chrome.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div/form/button')
    action.move_to_element(button)
    action.click()
    action.perform()
