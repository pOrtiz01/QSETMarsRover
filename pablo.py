import math 

import time 

import rospy  # this is the module required for all simulation communication 

 
 

# start of wheel control code 

from wheel_control.msg import wheelSpeed  # this is a required module for the drive communication 

 
 

rospy.init_node("controller") 

 
 

class WheelController: 

 
 

    def __init__(self): 

        self.wheel_pub = rospy.Publisher("/gazebo_wheelControl/wheelSpeedTopic", wheelSpeed, queue_size=1) 

 
 

    def drive_wheels(self, left, right): 

        # type: (float, float) -> None 

        # left and right are numbers between -1 and 1 

        msg = wheelSpeed() 

        msg.left = left 

        msg.right = right 

        msg.wheelMode = 0 

        self.wheel_pub.publish(msg) 

        #print(msg) 

 
 
 

# end of wheel control code 

 
 

# start of laser scan code 

from sensor_msgs.msg import LaserScan 

 
 
 

class LaserListener: 

 
 

    def __init__(self): 

        self.laserSub = rospy.Subscriber("/leddar/leddarData", LaserScan, self.laser_callback, queue_size=1) 

        self.laserRanges = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] 

 
 

    def laser_callback(self, msg): 

        # type: (LaserScan) -> None 

        self.laserRanges = msg.ranges 

 
 
 

# end of laser scan code access laserRanges for an array of all measured distances from the laser sensors 

 
 

# start of localization stuff 

from geometry_msgs.msg import Point 

from std_msgs.msg import Float32 

 
 
 

class LocationHeading: 

 
 

    def __init__(self): 

        self.fixSub = rospy.Subscriber("/fix/metres", Point, self.fix_callback, queue_size=1) 

        self.headingSub = rospy.Subscriber("/heading",Float32, self.heading_callback, queue_size=1) 

        self.x = 0.0 

        self.y = 0.0 

        self.z = 0.0 

        self.heading = 0.0 

 
 

    def fix_callback(self, msg): 

        # type: (Point) -> None 

        self.x = msg.x 

        self.y = msg.y 

        self.z = msg.z 

 
 

    def heading_callback(self, msg): 

        # type: (Float32) -> None 

        self.heading = msg.data 

 
 
 
 

def create_Vector(cord1,cord2): 

    fvector = [] 

    fvector[0]=cord2[0]-cord1[0] 

    fvector[1]=cord2[1]-cord1[1] 

    return fvector 

  
 

def turn_Angle(angle, direction): 

    steps = stepCalculator(angle) 

    if direction == "r": 

        for t in range(steps): 

            rover.drive(0,1) 

    else: 

        for t in range(steps): 

            rover.drive(1,0) 

 
 

##def best_First_Search_Rock(array): 

##    counter = 0 

##    counter2 = 0 

##    myList = [] 

##    for n,i in enumerate(array): 

##        if i <= 20 and counter == 0: 

##            while True: 

##                if array[n+1+counter] >= 20: 

##                    break 

##                else: 

##                    counter += 1                     

##            myList.append([n,counter]) 

##        elif counter >= 1: 

##                counter -= 1 

## 

##    largeRock = myList[0][1] 

##    smallCord 

##    for ind in myList: 

##        if ind[1] < largeRock: 

##            ind[1] = largeRock       

# end of localization stuff 

 
def decide(array):
    
    if (array[0] == True and array[1] == True and array[2] == True):
        
        wheel.drive_wheels(-.2,-.2)
        
        r=findGap(laser.laserRanges)[0]
        l=findGap(laser.laserRanges)[1]
        
        if r==True:
            wheel.drive_wheels(-1,1)
        elif l==True:
            wheel.drive_wheels(1,-1)

    elif array[1] == False:
        wheel.drive_wheels(1,1)
    
    else :
        if array[2]== True:
            for x in range (0,10):
                wheel.drive_wheels(-1,-1)
            
            for x in range(0,50):
                wheel.drive_wheels(-1,1)
        elif array[0]== True:
            for x in range (0,10):
                wheel.drive_wheels(-1,-1)
            for x in range(0,50):
                wheel.drive_wheels(1,-1)

def findGap(array):
    l=False
    r=False
    gap=0
    found=False
    for x in range(0,15):
        if array[x] >=10:
            gap=x
            found = True
            break
    if found == False:
        r=False
        l=False
    elif gap>7:
        r=True
    else:
        l=True
    return[r,l]

def check_turning():            
    counter =0
    for x in range(0,10):
        print("j")
        wheel.drive_wheels(-1,1)
        counter =x
    if counter == 10:
        wheel.drive_wheels(0,0)
   
    
    



def rock_Checker(array): 

    l = False 

    c = False 

    r = False 

    for i in range(5): 

        if array[i] <= 10: 

            r = True 

    for i in range(5,12): 

        if array[i] <= 10: 

            c = True 

    for i in range(12,15): 

        if array[i] <= 10: 

            l = True 

    return [l,c,r] 

 

    


 

     

 
 
 

#initiallize classes to get and send data to gazebo 

locHead  = LocationHeading() 

laser = LaserListener() 

wheel = WheelController() 

#end of initialization 

 
 

# start of control loop snippet 



while not rospy.is_shutdown():  #this will run until gazebo is shut down or CTRL+C is pressed in the ubuntu window that is running this code 
    
   
    minRange = 99 #initialize minRange to a value larger than what will be recieved 

    for x in range(0, 15): #iterate through the ranges list 

        if laser.laserRanges[x] < minRange: #if the current range is smaller than the smallest know range 

            minRange = laser.laserRanges[x] #update the range 
    
    
    #wheel.drive_wheels(0,0)
    decide(rock_Checker(laser.laserRanges))
    
    
   
   

    
    
    
   

    

    

    

   
    #print(rock_Checker(laser.laserRanges)) 



    #print("Current Heading: ", locHead.heading, "Current x val: ", locHead.x, "RightMostLaser: ", laser.laserRanges[0]) #print some random data to the command line 

 
 

# end of control loop snippet 

 
 

 
