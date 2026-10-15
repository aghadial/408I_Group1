#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

obstacle_detected = False
latest_keyboard_cmd = Twist()

def scan_callback(data):

    global obstacle_detected

    #get distance in front on robot
    front_distance = data.ranges[0]

    # If something is closer than 0.3 meters, set the flag to True
    if 0.0 < front_distance < 0.3:
        obstacle_detected = True
    else:
        obstacle_detected = False

def keyboard_callback(msg):
    global latest_keyboard_cmd
    latest_keyboard_cmd = msg

def safety_node():
    rospy.init_node('turtlebot3_safety_node', anonymous=True)

    # Subscribe to 
    rospy.Subscriber('/cmd_vel_mux/keyboard', Twist, keyboard_callback) # get motor info from "Move" file
    rospy.Subscriber('/scan', LaserScan, scan_callback)

    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)  # 10 Hz

    # Main Loop
    while not rospy.is_shutdown():
        final_cmd = Twist()
        
        # Check global obstacle
        
        if obstacle_detected:
            # OVERRIDE: Hard stop if something is in the way
            final_cmd.linear.x = 0.0
            rospy.logwarn("Emergency Stop active!")
        else:
            # NORMAL: Let the keyboard commands pass straight through
            final_cmd = latest_keyboard_cmd
            
        # Send the decided velocity command to the robot
        pub.publish(final_cmd)
        rate.sleep()

if __name__ == '__main__':
    try:
        safety_node()
    except rospy.ROSInterruptException:
        pass