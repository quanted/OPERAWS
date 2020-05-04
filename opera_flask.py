from flask import Flask, request, jsonify
import os
import time
import logging

# Local imports:
from opera_cli import OPERACLI

app = Flask(__name__)
app.config.update(
	DEBUG=True
)

# PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
# os.environ.update({
# 	'PROJECT_ROOT': PROJECT_ROOT
# })
logging.basicConfig(level=logging.DEBUG)

###################
# FLASK ENDPOINTS #
###################

@app.route("/opera")
def test_page():
	pass

@app.route("/opera/test")
def test_opera():
	return jsonify({"status": "opera_flask up and running."})

@app.route("/opera/rest")
def rest_endpoints():
	pass

@app.route("/opera/rest/run", methods=["POST"])
def run_opera():
	"""
	Runs opera_cli.py module for all OPERA properties.
	Currently: reads in single 'smiles' key, returns all properties.
	"""
	post_dict = request.get_json()
	requested_smiles = post_dict['smiles']
	if not isinstance(requested_smiles, list):
		requested_smiles = [requested_smiles]
	logging.info("Starting OPERA CLI routine.")
	start_time = time.time()
	opera_results = OPERACLI().run_opera_routine(requested_smiles)  # opera_cli expecting list of smiles
	logging.info("Returning OPERA CLI results.")
	return jsonify({
		"status": True,
		"data": opera_results,
		"meta": {
			"exec_time": round(time.time() - start_time, 1),
			"exec_units": "seconds"
		}
	})

if __name__ == '__main__':
	app.run(debug=True)