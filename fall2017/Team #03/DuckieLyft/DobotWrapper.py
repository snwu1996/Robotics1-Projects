ANGLE_BOUNDS = dict(lower_q1      = -90,
					upper_q1      = 90,
					lower_q2      = 0,
					upper_q2      = 40,
					lower_q3      = 0,
					upper_q3      = 80,
					lower_q4      = -30,
					upper_q4      = 30,
					lower_suction = 0,
					upper_suction = 1)
SPEED_BOUNDS = dict(lower_vel = 0,
					upper_vel = 100,
					lower_acc = 0,
					upper_acc = 100)

ZERO_CONFIGURATION = (-90,0,0,0)

class DobotWrapper():
	def __init__(self, dobot=None):
		self._dobot = dobot
		self._joint_positions = None
		self._ee_location = None

	def boundAngles(self, q1, q2, q3, q4, suction):
		"""
		Written by Shu-Nong Wu
		
		"""
		new_q1 = max(q1,ANGLE_BOUNDS['lower_q1'])
		new_q1 = min(q1,ANGLE_BOUNDS['upper_q1'])
		new_q2 = max(q2,ANGLE_BOUNDS['lower_q2'])
		new_q2 = min(q2,ANGLE_BOUNDS['upper_q2'])
		new_q3 = max(q3,ANGLE_BOUNDS['lower_q3'])
		new_q3 = min(q3,ANGLE_BOUNDS['upper_q3'])
		new_q4 = max(q4,ANGLE_BOUNDS['lower_q4'])
		new_q4 = min(q4,ANGLE_BOUNDS['upper_q4'])
		new_suction = max(suction,ANGLE_BOUNDS['lower_suction'])
		new_suction = min(suction,ANGLE_BOUNDS['upper_suction'])
		if (new_q1, new_q2, new_q3, new_q4, new_suction) != (q1, q2, q3, q4, suction):
			# print (new_q1, new_q2, new_q3, new_q4, new_suction)
			print 'debug: ', 'Desired joint position {} out of bounds'.format((q1, q2, q3, q4, suction))        
		return (new_q1, new_q2, new_q3, new_q4, new_suction)

	def setJointPositions(self, q1, q2, q3, q4, suction):
		"""
		Written by Shu-Nong Wu
		Sets the joint angles
		"""
		new_joint_pos = self.boundAngles(q1,q2,q3,q4,suction)
		self._dobot.setJointPositions(*new_joint_pos)
		self._joint_positions = (q1,q2,q3,q4,suction)

	def getJointPositions(self):
		"""
		Written by Shu-Nong Wu
		Returns the joint angles
		"""
		return self._joint_positions

	def boundSpeed(self, vel, acc):
		"""
		Written by Shu-Nong Wu
		
		"""
		vel = max(vel, SPEED_BOUNDS['lower_vel'])
		vel = min(vel, SPEED_BOUNDS['upper_vel'])
		acc = max(acc, SPEED_BOUNDS['lower_acc'])
		acc = min(acc, SPEED_BOUNDS['upper_acc'])
		return vel, acc

	def setSpeed(self, vel=100, acc=100):
		"""
		Written by Shu-Nong Wu
		Sets velocity and acceleration
		"""
		vel, acc = self._boundSpeed(vel,acc)
		self._dobot.setSpeed(vel,acc)