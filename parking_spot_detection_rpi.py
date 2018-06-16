from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import cv2
import numpy as np
import math
camera=PiCamera()
#camera.brightness=60
#camera.contrast=60
#camera.awb_mode='auto'
#camera.exposure_mode='auto'
camera.resolution=(640,480)#1280,720
camera.framerate=30
camera.rotation=270
rawCapture=PiRGBArray(camera,size=(640,480))
time.sleep(0.1)
slope=90
for frame in camera.capture_continuous(rawCapture,format="bgr",use_video_port=True):
	#flag=0
	image=frame.array
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	cv2.imshow('sdfsdf',hsv)
	lower=np.uint8([1,38,50])
	upper=np.uint8([51,88,180])
	mask=cv2.inRange(hsv,lower,upper)
	res = cv2.bitwise_and(image,image, mask= mask)
	average=cv2.mean(res)
	flag=sum(average)/len(average)
	print(flag)	
	
	#if(lines is None):
		#print(flag)
		#rawCapture.truncate(0)
		#continue
		
	#for line in lines:
		#flag=1
		#print(flag)
		#for rho,theta in line:
			#print((theta*180)/math.pi)
    			#a = np.cos(theta)
    			#b = np.sin(theta)
    			#x0 = a*rho
    			#y0 = b*rho
    			#x1 = int(x0 + 1000*(-b))
    			#y1 = int(y0 + 1000*(a))
    			#x2 = int(x0 - 1000*(-b))
    			#y2 = int(y0 - 1000*(a))
			#cv2.line(image,(x1,y1),(x2,y2),(0,0,255),2)
	cv2.imshow("frame1",image)		
	cv2.imshow("frame",mask)
	cv2.waitKey(3)
	try:
		rawCapture.truncate(0)
	except PiCameraValueError:
		print('closed') 
camera.close()
	
