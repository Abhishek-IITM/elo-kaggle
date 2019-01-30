import pandas as pd
import numpy as np
from config import path
from utils.log_setup import _log


def get_unique_count_and_mode(source_df, field, path=path.path, nrows=None):
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

    if sum(pd.isnull(df[field])):
        field_mode = df[field].mode()[0]
        df.loc[pd.isnull(df[field]), field] = field_mode

    _log.info("Fetching no. of distinct merchants transacted on")
    df_uniq = df.groupby("card_id").agg({field: pd.Series.nunique}).reset_index().rename(columns={field: "{}_{}_{}".format(prefix, "unique", field)})

    _log.info("Computing mode of merchants")
    df_agg = df.groupby(["card_id", field]).agg({field: np.count_nonzero}).rename(columns={field: "count"}).reset_index()
    df_max = df_agg.groupby("card_id").agg({"count": np.max}).reset_index()
    df_max = df_agg.merge(df_max, how="inner", on=["card_id", "count"]).drop_duplicates().reset_index(drop=True)
    df_max['rank'] = df_max.groupby(['card_id']).cumcount() + 1
    df_max = df_max[df_max['rank'] == 1]
    df = df_max.merge(df_uniq, on="card_id", how="inner")
    df.rename(columns={"count":"{}_{}_{}".format(prefix, "max_count", field)}, inplace=True)

    _log.info("Succesfully computed mode and levels for {}".format(field))
    return df

