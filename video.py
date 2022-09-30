import time
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


def collect(chrome, file, load_page):
    action = ActionChains(chrome)

    chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    # 載入10頁
    for i in range(load_page):
        chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        try:
            load_more = WebDriverWait(chrome, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[2]/div[2]/button'))
            )
            load_more.click()
            time.sleep(0.5)
        except:
            print('tiktok load stage: no more contents')
            break

    # 回頂端
    top_buttom = chrome.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[3]/button')
    top_buttom.click()
    chrome.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)
    time.sleep(2)

    # 點開影片reel
    flag = True
    while flag:
        try:
            head_video = WebDriverWait(chrome, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//*[@id="app"]/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[1]/div/div/a/div/div[1]/img')
                )
            )
            flag = False
            time.sleep(0.3)
        except:
            flag = True

    time.sleep(0.3)
    head_video.click()
    time.sleep(1)

    while True:
        action.send_keys(Keys.DOWN).perform()
        likes = WebDriverWait(chrome, 5).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '//*[@id="app"]/div[2]/div[2]/div[2]/div[3]/div[2]/div[2]/div[2]/div[1]/div[1]/button[1]/strong')
            )
        )
        if likes.text[-1] == 'M':
            link = chrome.find_element(By.XPATH,
                                       '//*[@id="app"]/div[2]/div[2]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/p')
            bread_index = link.text.find('?')
            file.write(link.text[:bread_index]+'\n')

        down_arrow = WebDriverWait(chrome, 5).until(
            EC.presence_of_element_located((By.XPATH,
                                            '//*[@id="app"]/div[2]/div[2]/div[2]/div[3]/div[1]/button[3]'))
        )
        if not down_arrow.is_enabled():
            break

    print('end of collect')
    chrome.close()

