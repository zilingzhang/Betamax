#Python 3.6.1 |Anaconda 4.4.0 (64-bit)| (default, May 11 2017, 13:25:24) [MSC v.1900 64 bit (AMD64)] on win32
#Type "copyright", "credits" or "license()" for more information.
#!/usr/bin/env python

'''
Copyright (c) 2015, Mark Silliman
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

# TurtleBot must have minimal.launch & amcl_demo.launch
# running prior to starting this script
# For simulation: launch gazebo world & amcl_demo prior to run this script

import rospy
import random
import math
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion

# Enter corners of room, then how many points you want robot to move to (square)
x1 = -0.2
y1 = 0.3
x2 = 1.4
y2 = -1.2
points = 4
root = math.sqrt(points)
while (int(root + 0.5) ** 2 != points):
    root = math.sqrt(points)
    points = round(points)
# Increment number of points until it is a perfect square
    points = points+1
    root = math.sqrt(points)
# Find next greatest perfect square
points2 = points + 1
root2 = math.sqrt(points2)
while (int(root2 + 0.5) ** 2 != points2):
    root2 = math.sqrt(points2)
# Increment number of points until it is a perfect square
    points2+=1
# Print side of square 
root = int(round(root))
print(root)
# Print next largest side of square (3x3 = 4)
root2 = int(round(math.sqrt(points2)))
print(root2)
# Set x coordinate closer to origin as x1
if x1 > x2:
    temp = x1;
    x1 = x2;
    x2 = temp;

class GoToPose():
    def __init__(self):

        self.goal_sent = False

    # What to do if shut down (e.g. Ctrl-C or failure)
        rospy.on_shutdown(self.shutdown)

    # Tell the action client that we want to spin a thread by default
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        rospy.loginfo("Wait for the action server to come up")

    # Allow up to 5 seconds for the action server to come up
        self.move_base.wait_for_server(rospy.Duration(5))

    def goto(self, pos, quat):

    # Send a goal
        self.goal_sent = True
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose = Pose(Point(pos['x'], pos['y'], 0.000),
                         Quaternion(quat['r1'], quat['r2'], quat['r3'], quat['r4']))

    # Start moving
        self.move_base.send_goal(goal)

    # Allow TurtleBot up to 60 seconds to complete task
        success = self.move_base.wait_for_result(rospy.Duration(60)) 

        state = self.move_base.get_state()
        result = False

        if success and state == GoalStatus.SUCCEEDED:
    # We made it!
            result = True
        else:
            self.move_base.cancel_goal()

        self.goal_sent = False
        return result
    def moveAround(self,x1,y1,x2,y2,points):
        root = math.sqrt(points)
        while (int(root + 0.5) ** 2 == points):
            root = math.sqrt(points)
            points = round(points)
            points = points+1
    def shutdown(self):
        if self.goal_sent:
            self.move_base.cancel_goal()
            rospy.loginfo("Stop")
            rospy.sleep(1)

if __name__ == '__main__':
    try:
        rospy.init_node('nav_test', anonymous=False)
        navigator = GoToPose()
# Position coordinates customized based on user input

        for i in range (0,root):
            if i%2 == 0:
                for j in range (0,root):
                    x = ((x2-x1)/root*j+x1+(x2-x1)/root*(j+1)+x1)/2
                    y = ((y2-y1)/root*i+y1+(y2-y1)/root*(i+1)+y1)/2
                    # Print coordinates
                    print ('(X,Y) = ',x,',',y,'\n')
                    position = {'x': x, 'y' : y}
                    theta = 0;
                    #NOTE: If the following commands do not work outside the loop, comment them and uncomment the ones below.
                    quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : theta, 'r4' : 1.000}
                    success = navigator.goto(position, quaternion)
                    if success:
                        rospy.loginfo("Hooray, reached (%s, %s)",x,y)
                    else:
                        rospy.loginfo("The base failed to reach the desired pose (%s, %s)",x,y)

# Sleep to give the last log messages time to be sent
                    rospy.sleep(3)

            else:
                for j in range (root-1,-1,-1):
                    x = ((x2-x1)/root*j+x1+(x2-x1)/root*(j+1)+x1)/2
                    y = ((y2-y1)/root*i+y1+(y2-y1)/root*(i+1)+y1)/2
                    print ('(X,Y) = ',x,',',y,'\n')
                    theta = 3.14159;
                    position = {'x': x, 'y' : y}
                    quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : theta, 'r4' : 1.000}
                    rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
                    success = navigator.goto(position, quaternion)
                    if success:
                        rospy.loginfo("Hooray, reached (%s, %s)",x,y)
                    else:
                        rospy.loginfo("The base failed to reach the desired pose (%s, %s)",x,y)
#            position = {'x': x, 'y' : y}
#            quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : theta, 'r4' : 1.000}
#            success = navigator.goto(position, quaternion)
#            if success:
#                rospy.loginfo("Hooray, reached (%s, %s)",xPos[i],yPos[i])
#            else:
#                rospy.loginfo("The base failed to reach the desired pose (%s, %s)",xPos[i],yPos[i])

# Sleep to give the last log messages time to be sent
            rospy.sleep(3)

    except rospy.ROSInterruptException:
        rospy.loginfo("Ctrl-C caught. Quitting")
