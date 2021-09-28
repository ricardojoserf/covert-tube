from pyzbar.pyzbar import decode
from PIL import Image
from glob import glob
import pytesseract
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
			cv2.imwrite(filename, frame)
	cap.release()
	return images_counter


def read_frames(image_type, imagesFolder):
	natsort = lambda s: [int(t) if t.isdigit() else t.lower() for t in re.split('(\d+)', s)]
	commands = []
	for filename in sorted(glob(imagesFolder+'/*.png'), key=natsort):
		if image_type == "cleartext":
			image = cv2.imread(filename)
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			test_file = "/tmp/filename.png"
			cv2.imwrite(test_file, gray)
			text = pytesseract.image_to_string(Image.open(test_file))
		elif image_type == "qr":
			text = decode(Image.open(filename))[0].data.decode()
		else:
			print("[-] Error: Unknown type")
			return "unknown_type"
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