from config import path
from services.distinct_levels_and_mode import get_unique_count_and_mode
from utils.log_setup import _log

_log.info("-----------------------------------------------------------------------------------------------------------")
_log.info("|                                Running merchant_metadata feature maker                                  |")
_log.info("-----------------------------------------------------------------------------------------------------------")

_log.info("Running merchant_category_id feature maker")
historical_merc_cat_id_features = get_unique_count_and_mode("historical_transactions.csv", "merchant_category_id")
historical_merc_cat_id_features.to_csv("{}/{}.csv".format(path.feature_path, "historical_merc_cat_id_features"))
del historical_merc_cat_id_features
_log.info("Completed running merchant_category_id feature maker")

_log.info("Running merchant_id feature maker")
historical_merc_id_features = get_unique_count_and_mode("historical_transactions.csv", "merchant_id")
historical_merc_id_features.to_csv("{}/{}.csv".format(path.feature_path, "historical_merc_id_features"))
del historical_merc_id_features
_log.info("Completed running merchant_id feature maker")

_log.info("Running state_id feature maker")
historical_state_id_features = get_unique_count_and_mode("historical_transactions.csv", "state_id")
historical_state_id_features.to_csv("{}/{}.csv".format(path.feature_path, "historical_state_id_features"))
del historical_state_id_features
_log.info("Completed running state_id feature maker")

_log.info("Running city_id feature maker")
historical_city_id_features = get_unique_count_and_mode("historical_transactions.csv", "city_id")
historical_city_id_features.to_csv("{}/{}.csv".format(path.feature_path, "historical_city_id_features"))
del historical_city_id_features
_log.info("Completed running city_id feature maker")

_log.info("Running subsector_id feature maker")
historical_subsector_id_features = get_unique_count_and_mode("historical_transactions.csv", "subsector_id")
historical_subsector_id_features.to_csv("{}/{}.csv".format(path.feature_path, "historical_subsector_id_features"))
del historical_subsector_id_features
_log.info("Completed running subsector_id feature maker")

_log.info("-----------------------------------------------------------------------------------------------------------")
_log.info("|                            Successfully ran merchant_metadata feature maker                             |")
_log.info("-----------------------------------------------------------------------------------------------------------")
