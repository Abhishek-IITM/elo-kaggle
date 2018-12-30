import pandas as pd
import numpy as np
from config import path
from utils.log_setup import _log
from utils.get_rename_dict_from_funcs import create_rename_dict


def month_lag_distribution(source_df, field="month_lag", path=path.path, nrows=None):
    """
        Returns min,max and count unique values of month_lag
            :param source_df: historical/new transactions
            :param field: feature to be extracted from
            :param path: path of source df
            :param nrows: no. of rows to be read
            :return: df with unique levels count and mode
        :return: df with card wise purchase amount details
        """
    _log.info("Creating features from {}".format(field))
    prefix = source_df.split("_")[0]
    source_df = "{}/{}".format(path, source_df)

    _log.info("Reading from {}".format(source_df))
    try:
        df = pd.read_csv(source_df, usecols=["card_id", field], nrows=nrows)
        _log.info("Successfully read from {}".format(source_df))
    except Exception as e:
        _log.exception(e)

    _log.info("Computing distribution of month lag")
    func_to_be_applied = [min, max, pd.Series.nunique]
    func_to_be_applied_dummy = [max, np.mean]
    rename_dict = create_rename_dict(prefix, field, func_to_be_applied)
    rename_dict_dummy = create_rename_dict(prefix, "dummy", func_to_be_applied_dummy)

    df["dummy"] = 1
    df_features = df.groupby("card_id").agg({field:func_to_be_applied}).reset_index()
    df_features = pd.concat([pd.DataFrame(df_features["card_id"]), df_features[field]], axis=1, sort=False)

    _log.info("Renaming columns: {}".format(rename_dict))
    df_features.rename(columns=rename_dict, inplace=True)

    _log.info("Computing time in month between transactions")
    df_freq = (df.groupby(["card_id", field]).agg({"dummy": np.sum}).reset_index().groupby("card_id")
               .agg({"dummy": func_to_be_applied_dummy}).reset_index())
    df_freq = pd.concat([pd.DataFrame(df_freq["card_id"]), df_freq["dummy"]], axis=1, sort=False)
    df_freq.rename(columns=rename_dict_dummy, inplace=True)

    _log.info("Creating final df")
    df_features = df_features.merge(df_freq, how="inner", on="card_id")
    return df_features
