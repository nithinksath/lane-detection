

import cv2

import numpy as np

import math
scale = 1
delta = 0
ddepth = cv2.CV_16S
minLineLength = 100
maxLineGap = 10
width_of_lane_mm=750
threshold=100
def hough_lines_acc(img, rho_resolution=1, theta_resolution=1):

    height, width = img.shape
    img_diagonal = np.ceil(np.sqrt(height**2 + width**2)) 
    rhos = np.arange(-img_diagonal, img_diagonal + 1, rho_resolution)
    thetas = np.deg2rad(np.arange(-90, 90, theta_resolution))

    
    H = np.zeros((len(rhos), len(thetas)), dtype=np.uint64)
    y_idxs, x_idxs = np.nonzero(img) 
    for i in range(len(x_idxs)): 
        x = x_idxs[i]
        y = y_idxs[i]

        for j in range(len(thetas)):
            rho = int((x * np.cos(thetas[j]) +
                       y * np.sin(thetas[j])) + img_diagonal)
            H[rho, j] += 1	
    count=0
    h=np.ravel(H)
    for i in range(len(rhos)*len(thetas)):
        if(h[i]>threshold and h[i-1]<h[i] and h[i+1]<h[i] and h[i-2]<h[i] and h[i+2]<h[i] and h[i-3]<h[i] and h[i+3]<h[i]):
	    count=count+1		
    return H, rhos, thetas,count

def hough_peaks(H, num_peaks=2, threshold=0, nhood_size=3):

    indicies = []
    H1 = np.copy(H)
    for i in range(num_peaks):
        idx = np.argmax(H1) # find argmax in flattened array
        H1_idx = np.unravel_index(idx, H1.shape) # remap to shape of H
        indicies.append(H1_idx)
	#print(indicies)


       
        idx_y, idx_x = H1_idx 
        
        if (idx_x - (nhood_size/2)) < 0: min_x = 0
        else: min_x = idx_x - (nhood_size/2)
        if ((idx_x + (nhood_size/2) + 1) > H.shape[1]): max_x = H.shape[1]
        else: max_x = idx_x + (nhood_size/2) + 1

       
        if (idx_y - (nhood_size/2)) < 0: min_y = 0
        else: min_y = idx_y - (nhood_size/2)
        if ((idx_y + (nhood_size/2) + 1) > H.shape[0]): max_y = H.shape[0]
        else: max_y = idx_y + (nhood_size/2) + 1

       
        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
               
                H1[y, x] = 0

               
                if (x == min_x or x == (max_x - 1)):
                    H[y, x] = 255
                if (y == min_y or y == (max_y - 1)):
                    H[y, x] = 255

    
    return indicies, H


def hough_lines_draw(img, indicies, rhos, thetas):
    
    p1=[]
    p2=[]
    count=0
    for i in range(len(indicies)):
        # reverse engineer lines from rhos and thetas
        rho = rhos[indicies[i][0]]
        theta = thetas[indicies[i][1]]
	a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        # these are then scaled so that the lines go off the edges of the image
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
	denom=x2-x1
	if (denom!=0):
		m=(y2-y1)/denom
		m1=math.degrees(math.atan(m))
		if(m1==-45):
			print 'HORIZONTAL LINE' 
		

        count=count+1	
	p1.append(x1)
	p2.append(x2)
	cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
	cv2.imshow('frame',img)
	
	if(count==len(indicies)):
		distance=((max(p1)+max(p2))/2)-((min(p1)+min(p2))/2)
		#print("width of lane in pixels:",distance)
		print('The width of lane in pixels {0:.1f}.'.format(distance))
		if(distance==0):
			print 'YOU HAVE PARKED SUCESSFULLY'
		else:		
			return(distance)
		
	else:
		continue

	
	#end=time.time()
	#print(end-start)

def obstacle_detection(frame):
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		#cv2.imshow('frame',hsv)
		lower=np.uint8([25,50,50])
		upper=np.uint8([32,255,255])
		mask=cv2.inRange(hsv,lower,upper)
		#cv2.imshow('frame',mask)	
		res = cv2.bitwise_and(frame,frame, mask= mask)
		#cv2.imshow('frame',res)
		gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
		gaussian = cv2.GaussianBlur(gray,(5, 5), 1.5)
		edges = cv2.Canny(gaussian,50,150,apertureSize = 3)
		#cv2.imshow('frame',edges)
		(_, cnts, _) = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) 	
		c = max(cnts, key = cv2.contourArea)
		#x,y,w,h = cv2.boundingRect(c)
    		#cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
		area = cv2.contourArea(c)
		if(area>1000):		
			rect=cv2.minAreaRect(c)
			(_,(width,_),_)=rect
			
			box = cv2.boxPoints(rect)
    			box = np.int0(box)
	
		
    			cv2.drawContours(frame,[box],0,(0,0,255),2)
			return(width)
	
cap=cv2.VideoCapture(0)
while(cap.isOpened()):
	ret, frame = cap.read()
	while ret:
		ret,frame=cap.read()
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		#cv2.imshow('frame',hsv)
		lower=np.uint8([0,70,50])
		upper=np.uint8([10,255,255])
		mask=cv2.inRange(hsv,lower,upper)
		#cv2.imshow('frame',mask)	
		res = cv2.bitwise_and(frame,frame, mask= mask)
		#cv2.imshow('frame',res)
		gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
		gaussian = cv2.GaussianBlur(gray,(5, 5), 1.5)
		edges = cv2.Canny(gaussian,50,150,apertureSize = 3)
		#cv2.imshow('frame',edges)
		#start=time.time()
		H,rhos,thetas,ab = hough_lines_acc(edges)
		#print(ab)
		a=np.amax(H)
		#print(a)
		if(ab==0):
			indicies,H=hough_peaks(H,2,0,nhood_size=11)
		else:
			indicies,H = hough_peaks(H,ab,0,nhood_size=11)

		distance1=hough_lines_draw(frame, indicies, rhos, thetas)
		#print(rhos,thetas)
		mtx=np.loadtxt('cameramatrix.txt')
		#print(mtx)
		fx=mtx[0][0]
		fy=mtx[1][1]
		cx=mtx[0][2]
		cy=mtx[1][2]
		f=np.loadtxt('focallength.txt')
		m=np.int_(fx/f)
	
		width_lane_pixels=373
		
		distance_of_camera_lane=np.int_((f*width_of_lane_mm*1280)/(width_lane_pixels*109))
		
		if cv2.waitKey(10) == 27:                     # exit if Escape is hit
        		break	
cap.release()
out.release()
cv2.destroyAllWindows


