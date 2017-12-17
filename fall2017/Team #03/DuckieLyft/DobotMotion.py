from DobotWrapper import DobotWrapper, ANGLE_BOUNDS, SPEED_BOUNDS
from DobotVision import DobotVision
from DobotKinematics import DobotKinematics
from time import sleep
import math

TOOL_HEIGHT = 73
HEIGHT_FROM_GROUND = 80+23
ALLIGN_Y_MOVE_FORWARD_DISTANCE = 15
LOWER_EE_DESIRED_HEIGHT = 107
LIFT_EE_DESIRED_HEIGHT = 170
PP_LOWER_EE_DESIRED_HEIGHT = 165

DELAY_BETWEEN_ROUTINES = 2

class DobotMotion():
    def __init__(self,dobot,debug=False,video_cap=0):
        self._dobot = DobotWrapper(dobot)
        self._kinematics = DobotKinematics(debug=debug)
        self._vision = DobotVision(video_cap=video_cap,debug=debug)
        self._breakout = False
        self._debug = debug

    def setZeroConfig(self, sleep_time=-1):
        """
        Written by Shu-Nong Wu
        Sets the Dobot to zero configuration
        """
        # there is a glitch with the Dobot where q1 must be set to 1 before
        # it can be set to 0, Don't question it
        self._dobot.setJointPositions(-89,0,0,0,0)
        sleep(1)
        self._dobot.setJointPositions(-90,0,0,0,0)
        if sleep_time != -1:
            sleep(sleep_time)


    def initialize(self):
        """
        Written by Shu-Nong Wu
        Initializes the DuckieLyft
        """
        self.setZeroConfig(sleep_time=1)
        assert self._dobot.getJointPositions() == (-90,0,0,0,0), \
        'DuckieLyft Position {}\n'.format(self._dobot.getJointPositions())+\
        'DuckieLyft not succesfully set to zero configuration on startup'
        
    def terminate(self):
        """
        Written by Shu-Nong Wu
        Cleanup code
        """
        self._vision.terminate()

    def breakout(self):
    	return self._breakout

    def sweepDuckie(self):
        # zero configuration to an appropriate inner raduis
        q1, q2, q3, q4, suction = self._dobot.getJointPositions()
        x, y, z = self._kinematics.coordinatesFromAngles(q1, q2, q3)
        while True:
            self._vision.enterFrames()
            self._vision.imshow()
            q1 += 10
            self._dobot.setJointPositions(q1, q2, q3, q4, suction) 
            if len(self._vision.getDuckies()) != 0:
                # print 'Found a Duckie'
                break
            if q1 == ANGLE_BOUNDS['upper_q1']:
                # print 'Couldn\'t find Duckie, give up'
                break
            self._vision.exitFrames()
            if self._vision.pressKey('q'):
            	self._breakout = True
                # print 'Button Pressed' 
                break
            sleep(1)
        self._vision.exitFrames()

    def duckieAlignX(self):
        #Align to the X axis of the Dobot
        q1, q2, q3, q4, suction = self._dobot.getJointPositions()
        threshold = 5
        while True:
            self._vision.enterFrames()
            duckiePos = self._vision.getDuckies()
            if len(duckiePos) != 0:
                self._vision.putDot(duckiePos[0])
                dx, dy = duckiePos[0]
                # print "dx {}, dy {}".format(dx, dy)
                if dx > 320 + threshold:
                    q1 -= 1
                    self._dobot.setJointPositions(q1, q2, q3, q4, suction)
                elif dx < 320 - threshold:
                    q1 += 1
                    self._dobot.setJointPositions(q1, q2, q3, q4, suction)
                else:
                    print('X Aligned')
                    break
            self._vision.imshow()
            self._vision.exitFrames()
            sleep(.5)
            if self._vision.pressKey('q'):
            	self._breakout = True
                break
        self._vision.exitFrames()


    def duckieAlignY(self):
        #Align to the Y axis of the end effector
        threshold = 5
        q1, q2, q3, q4, suction = self._dobot.getJointPositions()
        while True:
            self._vision.enterFrames()
            duckiePos = self._vision.getDuckies()
            if len(duckiePos) != 0:
                self._vision.putDot(duckiePos[0])
                dx, dy = duckiePos[0]
                if dy > 240 + threshold:
                    q2 -= 1
                    self._dobot.setJointPositions(q1, q2, q3, q4, suction)
                elif dy < 240 - threshold:
                    q2 += 1
                    self._dobot.setJointPositions(q1, q2, q3, q4, suction)
                else:
                    q1, q2, q3, q4, suction = self._dobot.getJointPositions()
                    q1rad = math.radians(q1)
                    q2rad = math.radians(q2)
                    q3rad = math.radians(q3)
                    # print 'q1rad {} q2rad {} q3rad{}'.format(q1rad, q2rad, q3rad)
                    x, y, z = self._kinematics.coordinatesFromAngles(q1rad, math.pi/2-q2rad, q3rad)
                    print 'init pos: x {} y {} z {}'.format(x, y, z)
                    desiredmag = math.sqrt(x ** 2 + y ** 2) + ALLIGN_Y_MOVE_FORWARD_DISTANCE
                    desiredx = abs(desiredmag * math.cos(q1rad))
                    desiredy = abs(desiredmag * math.sin(q1rad))
                    if x < 0:
                        desiredx = -desiredx
                    if y < 0:
                        desiredy = -desiredy
                    print 'desiredx {} desiredy {} desiredz{}'.format(desiredx, desiredy, z)
                    q1rad, q2rad, q3rad = self._kinematics.anglesFromCoordinates(desiredx, desiredy, z)
                    q1 = math.degrees(q1rad)
                    q2 = math.degrees(q2rad)
                    q3 = math.degrees(q3rad)
                    self._dobot.setJointPositions(q1, q2, q3, q4, suction)
                    sleep(DELAY_BETWEEN_ROUTINES)
                    print('Y Aligned')
                    break
            sleep(.5)
            self._vision.imshow()
            self._vision.exitFrames()
            if self._vision.pressKey('q'):
            	self._breakout = True
                break
        self._vision.exitFrames()
    
    def duckieLowerEE(self):
        q1, q2, q3, q4, suction = self._dobot.getJointPositions()
        print 'q1 {},q2 {},q3 {},q4 {},'.format(q1,q2,q3,q4)
        q1rad = math.radians(q1)
        q2rad = math.pi/2 - math.radians(q2)
        q3rad = math.radians(q3)
        x, y, z = self._kinematics.coordinatesFromAngles(q1rad,q2rad, q3rad)
        print 'x {}, y {}, z {}'.format(x,y,z)
        q1rad, q2rad, q3rad = self._kinematics.anglesFromCoordinates(x, y, LOWER_EE_DESIRED_HEIGHT)
        q1 = math.degrees(q1rad)
        q2 = math.degrees(q2rad)
        q3 = math.degrees(q3rad)
        self._dobot.setJointPositions(q1, q2, q3, q4, suction)
        print('Suction cup is at z = %s mm' % LOWER_EE_DESIRED_HEIGHT)
                            
    def duckieSuctionOn(self):
        q1, q2, q3, q4, suction = self._dobot.getJointPositions()
        self._dobot.setJointPositions(q1, q2, q3, q4, 1)
        print 'Suction On'
        sleep(DELAY_BETWEEN_ROUTINES+1)
                        
    def duckieLiftEE(self):
        q1, q2, q3, q4, suction = self._dobot.getJointPositions()
        q1rad = math.radians(q1)
        q2rad = math.pi/2 - math.radians(q2)
        q3rad = math.radians(q3)
        LIFT_EE_DESIRED_HEIGHT = 170
        x, y, z = self._kinematics.coordinatesFromAngles(q1rad, q2rad, q3rad)
        q1rad, q2rad, q3rad = self._kinematics.anglesFromCoordinates(x, y, LIFT_EE_DESIRED_HEIGHT)
        q1 = math.degrees(q1rad)
        q2 = math.degrees(q2rad)
        q3 = math.degrees(q3rad)
        self._dobot.setJointPositions(-90, 0, 0, 0, 1)
                        
    def ppSweep(self):
        q1, q2, q3, q4, suction = self._dobot.getJointPositions()
        while True:
            self._vision.enterFrames()
            self._vision.imshow()
            q1 += 10
            self._dobot.setJointPositions(q1, q2, q3, q4, suction) 
            if len(self._vision.getPurplePlatforms()) != 0:
                # print 'Found a Duckie'
                break
            if q1 == ANGLE_BOUNDS['upper_q1']:
                # print 'Couldn\'t find Duckie, give up'
                break
            self._vision.exitFrames()
            if self._vision.pressKey('q'):
            	self._breakout = True
                # print 'Button Pressed' 
                break
            sleep(1)
        self._vision.exitFrames()
                        
    def ppAlignX(self):
        q1, q2, q3, q4, suction = self._dobot.getJointPositions()
        threshold = 40
        while True:
            self._vision.enterFrames()
            ppPos = self._vision.getPurplePlatforms()
            if len(ppPos) != 0:
                self._vision.putDot(ppPos[0])
                dx, dy = ppPos[0]
                # print "dx {}, dy {}".format(dx, dy)
                if dx > 320 + threshold:
                    q1 -= 1
                    self._dobot.setJointPositions(q1, q2, q3, q4, suction)
                elif dx < 320 - threshold:
                    q1 += 1
                    self._dobot.setJointPositions(q1, q2, q3, q4, suction)
                else:
                    print('X Aligned')
                    break
            self._vision.imshow()
            self._vision.exitFrames()
            sleep(.5)
            if self._vision.pressKey('q'):
            	self._breakout = True
                break
        self._vision.exitFrames()
                        
    def ppAlignY(self):
        threshold = 40
        q1, q2, q3, q4, suction = self._dobot.getJointPositions()
        while True:
            self._vision.enterFrames()
            ppPos = self._vision.getPurplePlatforms()
            if len(ppPos) != 0:
                self._vision.putDot(ppPos[0])
                dx, dy = ppPos[0]
                if dy > 160 + threshold:
                    q2 -= 1
                    self._dobot.setJointPositions(q1, q2, q3, q4, suction)
                elif dy < 160 - threshold:
                    q2 += 1
                    self._dobot.setJointPositions(q1, q2, q3, q4, suction)
                else:
                    q1, q2, q3, q4, suction = self._dobot.getJointPositions()
                    q1rad = math.radians(q1)
                    q2rad = math.radians(q2)
                    q3rad = math.radians(q3)
                    # print 'q1rad {} q2rad {} q3rad{}'.format(q1rad, q2rad, q3rad)
                    x, y, z = self._kinematics.coordinatesFromAngles(q1rad, math.pi/2-q2rad, q3rad)
                    print 'init pos: x {} y {} z {}'.format(x, y, z)
                    desiredmag = math.sqrt(x ** 2 + y ** 2) + ALLIGN_Y_MOVE_FORWARD_DISTANCE
                    desiredx = abs(desiredmag * math.cos(q1rad))
                    desiredy = abs(desiredmag * math.sin(q1rad))
                    if x < 0:
                        desiredx = -desiredx
                    if y < 0:
                        desiredy = -desiredy
                    print 'desiredx {} desiredy {} desiredz{}'.format(desiredx, desiredy, z)
                    q1rad, q2rad, q3rad = self._kinematics.anglesFromCoordinates(desiredx, desiredy, z)
                    q1 = math.degrees(q1rad)
                    q2 = math.degrees(q2rad)
                    q3 = math.degrees(q3rad)
                    self._dobot.setJointPositions(q1, q2, q3, q4, suction)
                    sleep(DELAY_BETWEEN_ROUTINES)
                    print('Y Aligned')
                    break
            sleep(.5)
            self._vision.imshow()
            self._vision.exitFrames()
            if self._vision.pressKey('q'):
            	self._breakout = True
                break
                        
    def ppLowerEE(self):
        q1, q2, q3, q4, suction = self._dobot.getJointPositions()
        print 'q1 {},q2 {},q3 {},q4 {},'.format(q1,q2,q3,q4)
        q1rad = math.radians(q1)
        q2rad = math.pi/2 - math.radians(q2)
        q3rad = math.radians(q3)
        x, y, z = self._kinematics.coordinatesFromAngles(q1rad,q2rad, q3rad)
        print 'x {}, y {}, z {}'.format(x,y,z)
        q1rad, q2rad, q3rad = self._kinematics.anglesFromCoordinates(x, y, PP_LOWER_EE_DESIRED_HEIGHT)
        q1 = math.degrees(q1rad)
        q2 = math.degrees(q2rad)
        q3 = math.degrees(q3rad)
        self._dobot.setJointPositions(q1, q2, q3, q4, suction)
        print('Suction cup is at z = %s mm' % PP_LOWER_EE_DESIRED_HEIGHT)
                        
    def ppSuctionOff(self):
        q1, q2, q3, q4, suction = self._dobot.getJointPositions()
        self._dobot.setJointPositions(q1, q2, q3, q4, 0)
        print 'Suction Off'
        sleep(DELAY_BETWEEN_ROUTINES)
                        
    def reset(self):
        self.setZeroConfig(sleep_time = -1);    