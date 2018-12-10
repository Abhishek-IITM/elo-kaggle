import pandas as pd
import numpy as np
from config import path
from utils import  dtypes_specifier
import os

os.chdir(path.path)

id_auth_flag = pd.read_csv("historical_transactions.csv", dtype=dtypes_specifier.dtypes,
                           usecols=["card_id", "authorized_flag"])

id_auth_flag["dummy"] = 1
id_auth_agg = (id_auth_flag.groupby(["authorized_flag", "card_id"]).agg({"dummy":np.sum}).reset_index()
               .pivot_table(index="card_id", columns="authorized_flag", values="dummy"))
id_auth_agg["total"] = id_auth_agg['N']+id_auth_agg['Y']
id_auth_agg['Y'] = id_auth_agg['Y']/id_auth_agg["total"]
id_auth_agg.drop(columns=["N", "total"], inplace=True)

id_auth_agg.to_csv("{}/{}.csv".format(path.feature_path,"auth_flag_features"))