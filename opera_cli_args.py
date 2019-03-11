"""
OPERA command line arguments.
Categorized by input, output, misc, and property endpoints.
"""

class InputArgs:
	"""
	OPERA CLI input arguments.
	"""
	def __init__(self):
		self.structure_file = {
			'arg': ["-s,", "--SDF", "--MOL", "--SMI"],
			'description': "Structure file containing the molecule(s) to be predicted. IDs will be assigned if the file does not contain molecule names. Molecular descriptors will be calculated using the PaDEL software."
		}
		self.descriptors = {
			'arg': ["-d", "--Descriptors"],
			'description': "pre-calculated PaDEL descriptors in csv file. If the first column is not 'Name' as the standard PaDEL output, molecule IDs will be assinged."
		}
		self.matlab_matrix_file = {
			'arg': ["-m", "--Mat", "--ascii"],
			'description': "Matlab matrix or ascii file containing PaDEL descriptors."
		}
		self.molecule_name = {
			'arg': ["-i", "--MolID"],
			'description': "Molecule names in csv file."
		}
		self.salt_id = {
			'arg': ["-t", "--SaltInfo"],
			'description': "Salt IDs to improve melting point predictions. List provided in Salts.xls."
		}
		self.descriptor_labels = {
			'arg': ["-l", "--Labels"],
			'description': "Descriptor labels. Necessary if the descriptor file does not contain labels or contains more than the 1444 PaDEL 2D descriptors."
		}

class OutputArgs:
	"""
	OPERA CLI output arguments.
	"""
	def __init__(self):
		self.output_file = {
			'arg': "-o",  # or "--Output"
			'description': ""
		}
		self.nearest_neighbors = {
			'arg': "-n",  # or "--Neighbors"
			'description': ""
		}
		self.output_file_detailed = {
			'arg': "-O",  # or "--FullOutput"
			'description': ""
		}
		self.separate_files = {
			'arg': "-x",  # or "--Seperate"
			'description': ""
		}

class MiscArgs:
	"""
	OPERA CLI misc arguments.
	"""
	def __init__(self):
		self.verbose = {
			'arg': "-v",  # or "--Verbose"
			'description': ""
		}
		self.all_endpoints = {
			'arg': "-a",  # or "--All"
			'description': ""
		}
		self.clean_temp_files = {
			'arg': "-c",  # or "--Clean"
			'description': ""
		}
		self.help = {
			'arg': "-h",  # or "--Help"
			'description': "Display this help file and exit."
		}
		self.version = {
			'arg': "-V",  # or "--Version"
			'description': "Version of the application."
		}

class EndpointGroupsArgs:
	"""
	OPERA CLI args for running multiple properties at once.
	"""
	def __init__(self):
		self.structural_properties = {
			'arg': "StrP",
			'description': ""
		}
		self.pchem_properties = {
			'arg': "PC",  # or "Physchem"
			'description': ""
		}
		self.environmental_fate = {
			'arg': "EnvFate",  # or "EF"
			'description': ""
		}
		self.toxicology = {
			'arg': "Tox",
			'dexcription': "Runs ER, AR, and AcuteTox"
		}

class EndpointArgs(EndpointGroupsArgs):
	"""
	OPERA CLI endpoints for structural properties, p-chem properties,
	environmental fate, and toxicology.
	"""
	def __init__(self):
		EndpointGroupsArgs.__init__(self)
		self.log_bcf = {
			'arg': "logBCF",  # or "BCF"
			'description': ""
		}
		self.melting_point = {
			'arg': "MP",
			'description': ""
		}
		self.boiling_point = {
			'arg': "BP",
			'description': ""
		}
		self.logp = {
			'arg': "logP",
			'description': ""
		}
		self.vapor_pressure = {
			'arg': "VP",  # or "logVP"
			'description': ""
		}
		self.water_solubility = {
			'arg': "WS",
			'description': ""
		}
		self.aoh = {
			'arg': "AOH",
			'description': ""
		}
		self.biodeg = {
			'arg': "BioDeg",
			'description': ""
		}
		self.ready_biodeg = {
			'arg': "RB",  # or "ReadyBiodeg"
			'description': ""
		}
		self.hl = {
			'arg': "HL",  # or "logHL"
			'description': ""
		}
		self.km = {
			'arg': "KM",  # or "logKM"
			'description': ""
		}
		self.koa = {
			'arg': "KOA",
			'description': ""
		}
		self.koc = {
			'arg': "logKoc",  # or "Koc"
			'description': ""
		}
		self.rt = {
			'arg': "RT",
			'description': ""
		}
		self.pka = {
			'arg': "pKa",
			'description': ""
		}
		self.logd = {
			'arg': "logD",
			'description': ""
		}
		self.cerapp = {
			'arg': "CERAPP",  # or "ER"
			'description': ""
		}
		self.compara = {
			'arg': "CoMPARA",  # or "AR"
			'description': ""
		}
		self.catmos = {
			'arg': "CATMoS",  # or "AcuteTox"
		}

class CLIArgs(InputArgs, OutputArgs, MiscArgs, EndpointArgs):
	"""
	Main class that inherits all arg classes below.
	"""
	def __init__(self):
		InputArgs.__init__(self)
		OutputArgs.__init__(self)
		MiscArgs.__init__(self)
		EndpointArgs.__init__(self)

		# OPERA CLI endpoint args used for CTS:
		self.cts_endpoints = ["LogP", "MP", "BP", "VP", "WS", "pKa", "LogD", "LogBCF", "LogKoc"]