#!/usr/bin/env python
import time
import sys
import rospy
import navio.rcinput
import navio.leds
from std_msgs.msg import Float32
rcin = navio.rcinput.RCInput()
led = navio.leds.Led()
class test(object):
        def __init__(self):
                rospy.init_node("RCIN")
                self.pub = rospy.Publisher('steering', Float32, queue_size = 10)
                self.pub1 = rospy.Publisher('speed', Float32, queue_size = 10)
		self.pub2 = rospy.Publisher('flag2', Float32, queue_size = 10)
                led.setColor('Green')
                self.rate = rospy.Rate(1) # 1hz
                self.indflag = 0 #mode flag
		self.stopflag = 0 #stable stop flag during mode change

        def spin(self):
                while not rospy.is_shutdown():
			indication = float(rcin.read(1))/1000
                        #print indication			
			if self.indflag == 0: #manual mode
                        	steer = rcin.read(3)
	                        steer = float(steer)/1000
        	                self.pub.publish(steer)#steering
                        	speed = float(rcin.read(2))/1000
				self.pub1.publish(speed)#speed
                        	self.pub2.publish(self.indflag)
				
                        
				
			if self.indflag == 1:
								
				
								
				self.pub2.publish(self.indflag)
                       	if (indication > 1.6) and (self.indflag == 0):
                                led.setColor('Red')
                               	self.indflag = 1
                               	print "Autonomous Mode Armed"
	                if (indication < 1.4) and (self.indflag == 1):
        	                led.setColor('Green')
           	                self.indflag = 0
                                print "Drive it Yourself"	
                        

if __name__ == '__main__':
        ctrl = test()
        try:
                ctrl.spin()
        except rospy.ROSInterruptException:
                pass

