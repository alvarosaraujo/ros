#!/usr/bin/env python
import rospy, sys, os
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt

class turtlebot():

    #Creating our node,publisher and subscriber
    def __init__(self):

        # Start ros node
        rospy.init_node('turtlebot_controller', anonymous=True)
        
        # Define topic to publish - robot velocity
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        
        # Define topic to subscribe - robot position
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.callback)
        
        # Create pose object to store robot position
        self.pose = Pose()
        self.rate = rospy.Rate(10)

    #Callback function implementing the pose value received
    def callback(self, data):

        self.pose = data
        #print self.pose
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

    
    def move2goal(self):
        
        # Create pose object to store user defined goal
        goal_pose = Pose()
        
        # Read input from CLI. Integer for x goal or 'q' to close application
        cmd = raw_input("Set your x goal, or 'q' to exit: ")
        
        # If read data from CLI is not 'q'
        if cmd != "q":
        
            # Read x setpoint, y setpoint and tolerance defined by the user
            goal_pose.x = int(cmd, 16)
            goal_pose.y = input("Set your y goal: ")
            distance_tolerance = input("Set your tolerance: ")
            vel_msg = Twist()

            
            while sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2)) >= distance_tolerance:

                #Porportional Controller
                #linear velocity in the x-axis:
                vel_msg.linear.x = 1.5 * sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2))
                vel_msg.linear.y = 0
                vel_msg.linear.z = 0

                #angular velocity in the z-axis:
                vel_msg.angular.x = 0
                vel_msg.angular.y = 0
                vel_msg.angular.z = 5 * (atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x) - self.pose.theta)

                #Publishing our vel_msg
                self.velocity_publisher.publish(vel_msg)
                self.rate.sleep()

            #Stopping our robot after the movement is over
            vel_msg.linear.x = 0
            vel_msg.angular.z =0
            self.velocity_publisher.publish(vel_msg)

            #rospy.spin()

            return
            
        else:
        
            sys.exit(0)

if __name__ == '__main__':

    try:
    
        # Create turtlebot class
        x = turtlebot()
        
        while True:
    
            # Move the robot to the position defined by the user in a loop
            x.move2goal()

    except rospy.ROSInterruptException: pass
