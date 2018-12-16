import pandas as pd
import numpy as np
from config import path
from utils.log_setup import _log


def field_to_features(source_df, field, path=path.path, nrows=None):
    """
    :param source_df: historical or new transactions.csv
    :param field:param to be used for making feature
    :param nrows: number of rows to be read
    :param path: path of source_df
    Reads selected field from data frame and
    :return: df with columns:
        card_id,
        column each for distinct levels  of field (giving count of txn),
        level with max txn
    """
    _log.info("Creating features from {}".format(field))
    prefix = source_df.split("_")[0]

    source_df = "{}/{}".format(path, source_df)
    _log.info("Reading from {}".format(source_df))
    try:
        df = pd.read_csv(source_df, usecols=["card_id", field], nrows=nrows)
    except Exception as e:
        _log.exception(e)

    keys = pd.Series(list(set(df[field])))
    vals = keys.apply(lambda x: "{}_{}_{}".format(prefix, field, x))
    rename_dict = dict(zip(keys, vals))
    _log.info("Rename dict: {}".format(rename_dict  ))
    df["dummy"] = 1
    df_agg = (df.groupby(["card_id", field]).agg({"dummy":np.sum}).reset_index()
              .pivot_table(index="card_id", columns=field, values="dummy", fill_value=0).reset_index())
    field_name = prefix+"_max_txn_"+str(field)
    df_agg[field_name] = df_agg.drop(columns="card_id").idxmax(axis=1)
    df_agg.rename(columns=rename_dict, inplace=True)
    _log.info("Successfully computed feature")
    return df_agg
