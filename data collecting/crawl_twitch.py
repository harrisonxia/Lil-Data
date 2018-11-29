# crawler_twitch.py
# This following code was partly adpated from Mr. Cong Zhang (congz@sfu.ca)
#   from https://clivecast.github.io
# The following lines are the initial disclaimer/header from original snippet.
# (C) Copyright 2015, Cong Zhang (congz@sfu.ca)
# This is the multi-thread crawler for Twitch.
# It will collect current streams in Twitch.
# If you use this crawler in your research, please cite the following paper
# -----------------------------------------------------
# Cong Zhang and Jiangchuan Liu. On crowdsourced interactive live streaming: a Twitch.tv-based measurement study. In ACM NOSSDAV, 2015
# -----------------------------------------------------

import urllib.request as urllib2
import time
import datetime
import os
import inspect
import threading
import zipfile


from os import listdir
from os.path import isfile, join

# files_dict = dict()
CLIENT_ID = 'urfntwbl92o0ojm7hee04t4tbfmavm'
total_html = dict()

class multi_crawler(threading.Thread):
    def __init__(self, **kwargs):

        threading.Thread.__init__(self)
        self.kwargs = kwargs['kwargs']

    def run(self):
        global total_html
        n = self.kwargs["n"]
        url = self.kwargs["url"] + \
            str(n) + '&' + 'broadcaster_software=&' + 'on_site=1'
        request = urllib2.Request(url)
        request.add_header('Client-ID', CLIENT_ID)
        # print n
        if not n in total_html.keys():
            s = urllib2.urlopen(request).read()
            s = s.decode('utf-8')
            total_html[n] = s + '\n'

def format_time(time_str):
    return datetime.datetime.fromtimestamp( \
        time_str).strftime('%Y-%m-%d-%H-%M-%S')

def return_total(html):
    flag = html.split(b'\"_total\":')[1]
    if flag:
        flag_2 = flag.split(b',\"streams\"')[0]
        if flag_2:
            return int(flag_2)

def return_html(start_num):
    twitch_url = 'https://api.twitch.tv/kraken/streams?limit=100&offset=' +\
        str(start_num) + '&broadcaster_software=&on_site=1'
    twitch_request = urllib2.Request(twitch_url)
    twitch_request.add_header('Client-ID', CLIENT_ID)
    response = urllib2.urlopen(twitch_request)
    return response.read()

def save_total(date):
    # script directory
    PATH = os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe())),
        ) 

    offset_num = 0
    increa_num = 100
    folder_path = PATH + '/data/'
    txt_name =  date +'.txt'
    file_path = folder_path + txt_name
    zip_path = folder_path + date +'.zip'
    fw = open(file_path, 'w')
    fw2 = open(PATH + '/streams.txt','a')

    try:
        html = return_html(offset_num)
        total = return_total(html)
        fw2.writelines(date + ':' + str(total) + '\n')
        fw2.close()
        works = [
            multi_crawler(
                kwargs={
                "url": "https://api.twitch.tv/kraken/streams?limit=100&offset=",
                 "n": i,
                 },
                 ) for i in range(0,total,100)
            ]
        num_works = len(works) 
        start_works = 0
        while start_works <= num_works:
            for i in range(start_works, min(start_works + 50, num_works)):
                works[i].start()
            for i in range(start_works, min(start_works + 50, num_works)):
                works[i].join()
            start_works += 50
        for i in range(0,total,100):
            fw.writelines(total_html[i])
        fw.close()
        zf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
        zf.write(file_path, txt_name)
        zf.close()
        os.remove(file_path)
    except BaseException as e:
        error = str(e)
        print(error)
    
def main():
    timer = 30 * 60
    start_time = time.time()
    print(
        'Start first collecting at ',
        format_time(start_time),
        ' timer is set at ',
        timer,
    )
    while True:
        current_time = time.time()
        current_time_formated = format_time(current_time)
        total_html.clear()
        print(current_time_formated, ' - ', 'start collecting')
        save_total(current_time_formated)
        sleep_time = round(timer - ((current_time - start_time) % timer))
        print('Going to sleep for ', sleep_time)
        time.sleep(sleep_time)
        print('Wake')

if __name__ == '__main__': 
    main()
