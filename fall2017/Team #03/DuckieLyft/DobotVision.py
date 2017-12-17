"""
Implements vision features for the DuckieLyft

Author: Shu-Nong Wu
Additional Authors:

Special Thanks: Montgomery Blair
for giving me some useful pointers with
regards to object tracking

Version 1.0.0
"""

import cv2
import numpy as np
import sys
import time
from math import sqrt

# Object parameters
DUCKIE_BODY =     dict(lower_hsv=np.array([0, 120, 150]),
					   upper_hsv=np.array([40, 255, 255]),
					   num_er=4,
					   num_di=4,
					   ksize=7,
					   cont_thresh=300)
DUCKIE_BEAK =     dict(lower_hsv=np.array([0, 170, 180]),
					   upper_hsv=np.array([10, 255, 255]),
					   num_er=0,
					   num_di=3,
					   ksize=1,
					   cont_thresh=100)
PURPLE_PLATFORM = dict(lower_hsv=np.array([120, 0, 150]),
					   upper_hsv=np.array([170, 190, 255]),
					   num_er=4,
					   num_di=4,
					   ksize=7,
					   cont_thresh=20000)

# Color parameters
COLOR_YELLOW = (0,255,255)
COLOR_RED    = (0,0,255)
COLOR_BLUE   = (255,0,0)
COLOR_GREEN  = (0,255,0)

# Other parameters
MAX_BODY2BEAK_DIST = 100
	   
class DobotVision:
	def __init__(self, video_cap, debug=False):
		self._cap = cv2.VideoCapture(video_cap)
		self._frame = None
		self._hsv_frame = None
		self._debug_on = debug
		self._last_time = None
		self._fps = None
		self._cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)

	def _debug(self, *args):
		if self._debug_on:
			for arg in args:
				sys.stdout.write(str(arg))
				sys.stdout.write(' ')
			print('')

	def enterFrames(self):
		"""
		Written by Shu-Nong Wu
		Run this in begining of the main while loop
		Loads in a new frame along with its hsv version
		"""
		assert self._cap is not None, 'No video capture entered in DobotVision contructor'
		assert self._frame is None or self._hsv_frame is None, 'Previous frames were not flushed with exitFrames()'
		ret, self._frame = self._cap.read()
		assert ret, 'ERROR READING FROM WEBCAM'
		self._hsv_frame = cv2.cvtColor(self._frame, cv2.COLOR_BGR2HSV)
		self._last_time = time.time()

	def exitFrames(self):
		"""
		Written by Shu-Nong Wu
		Run this at the end of the main while loop
		Flushes the frame
		Calculates the FPS
		Used for general cleanup at the end of each frame
		"""
		self._frame = None
		self._hsv_frame = None
		current_time = time.time()
		self._fps = 1/(self._last_time-current_time)
		self._last_time = current_time

	def imshow(self, frame=True, hsv_frame=False):
		"""
		Written by Shu-Nong Wu
		Shows the video stream
		Can show normal frame and/or hsv_frame
		"""
		if frame:
			cv2.imshow('frame', self._frame)
		if hsv_frame:
			cv2.imshow('hsv_frame', self._hsv_frame)

	def pressKey(self, key = 'q'):
		"""
		Written by Shu-Nong Wu

		"""
		return cv2.waitKey(1) & 0xFF == ord(key)

	def putDot(self,pos=None, color=COLOR_RED):
		if pos is not None:
			cv2.circle(self._frame, pos, 5, color, -1)

	def putTextOnFrame(self, text, pos, color=COLOR_YELLOW):
		"""
		Written by Shu-Nong Wu
		Adds text to frame on position pos
		Default color is yellow
		"""
		cv2.putText(self._frame, text, pos, cv2.FONT_HERSHEY_COMPLEX, 1, color, 2, cv2.LINE_AA)

	def terminate(self):
		"""
		Written by Shu-Nong Wu
		Releases video capture
		Closes the stream window
		"""
		if self._cap is not None:
			self._cap.release()
		cv2.destroyAllWindows()

	def getFPS(self):
		"""
		Written by Shu-Nong Wu
		Returns the FPS
		"""
		return self._fps

	def _getObjectContours(self, obj_param):
		"""
		Written by Shu-Nong Wu
		Performs a set a CV operations on the current frame such as 
		HSV thresholding, erosion, dilation, and blurring
		Returns the contours of the frame
		"""
		blur = cv2.cv2.medianBlur(self._hsv_frame,obj_param['ksize'])  # blur to reduce noise
		mask = cv2.inRange(blur, obj_param['lower_hsv'], obj_param['upper_hsv'])
		mask = cv2.erode(mask, None, iterations=obj_param['num_er'])
		mask = cv2.dilate(mask, None, iterations=obj_param['num_di'])
		cv2.imshow('mask',mask)
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
		return cnts

	def _getCenterOfContours(self, contours, obj_param):
		centers = []
		if len(contours) > 0:
			sorted(contours, key=lambda cnt: cv2.contourArea(cnt))
			for cnt in contours:
				self._debug('contour area', cv2.contourArea(cnt))
				if cv2.contourArea(cnt) >= obj_param['cont_thresh']:
					M = cv2.moments(cnt)
					centers.append((int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])))
		return centers

	def getCenterOfObjects(self, obj_param):
		"""
		Written by Shu-Nong Wu
		Returns a list of tuples containing the center (x,y) of all detect objects
		"""
		cnts = self._getObjectContours(obj_param)
		self._debug('num contours', len(cnts))
		object_centers = self._getCenterOfContours(cnts, obj_param)
		self._debug('num objects', len(object_centers))
		return object_centers

	def getDuckies(self, single=True):
		"""
		Written by Shu-Nong Wu
		Returns the center of a duckie
		Duckies much have a yellow body with a red beak
		"""
		duck_beaks = self.getCenterOfObjects(DUCKIE_BEAK)
		duck_bodys = self.getCenterOfObjects(DUCKIE_BODY)
		# body_centers = []
		# beak_centers = []
		centers = []
		for duck_body in duck_bodys:
			for duck_beak in duck_beaks:
				beak_body_dist = sqrt((duck_body[0]-duck_beak[0])**2+((duck_body[1]-duck_beak[1])**2)) 
				self._debug('beak body dist', beak_body_dist)
				if beak_body_dist < MAX_BODY2BEAK_DIST:
					average_center = (int(2.0/3*duck_body[0]+1.0/3*duck_beak[0]),int(2.0/3*duck_body[1]+1.0/3*duck_beak[1]))
					# body_centers.append(duck_body)
					# beak_centers.append(duck_beak)
					centers.append(average_center)
		# return centers, body_centers, beak_centers
		return centers

	def getPurplePlatforms(self):
		'''
		Written by Shu-Nong Wu
		Returns the center of the purple platform
		'''
		return self.getCenterOfObjects(PURPLE_PLATFORM)