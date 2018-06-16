#!/usr/bin/env python
import time
import sys
import rospy
import navio.pwm
import navio.util
navio.util.check_apm()
from std_msgs.msg import Float32
class test(object):
	def __init__(self):
		rospy.init_node("RC")		 
		global throttle 
		throttle = navio.pwm.PWM(0) 
		throttle.initialize()
   		throttle.set_period(50)
		throttle.enable()
		global steer
		steer = navio.pwm.PWM(1) 
		steer.initialize()  		
		steer.set_period(50)
		steer.enable()
		rospy.Subscriber('speed', Float32, self.throt, queue_size = 1)
		rospy.Subscriber('steering', Float32, self.steer, queue_size = 1)
		self.rate = rospy.Rate(1)
		self.speed = 0.0
		self.steerang = 0.0
	def throt(self, data):
		self.speed = data.data
		throttle.set_duty_cycle(self.speed)	#throttle
	def steer(self, data):
		steer.set_duty_cycle(data.data) #steering
		
	def spin(self):
		while not rospy.is_shutdown():
			#self.forward()
			car = 1
			

	def reverse(self):
		for i in range (0,2):		
			throttle.set_duty_cycle(1.7) #works fine
			self.rate.sleep()
		for i in range (0,1):
			throttle.set_duty_cycle(1.5)
			self.rate.sleep()
		throttle.set_duty_cycle(1.6)
	def none(self):
		throttle.set_duty_cycle(1.5) #Arming motor
	
if __name__ == '__main__':
	ctrl = test()
	try:
		ctrl.spin()
	except rospy.ROSInterruptException:
		pass
			
		
