from DobotMotion import DobotMotion
import math


# INITIALIZE_ROUTINE          = 0
# DUCKIE_SWEEP_ROUTINE        = 1
# DUCKIE_ALIGN_X_ROUTINE      = 2
# DUCKIE_ALIGN_Y_ROUTINE      = 3
# DUCKIE_LOWER_EE_ROUTINE     = 4
# DUCKIE_SUCTION_ON_ROUTINE   = 5
# DUCKIE_LIFT_EE_ROUTINE      = 6
# PP_SWEEP_ROUTINE            = 7
# PP_ALIGN_X_ROUTINE          = 8
# PP_ALIGN_Y_ROUTINE          = 9
# PP_LOWER_EE_ROUTINE         = 10
# PP_SUCTION_OFF_ROUTINE      = 11
# RESET_ROUTINE               = 12
# END_ROUTINE                 = 13



class DuckieLyft():
	def __init__(self, dobot=None, debug=None, video_cap=None):
		self._motion = DobotMotion(dobot,debug,video_cap)

	def _debug(self, *args):
		if self._debugOn:
			# Since "print" is not a function the expansion (*) cannot be used
			# as it is not an operator. So this is a workaround.
			for arg in args:
				sys.stdout.write(str(arg))
				sys.stdout.write(' ')
			print('')

	def runTask1(self):
		"""
		Written by Shu-Nong Wu, Xiao Yang, and David Yang
		Task 1
			- Stationary duckie
			- Stationary platform
			1) Locate duckie
			2) Pickup duckie
			3) Locate platform
			4) Drop duckie on platform
		"""
		if not self._motion.breakout():
			self._motion.initialize()
		if not self._motion.breakout():
			self._motion.sweepDuckie()
		if not self._motion.breakout():
			self._motion.duckieAlignX()
		if not self._motion.breakout():
			self._motion.duckieAlignY()
		if not self._motion.breakout():
			self._motion.duckieLowerEE()
		if not self._motion.breakout():
			self._motion.duckieSuctionOn()
		if not self._motion.breakout():
			self._motion.duckieLiftEE()
		if not self._motion.breakout():
			self._motion.ppSweep()
		if not self._motion.breakout():
			self._motion.ppAlignX()
		if not self._motion.breakout():
			self._motion.ppAlignY()
		if not self._motion.breakout():
			self._motion.ppLowerEE()
		if not self._motion.breakout():
			self._motion.ppSuctionOff()
		if not self._motion.breakout():
			self._motion.reset()
		self._motion.terminate()

	def test2(self):
		"""
		Written by Shu-Nong Wu
		Used for testing picking up of the duckie
		"""
		if not self._motion.breakout():
			self._motion.initialize()
		if not self._motion.breakout():
			self._motion.sweepDuckie()
		if not self._motion.breakout():
			self._motion.duckieAlignX()
		if not self._motion.breakout():
			self._motion.duckieAlignY()
		if not self._motion.breakout():
			self._motion.duckieLowerEE()
		if not self._motion.breakout():
			self._motion.duckieSuctionOn()
		if not self._motion.breakout():
			self._motion.duckieLiftEE()
		self._motion.terminate()

	def test3(self):
		if not self._motion.breakout():
			self._motion.initialize()
		if not self._motion.breakout():
			self._motion.duckieSuctionOn()
		if not self._motion.breakout():
			self._motion.ppSweep()
		if not self._motion.breakout():
			self._motion.ppAlignX()
		if not self._motion.breakout():
			self._motion.ppAlignY()
		if not self._motion.breakout():
			self._motion.ppLowerEE()
		if not self._motion.breakout():
			self._motion.ppSuctionOff()
		if not self._motion.breakout():
			self._motion.reset()
		self._motion.terminate()