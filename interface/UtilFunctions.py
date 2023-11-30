from copy import deepcopy
# aka i have no idea where to put these
def pad_or_truncate(some_list, target_len, default):
    while(len(some_list) < target_len):
        obj = deepcopy(default)
        obj.internal_id = len(some_list) + 1
        some_list.append(obj)
    while(len(some_list) > target_len):
        del some_list[-1]