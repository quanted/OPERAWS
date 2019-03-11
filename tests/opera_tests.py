import unittest
import datetime

class TestOpera(unittest.TestCase):
	"""
	Unit test class for OPERAWS and OPERA CLI.
	"""

	print("opera unittests conducted at " + str(datetime.datetime.today()))

	def setUp(self):
		"""
		Setup routine for Kabam unit tests.
		:return:
		"""
		# Sets up runtime environment:
		# runtime_env = DeployEnv()
		# runtime_env.load_deployment_environment()
		pass

	def tearDown(self):
		"""
		Teardown routine for Kabam unit tests.
		:return:
		"""
		pass
		# teardown called after each test
		# e.g. maybe write test results to some text file