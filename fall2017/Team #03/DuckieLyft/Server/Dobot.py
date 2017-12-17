import time
from DobotSerialInterface import DobotSerialInterface

class Dobot():
    def __init__(self, port):
        self.desired_joint_angles = [0, 0, 0, 0, 0];
        self.new_command = False;
        self.dobot_interface = DobotSerialInterface(port)
        self.dobot_interface.set_speed()
        self.dobot_interface.set_playback_config()

    def setJointPositions(self, q1, q2, q3, q4, suction):
        self.new_command = True;
        self.desired_joint_angles = [q1, q2, q3, q4, suction];

    def getJointPositions(self):
        return self.dobot_interface.current_status.angles

    def loop(self):
        print 'hi'
        while 1:
            time.sleep(.01)
            if self.new_command:
                suction = False
                print self.desired_joint_angles
                if self.desired_joint_angles[-1] > 0:
                    print 'SUCTION ON!'
                    suction = True
                self.dobot_interface.send_absolute_angles(self.desired_joint_angles[0], self.desired_joint_angles[1],
                                                          self.desired_joint_angles[2], self.desired_joint_angles[3], 1,
                                                          suction)
                self.new_command = False

    def setSpeed(self, vel=100, acc=100):
        """
        Written by Shu-Nong Wu
        Sets velocity and acceleration
        """
        self.dobot_interface.set_speed(vel, acc)

    # def initialize(self):
    #     """Written by Shu-Nong Wu, Sets up the Dobot in default configuration and queues the user to continue"""
    #     self.dobot_interface.send_absolute_angles(1, 0, 0, 0, 1, 0)
    #     time.sleep(1)
    #     self.dobot_interface.send_absolute_angles(0, 0, 0, 0, 1, 0)
    #     time.sleep(1)
    #     try:
    #         assert (self.dobot_interface.current_status.angles == (0, 0, 0, 0))
    #     except:
    #         print self.dobot_interface.current_status.angles
    #         print "Please calibrate the Dobot"


    # def setZeroConfig(self):
    #     """Written by Shu-Nong Wu"""
    #     self.new_command = True;
    #     self.desired_joint_angles = [0, 0, 0, 0, 0];