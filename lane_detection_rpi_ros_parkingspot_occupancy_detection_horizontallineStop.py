from picamera import PiCamera
from picamera.array import PiRGBArray
import math
import time
import rospy
import os, glob
from std_msgs.msg import Int32
import cv2
import numpy as np
#flag_hor=0
vis=0
def spin():
	global vis
	rospy.init_node("publisher")		
	pub = rospy.Publisher('flag1', Int32, queue_size = 10)
	pub1 = rospy.Publisher('flag_horizontal', Int32, queue_size = 10)
	rate = rospy.Rate(10)
	while not rospy.is_shutdown():
		camera=PiCamera()
		camera.brightness=60
		camera.contrast=60
		camera.awb_mode='auto'
		camera.exposure_mode='auto'
		camera.resolution=(640,480)
		camera.framerate=32
		rawCapture=PiRGBArray(camera,size=(640,480))
		time.sleep(0.1)
		
		for frame in camera.capture_continuous(rawCapture,format="bgr",use_video_port=True):
			flag=0
						
			image=frame.array
			hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
			lower=np.uint8([0,70,50])
			upper=np.uint8([10,255,255])
			mask=cv2.inRange(hsv,lower,upper)
			res = cv2.bitwise_and(image,image, mask= mask)
			gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
			median = cv2.medianBlur(gray,5)
			edges = cv2.Canny(median,50,150,apertureSize = 3)
			lines = cv2.HoughLines(edges,1,np.pi/180,50)
			#print(lines)	
	
			if(lines is None):
				flag_hor=0
				print("line",flag)
				pub.publish(flag)
				print("horizontal line",flag_hor)
				pub1.publish(flag_hor)
				rawCapture.truncate(0)
				continue
		
			for line in lines:
				flag=1
				print("line",flag)
				pub.publish(flag)
				
				for rho,theta in line:
					
					if(80<((theta*180)/math.pi)<110):
						
						vis=1						
						flag_hor=1
						print("horizontal line",flag_hor)
						pub1.publish(flag_hor)
					else:
						
						if(vis==0):
							flag_hor=0
							print("horizontal line",flag_hor)
							pub1.publish(flag_hor)		
						else:
							flag_hor=1
							print("horizontal line",flag_hor)
							pub1.publish(flag_hor)			
    					a = np.cos(theta)
    					b = np.sin(theta)
    					x0 = a*rho
    					y0 = b*rho
    					x1 = int(x0 + 1000*(-b))
    					y1 = int(y0 + 1000*(a))
    					x2 = int(x0 - 1000*(-b))
    					y2 = int(y0 - 1000*(a))
					cv2.line(image,(x1,y1),(x2,y2),(0,0,255),2)
	
			#cv2.imshow("frame",image)
			#cv2.waitKey(10)
			try:
				rawCapture.truncate(0)
			except PiCameraValueError:
				print('closed') 
	camera.close()
	
			
if __name__ == '__main__':
	
	try:
		spin()
	except rospy.ROSInterruptException:
		pass	
