from config import path
from services.purchase_amount_distribution import get_purchase_amt_dist
from utils.log_setup import _log

_log.info("-----------------------------------------------------------------------------------------------------------")
_log.info("|                               Running purchase amount feature maker                                     |")
_log.info("-----------------------------------------------------------------------------------------------------------")

historical_purchase_amount_features = get_purchase_amt_dist("historical_transactions.csv")

output_file_path = "{}/{}_{}.csv".format(path.feature_path, "historical", "purchase_amount_features")
_log.info("Writing to {}".format(output_file_path))
historical_purchase_amount_features.to_csv(output_file_path)

_log.info("-----------------------------------------------------------------------------------------------------------")
_log.info("|                             Successfully ran purchase amount feature maker                              |")
_log.info("-----------------------------------------------------------------------------------------------------------")
