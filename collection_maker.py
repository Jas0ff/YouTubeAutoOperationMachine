from os import listdir
from pathlib import Path
from moviepy.editor import *

import flag_maker


def main():
    configls = []
    with open('config.txt', 'r') as f:
        configls = f.read().splitlines()

    goal_min = int(configls[2])
    goal_max = int(configls[2])+100

    videos = listdir('videos')
    # get duration list
    times = get_duration(videos)

    collect_index = selected_proper_v(times, goal_min, goal_max)
    if collect_index[0] == -1:
        return 'out of source'

    selected_files = get_filename(times, collect_index)

    file_merge(selected_files)

    return 'completed'


def file_merge(files_path):
    clips = [VideoFileClip(c) for c in files_path]
    final = concatenate_videoclips(clips, method="compose")

    num = ''
    with open('video num.txt', 'r') as f:
        num = f.read()

    configls = []
    with open('config.txt', 'r') as f:
        configls = f.read().splitlines()

    final.write_videofile('result/'+str(configls[1])+' # '+str(num)+'.mp4')


def selected_proper_v(times, goal_min, goal_max):
    collect_index = []
    index = 0
    total = 0
    while total < goal_min:
        if index == len(times):
            flag_maker.show("doesn't have enough videos")
            return [-1]

        total += times[index]

        if total > goal_max:
            total -= times[index]
        else:
            collect_index.append(index)

        index += 1

    return collect_index


def get_duration(vs):
    temp = []
    for v in vs:
        bread_index = v.find('_')
        temp.append(int(v[:bread_index]))
    temp.sort(reverse=True)

    return temp


def get_filename(times, indexs):
    result = []
    for i in indexs:
        file_num = 0
        while not Path('videos/'+str(times[i])+'_'+str(file_num)+'.mp4').is_file():
            file_num += 1
        name = str(times[i])+'_'+str(file_num)+'.mp4'
        Path('videos/'+name).rename('result/'+name)

        result.append('result/'+name)

    return result
