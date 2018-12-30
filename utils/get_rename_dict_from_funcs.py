def create_rename_dict(prefix, field, func_to_be_applied):

    keys, vals = [],[]
    for func in func_to_be_applied:
        func_name = func.__name__
        keys.append(func_name)
        vals.append("{}_{}_{}".format(prefix, field, func_name))
    rename_dict = dict(zip(keys, vals))
    return rename_dict
