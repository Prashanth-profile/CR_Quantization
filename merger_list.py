import itertools

def merge(lst1, lst2):
    return [sub[item] for item in range(len(lst2))
                      for sub in [lst1, lst2]]

def merge_offset(x, y, offset):
    sep, lst = offset, []
    for i in range(len(x) + 1):
        lst += x[i:i + 1] + y[i * sep:(i + 1) * sep]

    return lst