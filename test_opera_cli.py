from opera_cli import OPERACLI

cli = OPERACLI()
print("Running opera.")
predictions = cli.run_opera_routine(["CCCC"])
print("Predictions: {}".format(predictions))