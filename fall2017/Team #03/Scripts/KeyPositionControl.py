from RobotRaconteur.Client import *
import time
import msvcrt

def main():
    dobot = RRN.ConnectService("tcp://localhost:10001/dobotRR/dobotController")
    dobot.initialize()
    dobot.setSpeed(vel=100,acc=100)
    print "1,2 increases and decreases Stepper 1"
    print "3,4 increases and decreases Stepper 2"
    print "5,6 increases and decreases Stepper 3"
    print "7,8 increases and decreases Tool Rotation Servo"
    print "9,0 turns on//off the suction"
    curr_joint_pos = list(dobot.getJointPositions())+[0]
    while(1):
        #gets user input
        try:
            # user_input = input()
            user_input = int(msvcrt.getch())
            time.sleep(.1)
            if not (user_input >=0 and user_input <=9) :
                raise Exception
        except:
            print "Invalid input"
            continue
        #change the list of joint positions
        if user_input%2 == 1:
            curr_joint_pos[user_input/2] += 1
        elif user_input%2 == 0:
            curr_joint_pos[user_input/2-1] -= 1
        #bound the dobot parameters
        bounds = ((-90, 90), (0, 30), (0, 80), (-30, 30), (0, 1))
        for i in range(len(curr_joint_pos)):
            curr_joint_pos[i] = max(curr_joint_pos[i], bounds[i][0])
            curr_joint_pos[i] = min(curr_joint_pos[i], bounds[i][1])

        print curr_joint_pos
        dobot.setJointPositions(*curr_joint_pos)

if __name__ == '__main__':
    main()