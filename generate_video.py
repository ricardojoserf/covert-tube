from glob import glob
import config
import cv2
import re
import os


def aes_encrypt(message, aes_key):
	import base64
	from Crypto.Cipher import AES
	message = message.encode()
	BS = 16
	pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode()
	raw = pad(message)
	cipher = AES.new(aes_key, AES.MODE_CBC, chr(0) * 16) # yes, IV is all zeros xD
	enc = cipher.encrypt(raw)
	return base64.b64encode(enc).decode('utf-8')


def generate_frames(image_type):
	images_counter = 0
	while True:
		cmd_ = input("Enter a command or 'exit' to generate video: ")
		images_counter += 1
		if cmd_ != "exit":
			if image_type == "cleartext":
				from PIL import Image, ImageDraw, ImageFont
				img = Image.new('RGB', (200, 200), color=(255,255,255))
				canvas = ImageDraw.Draw(img)
				font = ImageFont.truetype('Lato-Bold.ttf', size=30)
				canvas.text((16, 16), cmd_, font=font, fill='#000000')
				img.save(config.temp_folder+"image_"+str(images_counter)+".png")
			elif image_type == "qr":
				import pyqrcode
				qrcode = pyqrcode.create(cmd_,version=10)
				qrcode.png(config.temp_folder+"image_"+str(images_counter)+".png",scale=8)
			elif image_type == "qr_aes":
				import pyqrcode
				encrypted_cmd = aes_encrypt(cmd_,config.aes_key)
				qrcode = pyqrcode.create(encrypted_cmd,version=10)
				qrcode.png(config.temp_folder+"image_"+str(images_counter)+".png",scale=8)			
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