from DuckieLyft import DuckieLyft
# DELETE BELOW
import DobotVision as dv
import DobotKinematics as dk
import cv2
#DELETE ABOVE
import time
from RobotRaconteur.Client import *

def main():
	# RRN is imported from RobotRaconteur.Client
	# Connect tqqqqqqq the service.
	dobot = RRN.ConnectService("tcp://localhost:10001/dobotRR/dobotController")
	duckie_lyft = DuckieLyft(dobot=dobot, debug=False, video_cap=1)
	duckie_lyft.test3()

def main2():
	dobot = RRN.ConnectService("tcp://localhost:10001/dobotRR/dobotController")
	duckie_lyft = DuckieLyft(dobot=dobot, debug=False, video_cap=1)
	duckie_lyft.test2()

def main3():
	dobot = RRN.ConnectService("tcp://localhost:10001/dobotRR/dobotController")
	duckie_lyft = DuckieLyft(dobot=dobot, debug=False, video_cap=1)
	duckie_lyft.runTask1()

def vision_sandbox1():
	vision = dv.DobotVision(video_cap = 1, debug=False)

	# time_last = time.time()
	while(1):
	    vision.enterFrames()

	    # body_centers = vision.getCenters(dv.DUCKIE_BODY)
	    # body_centers = vision.getCenterOfObjects(dv.DUCKIE_BEAK)
	    # body_centers = vision.getCenterOfObjects(dv.PURPLE_PLATFORM)
	    # for i in body_centers:
	    #     vision.putTextOnFrame(text="Duckie at "+str(i), pos=i, color='YELLOW')  
	    
	    # if len(body_centers):
	    #     vision.putTextOnFrame(text="Duckie at "+str(body_centers[0]), pos=body_centers[0], color='YELLOW')
	    #     vision.putDot(pos=body_centers[0])

	    # duckies, bodies, beaks = vision.getDuckies()
	    # for duckie, body, beak in zip(duckies, bodies, beaks):
	    #     vision.putTextOnFrame(text="Duckie at "+str(duckie), pos=duckie, color=dv.COLOR_YELLOW)  
	    #     vision.putDot(duckie)
	    #     vision.putDot(body, color=dv.COLOR_GREEN)
	    #     vision.putDot(beak, color=dv.COLOR_GREEN)
	    # vision.imshow()   

	    # duckies = vision.getDuckies()
	    # for duckie in duckies:
	    #     vision.putTextOnFrame(text="Duckie at "+str(duckie), pos=duckie, color=dv.COLOR_YELLOW)  
	    #     vision.putDot(duckie)
	    # vision.imshow()   

	    pps = vision.getPurplePlatforms()
	    for pp in pps:
	        vision.putTextOnFrame(text="PP at "+str(pp), pos=pp, color=dv.COLOR_YELLOW)  
	        vision.putDot(pp)
	    vision.imshow(frame=True, hsv_frame=True)

	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        break

	    vision.exitFrames()

	vision.terminate()
	cv2.destroyAllWindows()


if __name__ == '__main__':
	# main()
	# main2()
	main3()
	# vision_sandbox1()
