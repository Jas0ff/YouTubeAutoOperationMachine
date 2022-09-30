import time
import cv2
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

import pickle


def puzzle(chrome):
    background = WebDriverWait(chrome, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="captcha-verify-image"]'))
    )
    slice = chrome.find_element(By.XPATH, '//*[@id="tiktok-verify-ele"]/div/div[2]/img[2]')

    bg_src = background.get_attribute("src")
    sl_src = slice.get_attribute("src")

    bg = requests.get(bg_src)
    with open("temp\\" + 'bg.jpeg', 'wb') as file:
        file.write(bg.content)

    sl = requests.get(sl_src)
    with open("temp\\" + 'slice.png', 'wb') as file:
        file.write(sl.content)

    top_left = detect_displacement('temp/slice.png', 'temp/bg.jpeg', background.size)

    # 拖動滑塊
    slider = chrome.find_element(By.XPATH, '//*[@id="secsdk-captcha-drag-wrapper"]/div[2]')
    mimic_left_drag(slider, top_left, chrome)

    time.sleep(3)
    try:
        capcha = chrome.find_element(By.XPATH, '//*[@id="tiktok-verify-ele"]/div')
        print("fail anti-bot")
        puzzle(chrome)
    except:
        print('', end='')


def mimic_left_drag(slider, value, chrome):
    action = ActionChains(chrome)
    action.click_and_hold(slider)
    action.perform()
    seg_num = 5
    slice = value / seg_num
    for i in range(seg_num):
        action.move_by_offset(slice, 0).perform()
    action.click().perform()


def show(name):
    '''展示圈出来的位置'''
    cv2.imshow('Show', name)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def _tran_canny(image):
    """消除噪声"""
    image = cv2.GaussianBlur(image, (3, 3), 0)
    return cv2.Canny(image, 50, 150)


def detect_displacement(img_slider_path, image_background_path, orginal_size):
    """detect displacement"""
    # # 参数0是灰度模式
    image = cv2.imread(img_slider_path, 0)
    template = cv2.imread(image_background_path, 0)

    # 寻找最佳匹配
    res = cv2.matchTemplate(_tran_canny(image), _tran_canny(template), cv2.TM_CCOEFF_NORMED)
    # 最小值，最大值，并得到最小值, 最大值的索引
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc[0]  # 横坐标
    '''
    # 展示圈出来的区域
    x, y = max_loc  # 获取x,y位置坐标
    w, h = image.shape[::-1]  # 宽高
    cv2.rectangle(template, (x, y), (x + w, y + h), (7, 249, 151), 2)
    show(template)
    '''

    top_left *= float(orginal_size['height']) / float(template.shape[0])

    return top_left


def get_cookies(chrome):
    chrome.get('https://www.youtube.com/')
    print('手動登入中')
    time.sleep(40)
    print('登入結束')

    cookies = chrome.get_cookies()
    with open('google_temp_cookies', 'wb') as f:
        pickle.dump(cookies, f)


def get_existed_cookies(chrome):
    chrome.get('https://www.youtube.com/')
    chrome.delete_all_cookies()
    with open('google_temp_cookies', 'rb') as f:
        cookies = pickle.load(f)
    for cookie in cookies:
        chrome.add_cookie(cookie)
    chrome.get('https://www.youtube.com/')
