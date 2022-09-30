import time
from pathlib import Path
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import anti
import init


def upload(chrome):
    try:
        anti.get_existed_cookies(chrome)

    except:
        windowchrome = init.show_chrome()
        anti.get_cookies(windowchrome)
        time.sleep(5)
        anti.get_existed_cookies(chrome)

    chrome.get('https://www.youtube.com/upload')

    file = WebDriverWait(chrome, 15).until(
        EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
    )

    with open('video num.txt', 'r') as f:
        num = int(f.read())

    uploading_process(num, chrome, file)

    with open('video num.txt', 'w') as f:
        f.write(str(num+1))


def uploading_process(num, chrome, file):
    configls = []
    with open('config.txt', 'r') as f:
        configls = f.read().splitlines()

    file.send_keys(str(Path.cwd())+'/result/'+str(configls[1])+' # '+str(num)+'.mp4')

    next = WebDriverWait(chrome, 100).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="next-button"]/div'))
    )
    for i in range(3):
        time.sleep(5)
        next.click()

    '''
    to_public_option = WebDriverWait(chrome, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="privacy-radios"]/tp-yt-paper-radio-button[3]'))
    )

    time.sleep(5)
    if to_public_option.is_displayed():
        to_public_option.click()
    '''

    publish = WebDriverWait(chrome, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="done-button"]'))
    )
    '''
    process = chrome.find_element(By.XPATH,
                                  '//*[@id="dialog"]/div/ytcp-animatable[2]/div/div[1]/ytcp-videos-upload-progress/span')
    while '檢查' not in process.text:
        continue
    '''
    try:
        time.sleep(60)
        publish.click()
    except:
        time.sleep(60)
        publish.click()

    time.sleep(10)


if __name__ == '__main__':
    chrome = init.show_chrome()
    upload(chrome)
