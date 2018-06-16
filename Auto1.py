#!/usr/bin/env python
import time
import sys
import rospy
import navio.pwm
import navio.util
navio.util.check_apm()
from std_msgs.msg import Float32
from std_msgs.msg import Int32
class test(object):
        def __init__(self):
                rospy.init_node("Auto")
                
                rospy.Subscriber('flag2', Float32, self.control, queue_size = 10)
                rospy.Subscriber('flag1', Int32, self.cv, queue_size = 10)
		self.pub = rospy.Publisher('steering', Float32, queue_size = 10)
                self.pub1 = rospy.Publisher('speed', Float32, queue_size = 10)
                self.cv_flag = 0
                self.speed = 1.52
                self.steer = 1.425
                self.complete1 = 1
                
        
        def cv(self, data1):
                self.cv_flag = data.data1


        def control(self, data2):
                
                self.complete1 = data.data2
                if(data.data2 == 1) and (self.cv_flag == 1):
                	self.steer = 1.425
                        self.pub.publish(self.steer)
                        self.speed = 1.2
                        self.pub1.publish(self.speed)
                              
                
                #stop
                if (data.data2 == 1) and (self.cv_flag == 0):
	        	self.steer = 1.425
                	self.pub.publish(self.steer)
                        self.speed = 1.52
                	self.pub1.publish(self.speed)
              
        def spin(self):
        	while not rospy.is_shutdown():
                      
                        if self.complete1 == 1:
                                self.pub.publish(self.steer)
                                self.pub1.publish(self.speed)
                                print "auto"
if __name__ == '__main__':
        ctrl = test()
        try:
                ctrl.spin()
        except rospy.ROSInterruptException:
                pass







