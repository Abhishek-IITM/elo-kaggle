from config import path
from services.field_to_features import field_to_features
from utils.log_setup import _log

_log.info("-----------------------------------------------------------------------------------------------------------")
_log.info("|                                     Running category feature maker                                      |")
_log.info("-----------------------------------------------------------------------------------------------------------")

_log.info("|                                    Running category 1 feature maker                                     |")
historical_cat1_features = field_to_features("historical_transactions.csv", "category_1")
historical_cat1_features.to_csv("{}/{}.csv".format(path.feature_path,"historical_cat1_features"))
del historical_cat1_features

_log.info("|                                    Running category 2 feature maker                                     |")
historical_cat2_features = field_to_features("historical_transactions.csv", "category_2")
historical_cat2_features.to_csv("{}/{}.csv".format(path.feature_path,"historical_cat2_features"))
del historical_cat2_features

_log.info("|                                    Running category 3 feature maker                                     |")
historical_cat3_features = field_to_features("historical_transactions.csv", "category_3")
historical_cat3_features.to_csv("{}/{}.csv".format(path.feature_path,"historical_cat3_features"))
del historical_cat3_features

_log.info("-----------------------------------------------------------------------------------------------------------")
_log.info("|                                 Successfully ran category feature maker                                 |")
_log.info("-----------------------------------------------------------------------------------------------------------")
