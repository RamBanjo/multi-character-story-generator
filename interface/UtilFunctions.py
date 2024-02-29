from copy import deepcopy
# aka i have no idea where to put these
def pad_or_truncate(some_list: list, target_len, default):
    while(len(some_list) < target_len):
        obj = deepcopy(default)
        some_list.append(obj)
    while(len(some_list) > target_len):
        del some_list[-1]
