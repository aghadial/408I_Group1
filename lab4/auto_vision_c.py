#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

import numpy as np
import cv2 

# Globals
latest_image_received = False
cv_image = None
bridge = CvBridge()

KP = 0.004                 # Proportional gain for turning
FORWARD_SPEED = 0.02       # Slow, constant forward velocity (m/s)
SEARCH_SPIN_SPEED = 0.5 
MIN_CONTOUR_AREA = 500     # Minimum area threshold (pixels) to reject noise

def image_callback(msg):
    global cv_image, latest_image_received

    try:
        # Convert ROS Image message directly to an OpenCV Mat
        cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        latest_image_received = True  # FIX 1: Set flag when image arrives
        
    except CvBridgeError as e:
        rospy.logerr("CvBridge Error: %s", e)

def autonomous_node():
    rospy.init_node('autonomous_node', anonymous=True)
    rospy.Subscriber("/camera/image_raw", Image, image_callback)

    rate = rospy.Rate(10)  # 10 Hz
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    while not rospy.is_shutdown():
        move_cmd = Twist()

        if latest_image_received and cv_image is not None:
            hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
            lower_blue = np.array([110, 50, 50])
            upper_blue = np.array([130, 255, 255])
         
            # Threshold the HSV image to get only blue colors
            mask = cv2.inRange(hsv_image, lower_blue, upper_blue)
        
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            target_found = False

            if contours:
                max_contour = max(contours, key=cv2.contourArea)
        
                # FIX 2: Filter out small speckles/noise using area threshold
                if cv2.contourArea(max_contour) > MIN_CONTOUR_AREA:
                    # Calculate the moments of the largest contour
                    M = cv2.moments(max_contour)
            
                    # Calculate the X and Y coordinates of the center
                    if M["m00"] != 0:
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                        target_found = True

            if target_found:
                # Find the center pixel column of the incoming camera stream dynamically
                image_center_x = cv_image.shape[1] / 2.0
                
                # Calculate tracking error (Target position minus current position)
                error_x = image_center_x - cX
                
                # Apply P-Controller formula to output angular turning velocity
                angular_velocity = error_x * KP
                
                # Set speeds: Slow constant forward speed + proportional turning alignment
                move_cmd.linear.x = FORWARD_SPEED
                move_cmd.angular.z = angular_velocity
                
                rospy.loginfo_throttle(1, f"Tracking Target -> Error: {error_x:.1f} px | Turn Speed: {angular_velocity:.3f} rad/s")
            else:
                # Target is not in view: maintain slow constant rotation velocity to find it
                move_cmd.linear.x = 0.0
                move_cmd.angular.z = SEARCH_SPIN_SPEED
                rospy.loginfo_throttle(2, "Target lost. Executing recovery search spin...")

            pub.publish(move_cmd)
            
        rate.sleep()


if __name__ == '__main__':
    try:
        autonomous_node()
    except rospy.ROSInterruptException:
        pass
    finally:
        # Safely shut down any leftover OpenCV display UI loops upon script termination
        cv2.destroyAllWindows()