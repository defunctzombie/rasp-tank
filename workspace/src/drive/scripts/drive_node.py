#!/usr/bin/env python

import time
import rospy
import rasptank
import drive

from std_msgs.msg import Float32
from geometry_msgs.msg import Twist

## The drive node subscribes to /cmd_vel (geometry_msgs/twist) and sends
## motor power on every received message.
##
## If a command is not received within 100ms then the motors are stopped

def main():
    # anonymouse false to prevent multiple drive nodes
    rospy.init_node('drive', anonymous=False)

    pub_commanded_left = rospy.Publisher('/drive/debug/commanded_left', Float32, queue_size=10)
    pub_commanded_right = rospy.Publisher('/drive/debug/commanded_right', Float32, queue_size=10)

    # track the last time we received a message for timeout to stop driving
    last_receive_time = time.time()

    # handle the cmd_vel message
    def onCmdVel(data):
        nonlocal last_receive_time

        try:
            # convert linear [-100, 100] and angular [-100, 100] into left/right power [-100, 100]
            left_power, right_power = drive.control_to_power(data.linear.x, data.angular.z)

            # write to drive
            # publish the commanded commands
            raspdrive.motor_left(left_power)
            raspdrive.motor_right(right_power)

            # publish some debug messages
            pub_commanded_left.publish(Float32(left_power))
            pub_commanded_right.publish(Float32(right_power))

            # indicate we've received commands
            last_receive_time = time.time()
        except  Exception as ex:
            rospy.logerr(ex, exc_info=True)

    rospy.loginfo("Setup raspdrive")
    raspdrive = rasptank.Drive()

    try:
        raspdrive.init()
        raspdrive.stop()
    except  Exception as ex:
        rospy.logerr(ex, exc_info=True)

    try:
        rospy.loginfo("Setup /cmd_vel subscriber")
        rospy.Subscriber("/cmd_vel", Twist, onCmdVel)

        rospy.loginfo("Setup complete...entering node loop")

        rate = rospy.Rate(1) # Hz
        while not rospy.is_shutdown():
            # we haven't received a message in time so we stop the robot
            if last_receive_time + 0.5 < time.time():
                rospy.loginfo("Message receive timeout. Stopping robot. Last received message: {time}".format(time=last_receive_time))
                raspdrive.stop()
                pub_commanded_left.publish(Float32(0))
                pub_commanded_right.publish(Float32(0))

            rate.sleep()
    except rospy.ROSInterruptException:
        pass
    finally:
        raspdrive.stop()
        raspdrive.cleanup()

if __name__ == '__main__':
    main()