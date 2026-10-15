#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import sys
import select
import tty
import termios

# Save original system terminal settings
settings = termios.tcgetattr(sys.stdin)

# Get keystrokes
def get_key():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)    
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    # Restore normal terminal behavior
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def move():
    rospy.init_node('turtlebot3_autonomous_move', anonymous=True)
    pub = rospy.Publisher('/cmd_vel_mux/keyboard', Twist, queue_size=10) # sending motor info to intermediate topic
    rate = rospy.Rate(10)  # 10 Hz
    vel_msg = Twist()

    # Move forward 
    '''
    vel_msg.linear.x = 0.2  # Forward speed
    vel_msg.angular.z = 0.0  # No rotation
    '''

    while not rospy.is_shutdown():

        key = get_key()

        if key == 'w':
            vel_msg.linear.x = 0.2  # Forward speed
            vel_msg.angular.z = 0.0  # No rotation    
        elif key == 's':
            vel_msg.linear.x = -0.2  # Forward backward
            vel_msg.angular.z = 0.0  # No rotation
        elif key == 'a':
            vel_msg.linear.x = 0.0  # No linear
            vel_msg.angular.z = 1.0  # Rotate left
        elif key == 'd':
            vel_msg.linear.x = 0.0  # No  linear
            vel_msg.angular.z = -1.0  # Rotate right
        elif key == 'z':
            vel_msg.linear.x = 0.0  # No linear 
            vel_msg.angular.z = 0.0  # No rotation
        elif key == '\x03':           # Catch Ctrl+C key combo
            break


        pub.publish(vel_msg)
        rate.sleep()


if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException:
        pass
    finally:
        # Guarantee the terminal settings return to normal even if the script crashes
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

