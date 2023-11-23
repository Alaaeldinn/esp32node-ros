#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
import requests

rospy.init_node('esp32cam_node')

# ESP32 URL
URL = "192.168.215.161"
AWB = True

cap = cv2.VideoCapture(URL + ":81/stream")

bridge = CvBridge()
image_pub = rospy.Publisher('/esp32/image_raw', Image, queue_size=1)

def set_resolution(url, index=1, verbose=False):
    try:
        if verbose:
            resolutions = "10: UXGA(1600x1200)\n9: SXGA(1280x1024)\n8: XGA(1024x768)\n7: SVGA(800x600)\n6: VGA(640x480)\n5: CIF(400x296)\n4: QVGA(320x240)\n3: HQVGA(240x176)\n0: QQVGA(160x120)"
            print("available resolutions\n{}".format(resolutions))

        if index in [10, 9, 8, 7, 6, 5, 4, 3, 0]:
            requests.get(url + "/control?var=framesize&val={}".format(index))
        else:
            print("Wrong index")
    except:
        print("SET_RESOLUTION: something went wrong")

def set_quality(url, value=1, verbose=False):
    try:
        if 10 <= value <= 63:
            requests.get(url + "/control?var=quality&val={}".format(value))
    except:
        print("SET_QUALITY: something went wrong")

def set_awb(url, awb=1):
    try:
        awb = not awb
        requests.get(url + "/control?var=awb&val={}".format(1 if awb else 0))
    except:
        print("SET_QUALITY: something went wrong")
    return awb

def main():
    set_resolution(URL, index=8)

    while not rospy.is_shutdown():
        if cap.isOpened():
            ret, frame = cap.read()

            image_msg = bridge.cv2_to_imgmsg(frame, "bgr8")
            image_pub.publish(image_msg)

        
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

