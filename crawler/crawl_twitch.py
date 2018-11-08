# crawler_twitch.py
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

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory


from os import listdir
from os.path import isfile, join
files_dict = dict()
CLIENT_ID = 'urfntwbl92o0ojm7hee04t4tbfmavm'

class multi_crawler(threading.Thread):
	def __init__(self, **kwargs):

		threading.Thread.__init__(self)
		self.kwargs = kwargs['kwargs']

	def run(self):
		global total_html
		n = self.kwargs["n"]
		url = self.kwargs["url"] + str(n) + '&' + 'broadcaster_software=&' + 'on_site=1'
		request = urllib2.Request(url)
		request.add_header('Client-ID', CLIENT_ID)
		# print n
		if not n in total_html.keys():
			s = urllib2.urlopen(request).read()
			s = s.decode('utf-8')
			total_html[n] = s + '\n'




def return_total(html):
	flag = html.split(b'\"_total\":')[1]
	if flag:
		flag_2 = flag.split(b',\"streams\"')[0]
		if flag_2:
			return int(flag_2)

def return_html(start_num):
	twitch_url = 'https://api.twitch.tv/kraken/streams?limit=100&offset=' + str(start_num) + '&broadcaster_software=&on_site=1'
	twitch_request = urllib2.Request(twitch_url)
	twitch_request.add_header('Client-ID', CLIENT_ID)
	response = urllib2.urlopen(twitch_request)
	return response.read()

def save_total(platform):
	global total_html
	offset_num = 0
	increa_num = 100
	folder_path = PATH + '/'
	txt_name =  platform + '-' + date +'.txt'
	file_path = folder_path + txt_name
	zip_path = folder_path + platform + '-' + date +'.zip'
	fw = open(file_path, 'w')
	fw2 = open(PATH + '/streams.txt','a')
	try:
		html = return_html(offset_num)
		total = return_total(html)
		fw2.writelines(platform + '-' + date + ':' + str(total) + '\n')
		fw2.close()
		works = [multi_crawler(kwargs={"url": "https://api.twitch.tv/kraken/streams?limit=100&offset=", "n": i}) for i in range(0,total,100)]
		# print 'start'
		num_works = len(works) 
		start_works = 0
		while start_works <= num_works:
			for i in range(start_works, min(start_works + 50, num_works)):
			    works[i].start()
			# print 'join'
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
	

total_html = dict()
save_total("all")

