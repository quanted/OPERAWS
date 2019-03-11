import logging
import csv
import os

class OPERAResults:
	"""
	Handles OPERA prediction CSV results.
	"""
	def __init__(self):
		# Predictions csv result keys (Note: without running nearest neighbor option):
		self.result_keys = ["MoleculeID", "MolWeight", "nbAtoms", "nbHeavyAtoms", "nbC", "nbO",
			"nbN", "nbAromAtom", "nbRing", "nbHeteroRing", "Sp3Sp2HybRatio", "nbRotBd", "nbHBdAcc",
			"ndHBdDon", "nbLipinskiFailures", "TopoPolSurfAir", "MolarRefract", "CombDipolPolariz",
			"LogP_pred", "AD_LogP", "AD_index_LogP", "Conf_index_LogP", "MP_pred", "AD_MP",
			"AD_index_MP", "Conf_index_MP", "BP_pred", "AD_BP", "AD_index_BP", "Conf_index_BP",
			"LogVP_pred", "AD_VP", "AD_index_VP", "Conf_index_VP", "LogWS_pred", "AD_WS", "AD_index_WS",
			"Conf_index_WS", "LogHL_pred", "AD_HL", "AD_index_HL", "Conf_index_HL", "RT_pred", "AD_RT",
			"AD_index_RT", "Conf_index_RT", "LogKOA_pred", "AD_KOA", "AD_index_KOA", "Conf_index_KOA",
			"ionization", "pKa_a_pred", "pKa_b_pred", "AD_pKa", "AD_index_pKa", "Conf_index_pKa",
			"LogD55_pred", "LogD74_pred", "AD_LogD", "AD_index_LogD", "Conf_index_LogD", "LogOH_pred",
			"AD_AOH", "AD_index_AOH", "Conf_index_AOH", "LogBCF_pred", "AD_BCF", "AD_index_BCF",
			"Conf_index_BCF", "BioDeg_LogHalfLife_pred", "AD_BioDeg", "AD_index_BioDeg",
			"Conf_index_BioDeg", "ReadyBiodeg_pred", "AD_ReadyBiodeg", "AD_index_ReadyBiodeg",
			"Conf_index_ReadyBiodeg", "LogKM_pred", "AD_KM", "AD_index_KM", "Conf_index_KM",
			"LogKoc_pred", "AD_LogKoc", "AD_index_LogKoc", "Conf_index_LogKoc", "CERAPP_Ago_pred",
			"AD_CERAPP_Ago", "AD_index_CERAPP_Ago", "Conf_index_CERAPP_Ago", "CERAPP_Anta_pred",
			"AD_CERAPP_Anta", "AD_index_CERAPP_Anta", "Conf_index_CERAPP_Anta", "CERAPP_Bind_pred",
			"AD_CERAPP_BinD", "AD_index_CERAPP_Bind", "Conf_index_CERAPP_Bind", "CoMPARA_Ago_pred",
			"AD_CoMPARA_Ago", "AD_index_CoMPARA_Ago", "Conf_index_CoMPARA_Ago", "CoMPARA_Anta_pred",
			"AD_CoMPARA_Anta", "AD_index_CoMPARA_Anta", "Conf_index_CoMPARA_Anta", "CoMPARA_Bind_pred",
			"AD_CoMPARA_BinD", "AD_index_CoMPARA_Bind", "Conf_index_CoMPARA_Bind", "CATMoS_VT_pred",
			"AD_VT", "AD_index_VT", "Conf_index_VT", "CATMoS_NT_pred", "AD_NT", "AD_index_NT",
			"Conf_index_NT", "CATMoS_EPA_pred", "AD_EPA", "AD_index_EPA", "Conf_index_EPA",
			"CATMoS_GHS_pred", "AD_GHS", "AD_index_GHS", "Conf_index_GHS", "CATMoS_LD50_pred",
			"AD_LD50", "AD_index_LD50", "Conf_index_LD50"]

		# Maps predictions keys with CTS keys:
		# TODO: Probably move this to CTS side (calculator_opera.py)!!!
		self.results_map = {
			'kow_no_ph': {
				'result_key': "LogP_pred",  # is this correct?
				'methods': None
			},
			'melting_point': {
				'result_key': "MP_pred",
				'methods': None
			},
			'boiling_point': {
				'result_key': "BP_pred",
				'methods': None
			},
			'vapor_press': {
				'result_key': "LogVP_pred",
				'methods': None
			},
			'water_sol': {
				'result_key': "LogWS_pred",
				'methods': None
			},
			'ion_con': {
				'result_key': ["pKa_a_pred", "pKa_b_pred"],
				'methods': None
			},
			'kow_wph': {
				'result_key': ["LogD55_pred", "LogD74_pred"],
				'methods': None
			},
			'log_bcf': {
				'result_key': "LogBCF_pred",
				'methods': None
			},
			'koc': {
				'result_key': "LogKoc_pred",
				'methods': None
			}
		}

		# p-chem keys for CTS:
		self.cts_pchem_keys = ["LogP_pred", "MP_pred", "BP_pred", "LogVP_pred", "LogWS_pred", "pKa_a_pred",
			"pKa_b_pred", "LogD55_pred", "LogD74_pred", "LogBCF_pred", "LogKoc_pred"]


	def read_prediction_file(self, predictions_full_filename):
		"""
		Reads in prediction file that's created after
		OPERA runs.
		"""
		tempfile_obj = open(predictions_full_filename)
		return tempfile_obj

	def parse_csv_data_to_dict(self, prediction_file):
		"""
		Creates dict of predication data.
		"""
		csv_file = csv.DictReader(prediction_file)
		csv_data = []
		for row_dict in csv_file:
			csv_data.append(dict(row_dict))  # row per smiles
		return csv_data

	def curate_data_for_cts(self, prediction_data):
		"""
		Gets key:vals of predictions data for CTS.
		Returns smiles list of objects containing CTS-related property data.
		"""
		curated_list = []
		for smiles_data_obj in prediction_data:
			curated_dict = {}
			for result_key in self.cts_pchem_keys:
				if not result_key in list(smiles_data_obj.keys()):
					continue
				curated_dict[result_key] = smiles_data_obj[result_key]  # adds predictions that match CTS-requested keys
			curated_list.append(curated_dict)
		return curated_list

	def cleanup_tempfiles(self, *args):
		"""
		Closes and removes input and output temp files.
		"""
		for tempfile in args:
			tempfile.close()
			os.remove(tempfile.name)

	def get_predictions(self, predictions_full_filename):
		"""
		Routine that reads in prediction file, then converts
		it to a dictionary.
		"""
		try:
			prediction_file = self.read_prediction_file(predictions_full_filename)
			prediction_data = self.parse_csv_data_to_dict(prediction_file)
			# curated_data = self.curate_data_for_cts(prediction_data)
			self.cleanup_tempfiles(prediction_file)
			return prediction_data
			# return curated_data
		except Exception as e:
			logging.warning("Exception getting OPERA results: {}".format(e))
			self.cleanup_tempfiles(prediction_file)
			raise