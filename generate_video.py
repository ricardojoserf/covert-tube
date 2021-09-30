from PIL import Image, ImageDraw, ImageFont
from glob import glob
import pyqrcode
import config
import numpy
import cv2
import re
import os


def generate_frames(image_type):
	images_counter = 0
	while True:
		cmd_ = input("Enter a command or 'exit' to generate video: ")
		images_counter += 1
		if cmd_ != "exit":
			if image_type == "cleartext":
				img = Image.new('RGB', (200, 200), color=(255,255,255))
				canvas = ImageDraw.Draw(img)
				font = ImageFont.truetype('Lato-Bold.ttf', size=30)
				canvas.text((16, 16), cmd_, font=font, fill='#000000')
				img.save(config.temp_folder+"image_"+str(images_counter)+".png")
			elif image_type == "qr":
				qrcode = pyqrcode.create(cmd_,version=10)
				qrcode.png(config.temp_folder+"image_"+str(images_counter)+".png",scale=8)
			'''
			elif image_type == "stego":
				img = numpy.zeros((16,16,3), numpy.uint8)
				cmd_ += "====="
				data_index = 0
				binary_secret_data = ''.join([ format(ord(i), "08b") for i in cmd_ ])
				data_len = len(binary_secret_data)
				for row in img:
					for pixel in row:
						r, g, b = [ format(i, "08b") for i in pixel ]
						if data_index < data_len:
							pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
							data_index += 1
						if data_index < data_len:
							pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
							data_index += 1
						if data_index < data_len:
							pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
							data_index += 1
						if data_index >= data_len:
							break
				cv2.imwrite(config.temp_folder+"image_"+str(images_counter)+".png", img)
			'''
			else:
				print("Unknown type")
		else:
			return images_counter
			break


def create_file(video_file):
	img_array = []
	natsort = lambda s: [int(t) if t.isdigit() else t.lower() for t in re.split('(\d+)', s)]
	for filename in sorted(glob(config.temp_folder+'*.png'), key=natsort):
		img = cv2.imread(filename)
		height, width, layers = img.shape
		size = (width,height)
		img_array.append(img)
		fps = 1
		out = cv2.VideoWriter(video_file,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
	for i in range(len(img_array)):
		out.write(img_array[i])
	out.release()


def clean_images(images_counter, imagesFolder):
	for i in range(1, images_counter):
		os.remove(imagesFolder + "/image_" +  str(int(i)) + ".png")


def generate_video(image_type, video_file, imagesFolder):
	images_counter = generate_frames(image_type)
	create_file(video_file)
	clean_images(images_counter, imagesFolder)


def main():
	generate_video(config.image_type, config.generated_video_path, config.temp_folder)


if __name__== "__main__":
	main()