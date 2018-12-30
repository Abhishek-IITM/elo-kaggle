import pandas as pd
import numpy as np
from config import path
from utils.log_setup import _log
from utils import dtypes_specifier
import os

def auth_flag_features(source_df, field, path=path.path, nrows=None):
    """
        Returns number of levels and mode for a given field
        :param source_df: historical/new transactions
        :param field: feature to be extracted from
        :param path: path of source df
        :param nrows: no. of rows to be read
        :return: df with unique levels count and mode
        """
    _log.info("Creating features from {}".format(field))
    prefix = source_df.split("_")[0]

    source_df = "{}/{}".format(path, source_df)
    _log.info("Reading from {}".format(source_df))
    try:
        df = pd.read_csv(source_df, usecols=["card_id", field], nrows=nrows)
    except Exception as e:
        _log.exception(e)
    _log.info("Successfully read from {}".format(source_df))

    df["dummy"] = 1

    _log.info("Computing successful and unsuccesful authorizations")
    df_agg = (df.groupby([field, "card_id"]).agg({"dummy": np.sum}).reset_index()
              .pivot_table(index="card_id", columns=field, values="dummy"))
    df_agg["total"] = df_agg['N'] + df_agg['Y']
    df_agg['Y'] = df_agg['Y'] / df_agg["total"]
    df_agg.drop(columns=["N", "total"], inplace=True)
    df_agg.rename(columns={'Y':(prefix+'_Y')}, inplace=True)
    _log.info("Succesfully computed features for {}".format(field))

    return df_agg
