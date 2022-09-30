import glob
import time
from os import listdir
from os.path import join
from pathlib import Path
import cv2
import os


def add_new_to_master():
    with open('./link/new.txt', 'r') as new:
        new_link = new.read().splitlines()
    with open('./link/master.txt', 'r') as master:
        master_link = master.read().splitlines()
    with open('./link/used.txt', 'r') as used:
        used_link = used.read().splitlines()
    with open('./link/deleted.txt', 'r') as deleted:
        deleted_link = deleted.read().splitlines()

    new_num = 0
    for link in new_link:
        if link not in master_link and link not in used_link and link not in deleted_link:
            master_link.append(link)
            new_num += 1

    with open('./link/master.txt', 'w') as master:
        for link in master_link:
            master.write(link+'\n')

    print('append:', new_num, 'links')


def rename():
    # waiting for download completed
    while len(glob.glob(os.getcwd()+'/videos/*.tmp')) > 0 or len(glob.glob(os.getcwd()+'/videos/*.crdownload')) > 0:
        continue

    list_of_files = glob.glob(os.getcwd()+'/videos/*.mp4')
    file = max(list_of_files, key=os.path.getmtime)

    sec = get_video_sec(file)
    i = 0
    try:
        while os.path.isfile(Path('videos/'+str(sec)+'_'+str(i)+'.mp4')):
            i += 1
        Path(file).rename('videos/'+str(sec)+'_'+str(i)+'.mp4')
    except:
        print('unknown error occurs(filename exists), skipped')


def video_dir():
    download_path = 'C:/Users/Jason/Downloads'
    files = listdir(download_path)
    for f in files:
        if f[:7] != 'Snaptik':
            continue
        fullpath = join(download_path, f)
        Path(fullpath).rename(str(Path.cwd())+'\\videos\\'+f)


def get_video_sec(video):
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = round(frame_count/fps)

    return duration
