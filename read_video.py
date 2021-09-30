from PIL import Image
from glob import glob
import config
import cv2
import re
import os


def get_frames(video_path, imagesFolder):
	cap = cv2.VideoCapture(video_path)
	frameRate = int(cap.get(cv2.CAP_PROP_FPS))
	images_counter = 0
	while(cap.isOpened()):
		frameId = cap.get(1)
		ret, frame = cap.read()
		if (ret != True):
			break
		if (frameId % frameRate == 0):
			images_counter += 1
			filename = imagesFolder + "/image_" +  str(int(images_counter)) + ".png"
			height, width, layers = frame.shape
			size = (width,height)
			cv2.imwrite(filename, frame)
	cap.release()
	return images_counter


def read_frames(image_type, imagesFolder):
	natsort = lambda s: [int(t) if t.isdigit() else t.lower() for t in re.split('(\d+)', s)]
	commands = []
	for filename in sorted(glob(imagesFolder+'/*.png'), key=natsort):
		if image_type == "cleartext":
			import pytesseract
			image = cv2.imread(filename)
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			text = pytesseract.image_to_string(gray)
		elif image_type == "qr":
			from pyzbar.pyzbar import decode
			text = decode(Image.open(filename))[0].data.decode()
		'''
		elif image_type == "stego":
			image = cv2.imread(filename)
			binary_data = ""
			for row in image:
				for pixel in row:
					r, g, b = [ format(i, "08b") for i in pixel ]
					binary_data += r[-1]
					binary_data += g[-1]
					binary_data += b[-1]
			all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
			decoded_data = ""
			for byte in all_bytes:
				decoded_data += chr(int(byte, 2))
				if decoded_data[-5:] == "=====":
					break
			text = decoded_data[:-5]
		'''
		else:
			print("[-] Error: Unknown type")
			return "unknown_type"
		print(text)
		commands.append(text)
	return commands


def clean_images(images_counter, imagesFolder):
	for i in range(1, images_counter+1):
		os.remove(imagesFolder + "/image_" +  str(int(i)) + ".png")


def read_vid(image_type, video_path, imagesFolder):
	images_counter = get_frames(video_path, imagesFolder)
	commands = read_frames(image_type, imagesFolder)
	clean_images(images_counter, imagesFolder)
	return commands


def main():
	read_vid(config.image_type, config.generated_video_path, config.temp_folder)


if __name__== "__main__":
	main()