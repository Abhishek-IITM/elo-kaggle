import pandas as pd
import numpy as np
import os
import path

os.chdir(path.path)

id_month = pd.read_csv("historical_transactions.csv", usecols=["card_id", "month_lag"])
id_month["dummy"] = 1

month_lag_features = (id_month.groupby("card_id").agg({"month_lag": [np.min, np.max, pd.Series.nunique]})
                      .reset_index())
month_lag_features = pd.DataFrame([month_lag_features["card_id"], month_lag_features["month_lag"]["amin"],
                                   month_lag_features["month_lag"]["amax"],
                                   month_lag_features["month_lag"]["nunique"]]).T
month_lag_features.rename(columns={"amin":"min_month_lag", "amax":"max_month_lag",
                                   "nunique":"unique_transacted_months"},inplace=True)


monthly_freq = (id_month.groupby(["card_id", "month_lag"]).agg({"dummy":np.sum}).reset_index().groupby("card_id")
                .agg({"dummy":[np.max, np.mean]}).reset_index())
monthly_freq = pd.DataFrame([monthly_freq["card_id"], monthly_freq["dummy"]["amax"], monthly_freq["dummy"]["mean"]]).T
monthly_freq.rename(columns={"amax":"max_monthly_freq", "mean":"mean_monthly_freq"}, inplace=True)


month_lag_features = month_lag_features.merge(monthly_freq, how="inner", on="card_id")

month_lag_features.to_csv("{}/{}.csv".format(path.feature_path,"month_lag_features"))
del monthly_freq