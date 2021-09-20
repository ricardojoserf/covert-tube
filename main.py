from __future__ import unicode_literals
import urllib
import json
import time
import youtube_dl
import os
import cv2, math


def get_first_video_in_channel(api_key, channel_id):
	base_video_url = 'https://www.youtube.com/watch?v='
	base_search_url = 'https://www.googleapis.com/youtube/v3/search?'
	url = base_search_url + "part=snippet&channelId={}&maxResults=1&order=date&type=video&key={}".format(channel_id,api_key)

	video_links = []
	video_titles = []

	inp = urllib.request.urlopen(url)
	resp = json.load(inp)

	if (resp['items'] != []):
		title = resp['items'][0]['snippet']['title']
		video_id = resp['items'][0]['id']['videoId']
		video_url = base_video_url + video_id
		print(title)
		print(video_url)
		return video_url
	else:
		return "no_videos_yet"


def download_video(video_url, video_path):
	print(video_path)
	ydl_opts = {'outtmpl': video_path}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([video_url])


def analyze(video_path):
	print(video_path)
	
	imagesFolder = "/tmp/"
	cap = cv2.VideoCapture(video_path)
	frameRate = cap.get(5000) #frame rate
	while(cap.isOpened()):
	    frameId = cap.get(1) #current frame number
	    ret, frame = cap.read()
	    if (ret != True):
	        break
	    if (frameId % math.floor(frameRate) == 0):
	        filename = imagesFolder + "/image_" +  str(int(frameId)) + ".jpg"
	        cv2.imwrite(filename, frame)
	cap.release()
	'''
	vidcap = cv2.VideoCapture(video_path)
	count = 0
	success = True
	fps = int(vidcap.get(cv2.CAP_PROP_FPS))

	while success:
	    success,image = vidcap.read()
	    #print('read a new frame:',success)
	    if count%(20*fps) == 0 :
	         cv2.imwrite('frame%d.jpg'%count,image)
	         print('successfully written 10th frame')
	    count+=1
	'''

	print ("Done!")


def wait_for_upload(original_video_url):
	video_path = "/tmp/"+original_video_url.split("=")[1]+".mp4"
	download_video(original_video_url, video_path)
	analyze(video_path)
	'''
	while True:
		time.sleep(5000)
		video_url = get_first_video_in_channel(api_key, channel_id)
		if video_url != original_video_url:
			video_path = "/tmp/"+video_url.split("=")[1]+".mp4"
			download_video(video_url, video_path)
			analyze(video_path)
	'''


def main():
	# channel_id = "UCO0Bb2UjlIM6tJpdVSPl_Bw"
	channel_id = "UCop-oxKVfX6ErQIct2FRKhg"
	api_key =  #""
	original_video_url = get_first_video_in_channel(api_key, channel_id)
	print("original_video_url: {}".format(original_video_url))
	wait_for_upload(original_video_url)
	

main()
