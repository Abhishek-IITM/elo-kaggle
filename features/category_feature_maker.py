import pandas as pd

from config import path
from services.field_to_features import field_to_features

historical_cat1_features = field_to_features("historical_transactions.csv", "category_1")
historical_cat2_features = field_to_features("historical_transactions.csv", "category_2")
historical_cat3_features = field_to_features("historical_transactions.csv", "category_3")

historical_cat1_features.to_csv("{}/{}.csv".format(path.feature_path,"historical_cat1_features"))
historical_cat2_features.to_csv("{}/{}.csv".format(path.feature_path,"historical_cat2_features"))
historical_cat3_features.to_csv("{}/{}.csv".format(path.feature_path,"historical_cat3_features"))