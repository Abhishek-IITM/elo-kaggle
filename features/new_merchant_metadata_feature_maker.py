from config import path
from services.distinct_levels_and_mode import get_unique_count_and_mode
from utils.log_setup import _log

_log.info("-----------------------------------------------------------------------------------------------------------")
_log.info("|                                Running merchant_metadata feature maker                                  |")
_log.info("-----------------------------------------------------------------------------------------------------------")

_log.info("Running new merchant_category_id feature maker")
new_merc_cat_id_features = get_unique_count_and_mode("new_merchant_transactions.csv", "merchant_category_id")
new_merc_cat_id_features.to_csv("{}/{}.csv".format(path.feature_path, "new_merc_cat_id_features"))
del new_merc_cat_id_features
_log.info("Completed new running merchant_category_id feature maker")

_log.info("Running new merchant_id feature maker")
new_merc_id_features = get_unique_count_and_mode("new_merchant_transactions.csv", "merchant_id")
new_merc_id_features.to_csv("{}/{}.csv".format(path.feature_path, "new_merc_id_features"))
del new_merc_id_features
_log.info("Completed new running merchant_id feature maker")

_log.info("Running new state_id feature maker")
new_state_id_features = get_unique_count_and_mode("new_merchant_transactions.csv", "state_id")
new_state_id_features.to_csv("{}/{}.csv".format(path.feature_path, "new_state_id_features"))
del new_state_id_features
_log.info("Completed new running state_id feature maker")

_log.info("Running new city_id feature maker")
new_city_id_features = get_unique_count_and_mode("new_merchant_transactions.csv", "city_id")
new_city_id_features.to_csv("{}/{}.csv".format(path.feature_path, "new_city_id_features"))
del new_city_id_features
_log.info("Completed new running city_id feature maker")

_log.info("Running new subsector_id feature maker")
new_subsector_id_features = get_unique_count_and_mode("new_merchant_transactions.csv", "subsector_id")
new_subsector_id_features.to_csv("{}/{}.csv".format(path.feature_path, "new_subsector_id_features"))
del new_subsector_id_features
_log.info("Completed new running subsector id feature maker")

_log.info("-----------------------------------------------------------------------------------------------------------")
_log.info("|                            Successfully ran merchant_metadata feature maker                             |")
_log.info("-----------------------------------------------------------------------------------------------------------")
