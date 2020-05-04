"""
Calling OPERA CLI from Python.
"""

import subprocess
import logging
import os
import tempfile
import uuid
import glob
import time
from opera_cli_args import CLIArgs
from opera_cli_results import OPERAResults

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
logging.info("PROJECT_ROOT: {}".format(PROJECT_ROOT))

OPERA_EXE_PATH = os.path.join("c:", os.sep, "Program Files", "OPERA", "application")
if os.environ.get('OPERA_EXE_PATH'):
	OPERA_EXE_PATH = os.environ.get('OPERA_EXE_PATH')
logging.info("OPERA_EXE_PATH: {}".format(OPERA_EXE_PATH))

IS_LINUX = False
if os.environ.get('IS_LINUX') == "True":
	IS_LINUX = True
logging.info("IS_LINUX: {}".format(IS_LINUX))

MATLAB_RUNTIME_PATH = "/usr/local/MATLAB/MATLAB_Runtime/v94"
if os.environ.get('MATLAB_RUNTIME_PATH'):
	MATLAB_RUNTIME_PATH = os.environ.get('MATLAB_RUNTIME_PATH')
logging.info("MATLAB_RUNTIME_PATH: {}".format(MATLAB_RUNTIME_PATH))

class OPERACLI(CLIArgs, OPERAResults):

	def __init__(self):
		CLIArgs.__init__(self)
		OPERAResults.__init__(self)
		self.cli_example_1 = "OPERA -s Sample_50.sdf -o predictions.csv -a -x -n -v 2"
		self.cli_example_2 = "opera -d Sample_50.csv -o predictions.txt -e logP BCF -v 1"
		self.opera_exe_location = OPERA_EXE_PATH
		self.matlab_path = MATLAB_RUNTIME_PATH
		self.smiles_file_location = PROJECT_ROOT
		self.predictions_file_location = PROJECT_ROOT
		self.smiles_full_path = ""  # full path and filename for smiles input file
		self.predictions_full_path = ""  # full path and filename for predictions csv output

	def execute_opera(self, smiles_filename, predictions_filename):
		"""
		Executes OPERA CLI.
		"""
		logging.warning("Executing OPERA.exe in Windows.")
		subprocess.run([os.path.join(self.opera_exe_location, "opera"),
			"-s", smiles_filename,  # sets input smiles file
			"-o", predictions_filename,  # sets output csv file
			# "-c",  # cleans temp files from calculations
			"-a"])  # gets all opera properties
			# "-e", "HL", "LogP", "MP", "BP", "LogVP", "LogWS", "pKa", "LogD", "LogBCF", "LogKoc"])

	def execute_opera_linux(self, smiles_filename, predictions_filename):
		"""
		Execute OPERA in linux docker container.
		"""
		logging.warning("Running linux subprocess.")
		subprocess.run(["sh", self.opera_exe_location,
			self.matlab_path,
			"-s", smiles_filename,  # sets input smiles file
			"-o", predictions_filename,  # sets output csv file
			"-a"])  # gets all opera properties
			# "-e", "HL", "LogP", "MP", "BP", "LogVP", "LogWS", "pKa", "LogD", "LogBCF", "LogKoc"])		

	def create_smiles_tempfile(self, smiles_list):
		"""
		Creates smiles file of molecules to be predicted.
		Inputs: smiles - list of SMILES.
		Outputs: smiles tempfile name.
		"""
		# tempfile_obj = open("temp/" + self.generate_filename() + ".smi", "w")
		tempfile_obj = open(os.path.join(PROJECT_ROOT, "temp", self.generate_filename() + ".smi"), "w")
		smiles_string = ""
		for smiles in smiles_list:
			smiles_string += smiles + "\n"
		smiles_string = smiles_string[:-1]  # trims trailing newline
		tempfile_obj.write(smiles_string)
		tempfile_obj.close()
		return tempfile_obj

	def generate_filename(self):
		"""
		Generates a universally unique identifier for temp filenames.
		"""
		return str(uuid.uuid4())

	def remove_temp_files(self, *args):
		"""
		Closes and removes input and output temp files.
		"""
		for tempfile in args:
			tempfile.close()
			os.remove(tempfile.name)

	def remove_all_temp_files(self):
		"""
		Removes all temp files.
		"""
		for file in glob.glob("temp/*"):
			os.remove(file)

	def run_opera_routine(self, smiles_list, props_list=None):
		"""
		Runs OPERA CLI routine.
		"""
		try:
			self.remove_all_temp_files()
			smiles_tempfile = self.create_smiles_tempfile(smiles_list)  # creates temp file for smiles
			self.smiles_full_path = smiles_tempfile.name
			self.predictions_full_path = os.path.join(PROJECT_ROOT, "temp", self.generate_filename() + ".csv")
			logging.info("Initiating OPERA CLI execution.")
			if IS_LINUX:
				self.execute_opera_linux(self.smiles_full_path, self.predictions_full_path)  # runs opera cli (linux)
			else:
				self.execute_opera(self.smiles_full_path, self.predictions_full_path)  # runs opera cli (windows, default)
			logging.info("Finished executing OPERA CLI.")
			predictions_data = self.get_predictions(self.predictions_full_path)  # gets predictions from .csv
			self.remove_temp_files(smiles_tempfile)
			return predictions_data
		except Exception as e:
			logging.warning("Exception running OPERA: {}".format(e))
			self.remove_temp_files(smiles_tempfile)
			pass