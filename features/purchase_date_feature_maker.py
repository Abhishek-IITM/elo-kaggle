import datetime as dt
import pandas as pd
import numpy as np
from config import path
import os
from utils import time_fragments, dtypes_specifier
os.chdir(path.path)

id_purchase_date = pd.read_csv("historical_transactions.csv", usecols=["card_id", "purchase_date"],
                               dtype=dtypes_specifier.dtypes, parse_dates=dtypes_specifier.parse_dates)

id_purchase_date["dummy"] = 1
id_purchase_date["time_of_day"] = id_purchase_date["purchase_date"].apply(time_fragments.time_of_day_fragment)
id_purchase_date["day_of_week"] = id_purchase_date["purchase_date"].apply(time_fragments.day_of_week)
id_purchase_date["month"] = id_purchase_date["purchase_date"].apply(time_fragments.month_from_date)
id_purchase_date["date"] = id_purchase_date["purchase_date"].apply(lambda x: x.date())


def feature_by_field(field):
    """
    :param field:field from id_purchase_date to be used for making feature
    :return: df with no. of transacting periods(whether its time of day, or specific month of year or day of week)
    """
    keys = pd.Series(list(set(id_purchase_date[field])))
    vals = keys.apply(lambda x: "{}_{}".format(field,x))
    rename_dict = dict(zip(keys,vals))
    field_features = (id_purchase_date.groupby(["card_id", field]).agg({"dummy":np.sum}).reset_index()
                          .pivot_table(columns=field, index="card_id",values="dummy", fill_value=0)
                          .reset_index()
                          .rename(columns=rename_dict))
    return field_features


time_of_day_features = feature_by_field("time_of_day")
day_of_week_features = feature_by_field("day_of_week")
month_features = feature_by_field("month")

day_features = (id_purchase_date.groupby(["card_id", "date"]).agg({"dummy":np.sum}).reset_index()
               .groupby(["card_id"]).agg({"dummy":[np.max, np.mean]}).reset_index())
day_features = (pd.DataFrame([day_features["card_id"], day_features["dummy"]["amax"], day_features["dummy"]["mean"]])
                .T.rename(columns={"amax":"max_freq_in_day", "mean":"avg_freq_in_transacting_day"}))

id_purchase_date["next_purchase_date"] = id_purchase_date.groupby("card_id").shift(-1)["purchase_date"]
id_purchase_date.loc[pd.isnull(id_purchase_date["next_purchase_date"]), "next_purchase_date"] = dt.datetime.now() # should be a better value
id_purchase_date["days_between_purchases"] = id_purchase_date["next_purchase_date"] - id_purchase_date["purchase_date"]
id_purchase_date["days_between_purchases"] = id_purchase_date["days_between_purchases"].apply(lambda x: x.days)
days_bw_purchase = (id_purchase_date.groupby("card_id").agg({"days_between_purchases":np.mean}).reset_index()
                    .rename({"mean":"avg_days_bw_purchases"}))

purchase_date_features = (time_of_day_features.merge(day_of_week_features, on = "card_id")
                         .merge(month_features, on = "card_id")
                         .merge(day_features, on = "card_id")
                         .merge(days_bw_purchase, on="card_id"))

purchase_date_features.to_csv("{}/{}.csv".format(path.feature_path,"purchase_date_features"))