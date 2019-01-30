from config import path
from services.purchase_date_df_gen import purchase_date_features_df_gen, get_avg_days_bw_purchases, \
    frequency_features_from_field
from services.field_to_features import field_to_features
from utils.log_setup import _log
_log.info("-----------------------------------------------------------------------------------------------------------")
_log.info("|                                 Running purchase date feature maker                                     |")
_log.info("-----------------------------------------------------------------------------------------------------------")
_log.info("Creating necessary columns to extract features from purchase_date param")
raw_file_name = purchase_date_features_df_gen("historical_transactions.csv")

_log.info("Computing {}, {}, {}".format("time_of_day_features", "day_of_week_features", "month_features"))
time_of_day_features = field_to_features(raw_file_name, "time_of_day", path=path.feature_path)
day_of_week_features = field_to_features(raw_file_name, "day_of_week", path=path.feature_path)
month_features = field_to_features(raw_file_name, "month", path=path.feature_path)

_log.info("Computing {}, {}".format("days_bw_purchase", "day_features"))
days_bw_purchase = get_avg_days_bw_purchases(raw_file_name)
day_features = frequency_features_from_field(raw_file_name)

purchase_date_features = (time_of_day_features.merge(day_of_week_features, on="card_id")
                          .merge(month_features, on="card_id")
                          .merge(day_features, on="card_id")
                          .merge(days_bw_purchase, on="card_id"))

output_file_path = "{}/{}_{}.csv".format(path.feature_path, "historical", "purchase_date_features")
_log.info("Writing to {}".format(output_file_path))
purchase_date_features.to_csv(output_file_path)
_log.info("-----------------------------------------------------------------------------------------------------------")
_log.info("|                               Successfully ran purchase date feature maker                              |")
_log.info("-----------------------------------------------------------------------------------------------------------")
#abhishek
