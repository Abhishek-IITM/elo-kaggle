from config import path
from services.lag_distribution import month_lag_distribution
from utils.log_setup import _log

_log.info("-----------------------------------------------------------------------------------------------------------")
_log.info("|                                  Running month lag feature maker                                        |")
_log.info("-----------------------------------------------------------------------------------------------------------")

new_month_lag_features = month_lag_distribution("new_merchant_transactions.csv")

output_file_path = "{}/{}_{}.csv".format(path.feature_path, "new", "month_lag_features")
_log.info("Writing to {}".format(output_file_path))
new_month_lag_features.to_csv(output_file_path)

_log.info("-----------------------------------------------------------------------------------------------------------")
_log.info("|                                Successfully ran month lag feature maker                                 |")
_log.info("-----------------------------------------------------------------------------------------------------------")
