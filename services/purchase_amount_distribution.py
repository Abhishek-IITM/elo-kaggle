import pandas as pd
from config import path
from utils.split_across_zero import count_greater_than_equal_to_zero, count_less_than_zero, \
    sum_greater_than_equal_to_zero, sum_less_than_zero
from utils.log_setup import _log
from utils.get_rename_dict_from_funcs import create_rename_dict


def get_purchase_amt_dist(source_df, field="purchase_amount", path=path.path, nrows=None):
    """
    Returns min,max and distribution of purchase amount greater than and less than zero
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

    _log.info("Computing distribution of purchase amount")
    func_to_be_applied = [count_greater_than_equal_to_zero, sum_greater_than_equal_to_zero, count_less_than_zero,
                          sum_less_than_zero, min, max]

    rename_dict = create_rename_dict(prefix, field, func_to_be_applied)

    _log.info(("Creating final df"))
    df_features = df.groupby("card_id").agg({field: func_to_be_applied}).reset_index()
    df_features = pd.concat([pd.DataFrame(df_features["card_id"]), df_features[field]], axis=1, sort=False)
    _log.info("Renaming columns: {}".format(rename_dict))
    df_features.rename(columns=rename_dict, inplace=True)

    return df_features
