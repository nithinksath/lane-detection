import cv2
import numpy as np
cap=cv2.VideoCapture(0)
while(cap.isOpened()):
        ret,frame=cap.read()
        while(ret):
                ret,frame=cap.read()
                #hsv1 = cv2.cvtColor(frame, cv2.COLOR_BGR2BGR565)
                #hsv2 = cv2.cvtColor(frame, cv2.COLOR_BGR2BGR555)
                #hsv3 = cv2.cvtColor(frame, cv2.COLOR_BGR2XYZ)
                #hsv4 = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
                hsv5 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                lower1=np.uint8([0,70,50])
		upper1=np.uint8([10,255,255])
		mask1=cv2.inRange(hsv5,lower1,upper1)
                
                lower2=np.uint8([11,48,100])
                upper2=np.uint8([31,68,180])
                mask2=cv2.inRange(hsv5,lower2,upper2)
                mask=cv2.bitwise_or(mask1,mask2)
                res = cv2.bitwise_and(frame,frame, mask= mask)
                average=cv2.mean(res)#gives mean of each channel
                avg_allchannel=sum(average)/len(average)#mean of mean of each channel
                if(avg_allchannel>10):
                        count=0
                        var1=[]
                        var2=[]
                        print("this is not occupied region")
                        gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
		        gaussian = cv2.GaussianBlur(gray,(5, 5), 1.5)
		        edges = cv2.Canny(gaussian,50,150,apertureSize = 3)
                        lines = cv2.HoughLines(edges,1,np.pi/180,140)
                        print(lines)
                        print(len(lines))
                        for line in lines:
                                for rho,theta in line:
                                        a = np.cos(theta)
                                        b = np.sin(theta)
                                        x0 = a*rho
                                        y0 = b*rho
                                        x1 = int(x0 + 1000*(-b))
                                        y1 = int(y0 + 1000*(a))
                                        x2 = int(x0 - 1000*(-b))
                                        y2 = int(y0 - 1000*(a))

                                        cv2.line(frame,(x1,y1),(x2,y2),(0,0,255),2)       
                                        var1.append(x1) 
                                        var2.append(x2)
                                        count=count+1
                                        if(count==len(lines)):
                                                print("list 1",var1)
                                                print("list 2",var2)
                                                ll=min(min(var1),min(var2))
                                                rl=max(max(var1),max(var2))
                                                print("leftmost point",ll)
                                                print("rightmost point",rl)
                                                width=abs(ll-rl)
                                                print("width",width)
                                                if(400<width<460):
                                                        print("one vacant parking spot is detected")
                                                else:
                                                        print("more than one vacant parking detected, turn left") 
                                        #if(count<len(lines)):
                                                #count=count+1
                                                #var1.append[x1]              
                                                #var2.append[x2]

                                        #else:
                                                #var1=[]
                                                #var2=[]
                                                
                        
                                        
                
                #print(average)
                                        cv2.imshow('frame',frame)
                                        cv2.waitKey(3)
                else:
                        print("this is occupied region")
                        cv2.imshow('frame',frame)
                        cv2.waitKey(3)

                #hsv6 = cv2.cvtColor(frame, cv2.COLOR_BGR2Lab)
                #hsv7 = cv2.cvtColor(frame, cv2.COLOR_BGR2Luv)
                #hsv8 = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS) # this colorspace was also good
                #hsv9 = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
                #cv2.imshow('frame1',hsv1)
                #cv2.imshow('frame2',hsv2)
                #cv2.imshow('frame3',hsv3)
                #cv2.imshow('frame4',hsv4)
                #cv2.imshow('frame5',hsv5)
                #cv2.imshow('frame6',hsv6)
                #cv2.imshow('frame7',hsv7)
                #cv2.imshow('frame8',hsv8)
                #cv2.imshow('frame9',hsv9)
                #cv2.waitKey(3)

cap.release()
out.release()
cv2.destroyAllWindows
