import shutil
import time
import os.path
import glob

import collection_maker
import file_process
import init
import anti
import snaptik
import video
import youtube
import SMS
import flag_maker


# build a collection
def collect(page, chrome):
    # recommend hanging VPN to Europe country
    flag_maker.show("start collect videos' url")
    url = "https://www.tiktok.com/?lang=zh-Hant-TW"
    chrome.get(url)

    time.sleep(1)
    with open('config.txt', 'r') as f:
        configls = f.read().splitlines()

    searchItem = str(configls[0])
    init.searchbar(searchItem, chrome)

    time.sleep(4)
    anti.puzzle(chrome)

    file = open('./link/new.txt', 'w')
    video.collect(chrome, file, page)
    file.close()

    # sorting links
    file_process.add_new_to_master()

    # download videos(watermark removed)
    flag_maker.show("start download videos")
    chrome = init.guise_chrome()
    snaptik.gate(chrome)
    list_of_files = glob.glob(os.getcwd()+'/videos/*.crdownload')
    for file in list_of_files:
        os.remove(file)



try:
    chrome = init.guise_chrome()
    load_page = 10

    while True:
        flag_maker.show("start making compilation")
        if collection_maker.main() == 'out of source':
            flag_maker.show("out of video source")
            collect(load_page, chrome)
            load_page += 10
            chrome = init.guise_chrome()
        else:
            break

    # auto uploader
    flag_maker.show("start uploading to YouTube")
    youtube.upload(chrome)
    chrome.close()

    flag_maker.show("removing used videos compilation")
    shutil.rmtree('result', ignore_errors=True)
    if not os.path.isdir('result'):
        os.mkdir('result')

except Exception as e:
    print(e)
    chrome.close()
    SMS.send('auto operate machine has some error')
    os.system('pause')


