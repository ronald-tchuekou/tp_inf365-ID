import cv2
import numpy as np

def show_image(file_name):
	""" Function to read and show an image. """
	img = cv2.imread(file_name, 1) # Read the image.
	cv2.imshow('test of display image', img) # Show the image.
	cv2.waitKey(0) # Listen when press on the button.
	cv2.destroyAllWindows() # Destroy all the showing windows.

def show_video(file_name):
	""" Function to read video. """
	cap = cv2.VideoCapture(file_name) # Capture or read a video.
	while(cap.isOpened()):
		ret, img = cap.read() # Read the video.
		gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
		cv2.imshow('Video captuer', img)
		if (cv2.waitKey(1) == ord('q')):
			break
	cap.release()
	cv2.destroyAllWindows()

def detect_face_in_image (file_name):
	""" Function that detect face and eye in an image. """
	cascade_face = cv2.CascadeClassifier('./haarcascade_frontalface.xml')
	cascade_eye = cv2.CascadeClassifier('./haarcascade_eye.xml')
	while True:
		img = cv2.imread(file_name)
		gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
		face = cascade_face.detectMultiScale(gray_img, scaleFactor=1.2, minNeighbors=3)
		eye  = cascade_eye.detectMultiScale(gray_img, 1.4, 4)
		for x, y, w, h in face:
			cv2.rectangle(img, (x, y), (x+w, y+h), (200, 0, 0), 2)
		for x, y, w, h in eye:
			cv2.rectangle(img, (x, y), (x+w, y+h), (9, 200, 0), 2)
		cv2.imshow('Detect face in image', img)
		if(cv2.waitKey(1) == ord('q')):
			break
			
def detect_cars_in_image (file_name):
	""" Function that detect cars in an image. """
	cascade_car = cv2.CascadeClassifier('./cars.xml')
	while True:
		img = cv2.imread(file_name)
		gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
		face = cascade_car.detectMultiScale(gray_img, scaleFactor=1.2, minNeighbors=3)
		for x, y, w, h in face:
			cv2.rectangle(img, (x, y), (x+w, y+h), (200, 0, 0), 2)
		cv2.imshow('Detect cars in image', img)
		if(cv2.waitKey(1) == ord('q')):
			break

def detect_face (file_name):
	""" Function that detecte face in video. """
	cascade_face = cv2.CascadeClassifier('./haarcascade_frontalface.xml')
	cascade_eye = cv2.CascadeClassifier('./haarcascade_eye.xml')
	cap = cv2.VideoCapture(file_name)
	while (cap.isOpened()):
		ret, img = cap.read()
		if ret == True: # When the image is reading well.
			gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
			tickmark = cv2.getTickCount()
			face = cascade_face.detectMultiScale(gray_img, scaleFactor=1.2, minNeighbors=3)
			eye = cascade_eye.detectMultiScale(gray_img, scaleFactor=1.2, minNeighbors=3)
			for x, y, w, h in face:
				cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 200), 2)
			for x, y, w, h in eye:
				cv2.rectangle(img, (x, y), (x+w, y+h), (200, 0, 200), 2)
			fps = cv2.getTickFrequency() / (cv2.getTickCount() - tickmark)
			cv2.putText(img, "FPS: {:05.2f}".format(fps), (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 200, 0), 2)
			cv2.imshow('Detect face in video', img)
			if(cv2.waitKey(1) == ord('q')):
				break
		else:
			print('Error has provide.')
			break

	cap.release()
	cv2.destroyAllWindows()

def detect_cars (file_name):
	""" Function that detect cars in the video. """
	cascade_car = cv2.CascadeClassifier('./cars.xml')
	cap = cv2.VideoCapture(file_name)
	cv2.VideoCapture(-1)
	while (cap.isOpened()):
		ret, img = cap.read()
		if ret == True: # When the image is reading well.
			gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
			tickmark = cv2.getTickCount()
			car = cascade_car.detectMultiScale(gray_img, scaleFactor=1.15, minNeighbors=3)
			for x, y, w, h in car:
				cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 200), 2)
			fps = cv2.getTickFrequency() / (cv2.getTickCount() - tickmark)
			cv2.putText(img, "FPS: {:05.2f}".format(fps), (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 200, 0), 2)
			cv2.imshow('Detect face in video', img)
			if(cv2.waitKey(1) == ord('q')):
				break
		else:
			print('Error has provide.')
			break
	print('Operation about detection is finish.')
	cap.release()
	cv2.destroyAllWindows()

# call of the functions.
#detect_cars('./video1.mp4')
#detect_face_in_image('lena.png')
#detect_face_in_image('lena.png')

# Password : codyinovT14@
# email: codyinnovation7