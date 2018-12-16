import pandas as pd
import numpy as np
from config import path
from utils import dtypes_specifier, time_fragments
import datetime as dt
from utils.log_setup import _log


def purchase_date_features_df_gen(source_df):
    """
    create preliminary cols to derive essential features
    :param source_df:historica;/new transactions
    :return: file name of csv with essential cols created
    """
    _log.info("Creating necessary columns for extracting purchase date features")
    prefix = source_df.split("_")[0]
    source_df = "{}/{}".format(path.path, source_df)
    _log.info("Reading from {}".format(source_df))
    try:
        df = pd.read_csv(source_df, usecols=["card_id", "purchase_date"],
                         dtype=dtypes_specifier.dtypes, parse_dates=dtypes_specifier.parse_dates)
    except Exception as e:
        _log.exception(e)

    _log.info("Creating feature: {}".format("time_of_day"))
    df["time_of_day"] = df["purchase_date"].apply(time_fragments.time_of_day_fragment)
    _log.info("Creating feature: {}".format("day_of_week"))
    df["day_of_week"] = df["purchase_date"].apply(time_fragments.day_of_week)
    _log.info("Creating feature: {}".format("month"))
    df["month"] = df["purchase_date"].apply(time_fragments.month_from_date)
    _log.info("Creating feature: {}".format("date"))
    df["date"] = df["purchase_date"].apply(lambda x: x.date())

    written_file_name = "{}_{}.csv".format(prefix, "purchase_date_features_raw")
    written_file = "{}/{}_{}.csv".format(path.feature_path, prefix, "purchase_date_features_raw")
    _log.info("Writing file {}".format(written_file))
    df.to_csv(written_file)
    _log.info("Process successfully completed")
    return written_file_name


def get_avg_days_bw_purchases(source_df):
    """
    Gives average days between two purchases for a given card id
    :param source_df: historical/new transactions csv with essential derived features. Refer to earlier function
    :return: df with features corresponding to days between purchases
    """
    _log.info("Computing average number of days between consecutive purchases")
    prefix = source_df.split("_")[0]
    source_df = "{}/{}".format(path.feature_path, source_df)
    _log.info("Reading from {}".format(source_df))
    try:
        df = pd.read_csv(source_df)
    except Exception as e:
        _log.exception(e)
    df["next_purchase_date"] = df.groupby("card_id").shift(-1)["purchase_date"]
    df.loc[pd.isnull(df["next_purchase_date"]), "next_purchase_date"] = dt.datetime.now()  # should be a better value
    df["purchase_date"] = pd.to_datetime(df["purchase_date"])
    df["next_purchase_date"] = pd.to_datetime(df["next_purchase_date"])
    df["days_between_purchases"] = df["next_purchase_date"] - df["purchase_date"]
    df["days_between_purchases"] = df["days_between_purchases"].apply(lambda x: x.days)
    days_bw_purchase = (df.groupby("card_id").agg({"days_between_purchases": np.mean}).reset_index()
                        .rename({"mean": "{}_{}".format(prefix, "avg_days_bw_purchases")}))
    _log.info("Successfully computed feature")
    return days_bw_purchase


def frequency_features_from_field(source_df):
    """
    Gives average number of transactions and max number of transactions in a day
    :param source_df: historical/new transactions csv with essential derived features. Refer to earlier function
    :return: df with features corresponding to transactions in a day
    """
    _log.info("Computing average and max frequency transactions in a day")
    prefix = source_df.split("_")[0]
    source_df = "{}/{}".format(path.feature_path, source_df)
    _log.info("Reading from {}".format(source_df))
    try:
        df = pd.read_csv(source_df)
    except Exception as e:
        _log.exception(e)
    df["dummy"] = 1
    day_features_rename_dict = {"amax": "{}_{}".format(prefix, "max_freq_in_day"),
                                "mean": "{}_{}".format(prefix, "avg_freq_in_transacting_day")}
    day_features = (df.groupby(["card_id", "date"]).agg({"dummy": np.sum}).reset_index()
                    .groupby(["card_id"]).agg({"dummy": [np.max, np.mean]}).reset_index())

    day_features = (pd.DataFrame([day_features["card_id"], day_features["dummy"]["amax"],
                                  day_features["dummy"]["mean"]]).T.rename(columns=day_features_rename_dict))
    _log.info("Successfully computed feature")
    return day_features
