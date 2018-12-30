import pandas as pd

def count_greater_than_equal_to_zero(x):
    x = pd.Series(x)
    return sum(x>=0)

def count_less_than_zero(x):
    return sum(pd.Series(x)<0)

def sum_greater_than_equal_to_zero(x):
    x = pd.Series(x)
    return sum(x[x >= 0])

def sum_less_than_zero(x):
    x = pd.Series(x)
    return sum(x[x < 0])
