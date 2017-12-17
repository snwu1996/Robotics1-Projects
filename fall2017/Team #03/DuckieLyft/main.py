from DuckieLyft import DuckieLyft
import time
from RobotRaconteur.Client import *


def main():
 	dobot = RRN.ConnectService("tcp://localhost:10001/dobotRR/dobotController")
	duckie_lyft = DuckieLyft(dobot=dobot, debug=False, video_cap=1)
	duckie_lyft.runTask1()

if __name__ == '__main__':
    main()
