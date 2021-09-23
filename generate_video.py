from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from glob import glob
import re
import pyqrcode
import config
natsort = lambda s: [int(t) if t.isdigit() else t.lower() for t in re.split('(\d+)', s)]



def generate_frames(image_type):
	counter = 0
	while True:
		cmd_ = input("Enter command for the image or 'exit' to start generating the video: ")
		counter += 1
		if cmd_ != "exit":
			if image_type == "cleartext":
				img = Image.new('RGB', (200, 200), color=(255,255,255))
				canvas = ImageDraw.Draw(img)
				font = ImageFont.truetype('Lato-Bold.ttf', size=30)
				canvas.text((16, 16), cmd_, font=font, fill='#000000')
				img.save("image_"+str(counter)+".png")
			elif image_type == "qr":
				qrcode = pyqrcode.create(cmd_)
				qrcode.png("image_"+str(counter)+".png",scale=8)
			else:
				print("Unknown type")
		else:
			break


def create_file(video_file, fps):
	img_array = []
	for filename in sorted(glob('*.png'), key=natsort):
		img = cv2.imread(filename)
		height, width, layers = img.shape
		size = (width,height)
		img_array.append(img)
		out = cv2.VideoWriter(video_file,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
	for i in range(len(img_array)):
		out.write(img_array[i])
	out.release()


def generate_video(image_type, video_file, fps):
	generate_frames(image_type)
	create_file(video_file, fps)


def main():
	generate_video(config.image_type, "output.avi", 1)


if __name__== "__main__":
	main()