import random
import time
import requests
from pathlib import Path
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import file_process
import init


def gate(chrome):
    url = ['https://snaptik.app/en', 'https://snaptik.app/in',
           'https://snaptik.app/th', 'https://snaptik.app/ID', 'https://snaptik.app/cs']
    master = open('link/master.txt', 'r')
    links = master.read().splitlines()

    used_links = []
    error_links = []
    for link in links:
        chrome.get(url[random.randrange(5)])

        inputbar = WebDriverWait(chrome, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="url"]'))
        )
        button = WebDriverWait(chrome, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="submiturl"]'))
        )
        try:
            inputbar.send_keys(link)
            button.click()
            try:
                download = WebDriverWait(chrome, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="download-block"]/div/a[2]'))
                )
            except:
                print('載入影片檔逾時')

            href = download.get_attribute('href')
            chrome.get(href)

            file_process.rename()

            used_links.append(link)
        except Exception as e:
            print(e)
            error_links.append(link)

    with open('link/master.txt', 'w') as f:
        for link in error_links:
            f.write(link+'\n')

    with open('link/used.txt', 'r') as f:
        old_links = f.read().splitlines()

    used_links += old_links

    with open('link/used.txt', 'w') as f:
        for link in used_links:
            f.write(link+'\n')


if __name__ == '__main__':
    chrome = init.guise_chrome()
    gate(chrome)


