from __future__ import unicode_literals
import urllib
import json
import time
import youtube_dl
import os
import cv2, math
import config
import read_funcs


delay_seconds = 3
video_path = "/tmp/test.mp4" #+video_url.split("=")[1] #+".mp4"


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
		print("[-] Last video title: " + title)
		print("[-] Last video url: " + video_url)
		return video_url
	else:
		print("[-] No videos uploaded yet")
		return ""


def download_video(video_url, video_path):
	print("[+] Downloading video file to: "+video_path)
	ydl_opts = {'outtmpl': video_path}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([video_url])


def analyze(video_path):
	print ("[+] Analyzing video in: "+video_path)
	commands = read_funcs.read_video(config.image_type, video_path, "/tmp/")
	return commands


def execute_commands(commands):
	print(commands)
	for cmd_ in commands:
		os.system(cmd_)


def wait_for_upload(original_video_url, api_key, channel_id):
	while True:
		time.sleep(delay_seconds)
		video_url = get_first_video_in_channel(api_key, channel_id)
		if video_url == original_video_url:
		#if video_url != original_video_url:
			print("[+] New video uploaded!")
			download_video(video_url, video_path)
			time.sleep(5)
			commands = analyze(video_path)
			execute_commands(commands)
			original_video_url = video_url
			break
		else:
			print("[+] No new video uploaded. Waiting "+str(delay_seconds)+" seconds...")


def main():
	channel_id = config.channel_id
	api_key = config.api_key
	original_video_url = get_first_video_in_channel(api_key, channel_id)
	wait_for_upload(original_video_url, api_key, channel_id)
	

main()