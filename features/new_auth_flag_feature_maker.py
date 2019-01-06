from config import path
from services.get_successful_auth_perc import auth_flag_features
from utils.log_setup import _log

new_auth_flag_features = auth_flag_features("new_merchant_transactions.csv", "authorized_flag")
output_file_path = "{}/{}_{}.csv".format(path.feature_path, "new", "new_auth_flag_features")
_log.info("Writing to {}".format(output_file_path))
new_auth_flag_features.to_csv(output_file_path)