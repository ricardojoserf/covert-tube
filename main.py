from __future__ import unicode_literals
import sys
sys.path.append("./dependencies")
import read_funcs
import youtube_dl
import datetime
import urllib
import config
import json
import time
import os


def get_first_video_in_channel(api_key, channel_id):
	base_video_url = 'https://www.youtube.com/watch?v='
	base_search_url = 'https://www.googleapis.com/youtube/v3/search?'
	url = base_search_url + "part=snippet&channelId={}&maxResults=1&order=date&type=video&key={}".format(channel_id,api_key)
	inp = urllib.request.urlopen(url)
	resp = json.load(inp)
	if (resp['items'] != []):
		title = resp['items'][0]['snippet']['title']
		video_id = resp['items'][0]['id']['videoId']
		video_url = base_video_url + video_id
		now = datetime.datetime.now()
		print("[%02d:%02d] Last video title: %s" % (now.hour,now.minute,title))
		print("[%02d:%02d] Last video url:   %s" % (now.hour,now.minute,video_url))
		return video_url
	else:
		print("[%02d:%02d] No videos uploaded yet" % (now.hour,now.minute))
		return ""


def download_video(video_url, downloaded_video_path):
	now = datetime.datetime.now()
	print("[%02d:%02d] Downloading video file to: %s"%(now.hour,now.minute,downloaded_video_path))
	ydl_opts = {'outtmpl': downloaded_video_path}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([video_url])
	'''
	os.system("wget "+video_url+" -O "+downloaded_video_path)
	'''


def analyze(downloaded_video_path):
	now = datetime.datetime.now()
	print("[%02d:%02d] Analyzing video in: %s"%(now.hour,now.minute,downloaded_video_path))
	commands = read_funcs.read_video(config.image_type, downloaded_video_path, "/tmp/")
	return commands


def execute_commands(commands):
	for cmd_ in commands:
		os.system(cmd_)


def wait_for_upload(original_video_url, api_key, channel_id, delay_seconds, downloaded_video_path):
	now = datetime.datetime.now()
	print("[%02d:%02d] Waiting %s seconds..."%(now.hour,now.minute,delay_seconds))
	while True:
		time.sleep(delay_seconds)
		video_url = get_first_video_in_channel(api_key, channel_id)
		if video_url != original_video_url:
			now = datetime.datetime.now()
			print("[%02d:%02d] New video uploaded!"% (now.hour,now.minute))
			download_video(video_url, downloaded_video_path)
			time.sleep(5)
			commands = analyze(downloaded_video_path)
			execute_commands(commands)
			original_video_url = video_url
		else:
			now = datetime.datetime.now()
			print("[%02d:%02d] No new video uploaded. Waiting %s seconds..."%(now.hour,now.minute,delay_seconds))


def main():
	delay_seconds = config.upload_seconds_delay
	downloaded_video_path = config.downloaded_video_path
	channel_id = config.channel_id
	api_key = config.api_key
	original_video_url = get_first_video_in_channel(api_key, channel_id)
	wait_for_upload(original_video_url, api_key, channel_id, delay_seconds, downloaded_video_path)


main()