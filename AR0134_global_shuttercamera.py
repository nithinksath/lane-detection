#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image as RosImage
from cv_bridge import CvBridge

from ctypes import *

import ctypes

import os
import cv2
import time
import Image
import argparse
import numpy as np
import thread 
from select import select
from evdev import InputDevice

import ArducamSDK
import Queue

COLOR_BYTE2RGB = 48
CAMERA_AR0134 = 0x4D091031
SensorShipAddr = 32
I2C_MODE_16_16  = 3
usbVid = 0x52CB
Width = 1280
Height = 960
cfg ={"u32CameraType":CAMERA_AR0134,
      "u32Width":Width,"u32Height":Height,
      "u32UsbVersion":1,
      "u8PixelBytes":1,
      "u16Vid":0x52cb,
      "u8PixelBits":8,
      "u32SensorShipAddr":SensorShipAddr,
      "emI2cMode":I2C_MODE_16_16 }

regArr = [
    # //[PLL_settings]
    [0x3028, 0x0010],  # //ROW_SPEED = 16
    [0x302A, 0x0010],  # //VT_PIX_CLK_DIV = 16
    [0x302C, 0x0001],  # //VT_SYS_CLK_DIV = 1
    [0x302E, 0x0002],  # //PRE_PLL_CLK_DIV = 2
    [0x3030, 0x0028],  # //PLL_MULTIPLIER = 40
    [0x3032, 0x0000],  # //DIGITAL_BINNING = 0
    [0x30B0, 0x0080],  # //DIGITAL_TEST = 128


    # //[Timing_settings]
    [0x301A, 0x00D8],  # //RESET_REGISTER = 216
    [0x301A, 0x10DC],  # //RESET_REGISTER = 4316
    [0x3002, 0x0000],  # //Y_ADDR_START = 0
    [0x3004, 0x0000],  # //X_ADDR_START = 0
    [0x3006, 0x03BF],  # //Y_ADDR_END = 959
    [0x3008, 0x04FF],  # //X_ADDR_END = 1279
    [0x300A, 0x0488],  # //FRAME_LENGTH_LINES = 1160
    [0x300C, 0x056C],  # //LINE_LENGTH_PCK = 1388
    [0x3012, 0x00D8],  # //COARSE_INTEGRATION_TIME = 216
    [0x3014, 0x00C0],  # //FINE_INTEGRATION_TIME = 192
    [0x30A6, 0x0001],  # //Y_ODD_INC = 1
    [0x308C, 0x0000],  # //Y_ADDR_START_CB = 0
    [0x308A, 0x0000],  # //X_ADDR_START_CB = 0
    [0x3090, 0x03BF],  # //Y_ADDR_END_CB = 959
    [0x308E, 0x04FF],  # //X_ADDR_END_CB = 1279
    [0x30AA, 0x0488],  # //FRAME_LENGTH_LINES_CB = 1160
    [0x3016, 0x00D8],  # //COARSE_INTEGRATION_TIME_CB = 216
    [0x3018, 0x00C0],  # //FINE_INTEGRATION_TIME_CB = 192
    [0x30A8, 0x0001],  # //Y_ODD_INC_CB = 1
    [0x3040, 0x4000],  # //READ_MODE = 0
    # //{0x3064, 0x1982},		#//EMBEDDED_DATA_CTRL = 6530
    [0x3064, 0x1802],
    [0x31C6, 0x8008],  # //HISPI_CONTROL_STATUS = 32776
    [0x301E, 0x0000],  # //data_pedestal
    # //{0x3100, 0x0001},		#//auto exposure

    [0x3002, 0],  # // Y_ADDR_START
    [0x3012, 150],

    [0x3056, 0x004A],  # // Gr_GAIN
    [0x3058, 0x0070],  # // BLUE_GAIN
    [0x305a, 0x0070],  # // RED_GAIN
    [0x305c, 0x004A],  # // Gb_GAIN

    [0x3046, 0x0100],  # //en_flash/Flash indicator

    [0x301a, 0x10DC],

    [0xffff, 0xffff],
    [0xffff, 0xffff]]

global timestamps, images
timestamps = Queue.Queue()
images = Queue.Queue()

def readThread():
    global timestamps, images

    handle = {}
    data = {}
    
    regNum = 0
    res, handle = ArducamSDK.Py_ArduCam_autoopen(cfg)
    #print(handle)
    #print(3)
    if res == 0:
        print("device open success!")
        while (regArr[regNum][0] != 0xFFFF):
            ArducamSDK.Py_ArduCam_writeSensorReg(handle, regArr[regNum][0], regArr[regNum][1])
            regNum = regNum + 1
        #print(32143)
        res = ArducamSDK.Py_ArduCam_beginCapture(handle)
        if res == 0:
            print("transfer task create success!")
            while not rospy.is_shutdown():
                #print(2134124)
                res = ArducamSDK.Py_ArduCam_capture(handle)
                #print(res)
                if res == 0:
                    timestamp = rospy.Time.now()
                    #print(7324627864)
                    res, data = ArducamSDK.Py_ArduCam_read(handle, Width * Height)
                    #print(34242)
                    if res == 0:
                        #print(3746827346782)
                        ArducamSDK.Py_ArduCam_del(handle)
                        #print(374623846278)
                        timestamps.put(timestamp)
                        #print(3742846237846)
                        images.put(data)
                        #print(382746278346782)
                        time.sleep(0.03)
                    else:
                        print("read data fail!")
                if res != 0:
                    print("capture fail!")
                    break
        else:
            print("transfer task create fail!")

        res = ArducamSDK.Py_ArduCam_close(handle)
        if res == 0:
            print("device close success!")
        else:
            print("device close fail!")
    else:
        print("device open fail!")

pass

def camera():
    global timestamps, images

    rospy.init_node("AR0134")
    pub = rospy.Publisher("/cam0/image_raw", RosImage, queue_size=1000)
    print(1)
    thread.start_new_thread(readThread, (), )
    print(2)

    seq = 0
    while not rospy.is_shutdown():
        if not timestamps.empty():
            #print(777)
            timestamp = timestamps.get()
            data = images.get()

            rawImage = Image.frombuffer("L", (Width, Height), data, "raw", "L", 0, 1)
            arrayImage = np.array(rawImage)
            cvImage = cv2.cvtColor(arrayImage, COLOR_BYTE2RGB)
            #cv2.imshow("AR0134",cvImage)
	    #cv2.waitKey(1)

            rosImage = CvBridge().cv2_to_imgmsg(cvImage, "bgr8")
            rosImage.header.stamp = timestamp
            rosImage.header.frame_id = "cam0"
            rosImage.header.seq = seq
            seq = seq + 1
            #print(4)
            pub.publish(rosImage)

if __name__ == "__main__":
	camera()

