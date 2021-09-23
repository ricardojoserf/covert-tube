# import the necessary packages
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import math
from glob import glob
import re
import config
from pyzbar.pyzbar import decode
natsort = lambda s: [int(t) if t.isdigit() else t.lower() for t in re.split('(\d+)', s)]


def get_frames(video_path, imagesFolder):
	cap = cv2.VideoCapture(video_path)
	frameRate = int(cap.get(cv2.CAP_PROP_FPS))
	while(cap.isOpened()):
		frameId = cap.get(1)
		ret, frame = cap.read()
		if (ret != True):
			break
		if (frameId % frameRate == 0):
			filename = imagesFolder + "/image_" +  str(int(frameId+1)) + ".png"
			cv2.imwrite(filename, frame)
	cap.release()


def read_frames(image_type, imagesFolder):
	commands = []
	for filename in sorted(glob(imagesFolder+'/*.png'), key=natsort):
		if image_type == "cleartext":
			image = cv2.imread(filename)
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			test_file = "/tmp/filename.png"
			cv2.imwrite(test_file, gray)
			text = pytesseract.image_to_string(Image.open(test_file))
			print("Command: %s"%text)
		elif image_type == "qr":
			text = decode(Image.open(filename))[0].data.decode()
			print("Command: %s"%text)
		elif image_type == "qr_red":
			image = cv2.imread(filename)
			r = image.copy()
			r[:, :, 0] = 0
			r[:, :, 1] = 0
		else:
			print("Unknown type")
		commands.append(text)
	return commands


def read_video(image_type, video_path, imagesFolder):
	get_frames(video_path, imagesFolder)
	commands = read_frames(image_type, imagesFolder)
	return commands


def main():
	read_video(config.image_type, config.video_path, "/tmp/")


if __name__== "__main__":
	main()
