from config import path
from services.field_to_features import field_to_features
from utils.log_setup import _log

_log.info("-----------------------------------------------------------------------------------------------------------")
_log.info("|                                     Running category feature maker                                      |")
_log.info("-----------------------------------------------------------------------------------------------------------")

_log.info("|                                    Running category 1 feature maker                                     |")
new_cat1_features = field_to_features("new_merchant_transactions.csv", "category_1")
new_cat1_features.to_csv("{}/{}.csv".format(path.feature_path,"new_cat1_features"))
del new_cat1_features

_log.info("|                                    Running category 2 feature maker                                     |")
new_cat2_features = field_to_features("new_merchant_transactions.csv", "category_2")
new_cat2_features.to_csv("{}/{}.csv".format(path.feature_path,"new_cat2_features"))
del new_cat2_features

_log.info("|                                    Running category 3 feature maker                                     |")
new_cat3_features = field_to_features("new_merchant_transactions.csv", "category_3")
new_cat3_features.to_csv("{}/{}.csv".format(path.feature_path,"new_cat3_features"))
del new_cat3_features

_log.info("-----------------------------------------------------------------------------------------------------------")
_log.info("|                                 Successfully ran category feature maker                                 |")
_log.info("-----------------------------------------------------------------------------------------------------------")
