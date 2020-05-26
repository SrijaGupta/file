from itertools import product
import itertools
#import yaml

#f = open('sample_data_file.yaml')
#dict1 = f.read()

#enums_dict = yaml.load(dict1)


def gen_valid(thing, positive="valid", negative=None):

    """
    CAT -> Revised function to generate combinations for the data file with data segregation as "valid", "negative" etc.
    CAT -> This is the main function, but this function generates combinations only within the valid pool
    CAT -> Other functions like invalid, explore etc uses this function and generate hybrid of valid and the respective pool
    """

    if isinstance(thing, dict):  # if dictionary, distinguish between two types of dictionary
        if positive in thing:
            if negative is None:
                return thing[positive]  # here it's OK if it's empty
            elif thing[positive]:  # here it's not OK if it's empty
                return [random.choice(thing[positive])] + thing[negative]
            else:
                return []
        else:
            results = []
            for key, value in thing.items():  # generate all possible key: value combinations
                results.append([(key, result) for result in gen_valid(value, positive, negative)])
            return [dict(result) for result in itertools.product(*results)]

    elif isinstance(thing, (list, tuple)):  # added tuple just to be safe (thanks Padraic!)
        # generate recursive result sets for each element of list
        results = [gen_valid(element, positive, negative) for element in thing]
        return [list(result) for result in itertools.product(*results)]

    else:  # not a type we know how to handle
        raise TypeError("Unexpected type")


def str_of_code(d):
    k, v = list(d.items())[0]
    kwargs = {}
    for k2, v2 in v.items():
        if isinstance(v2, dict):
            kwargs[k2] = str_of_code(v2)
        elif isinstance(v2, list):
            res=[]
            for v3 in v2:
                if isinstance(v3, dict):
                    res.append(str_of_code(v3))
                else:
                    if type(v3) is str:
                        if "_cat_enum" not in k2:  # CAT -> If enum, double quote is not required and hence filtered from enclosing in double quotes
                            v3 = "\"" + v3 + "\""  # CAT -> Added to treat string as string by enclosing within double quotes. Note : repr(v3) can retain single quotes
                    res.append(str(v3))
            kwargs[k2] = '[{}]'.format(', '.join(str(res1) for res1 in res))
        else:
            if type(v2) is str:
                if "_cat_enum" not in k2:
                    v2 = "\"" + v2 + "\""
            kwargs[k2] = str(v2)
    return '{}({})'.format(k, ', '.join('{}={}'.format(*i) for i in kwargs.items()))


def clean_dict(d):
    """  CAT -> If Any dict or list is empty till its leaf, this function takes care of removing the complete hierarchy that is null """
    ret = {}
    for key, val in d.items():
        if isinstance(val, list):  # CAT -> This "if" handles list of dicts
            val = clean_list(val)
            if len(val) > 0:
                ret[key] = val
        elif isinstance(val, dict):
            if "valid" and "negative" and "boundary" and "explore" in val.keys():  # CAT -> This "if" is introduced to handle data segregation. Just remove this if to rollback.
                if any(len(val[i]) for i in val.keys()) > 0:
                    ret[key] = val
            else:
                val = clean_dict(val)
                if len(val) > 0:
                    ret[key] = val
    return ret


def clean_list(l):
    """  CAT -> Sub function called by clean_dict to handle list of dicts """
    ret = []
    for elem in l:

        try:
            iter(elem)  # raise TypeError if not iterable
            if isinstance(elem, dict):
                if "valid" and "negative" and "boundary" and "explore" in elem.keys():
                    if any(len(elem[i]) for i in elem.keys()) > 0:
                        ret.append(elem)
                else:
                    elem = clean_dict(elem)
                    if len(elem) > 0:
                        ret.append(elem)
            elif isinstance(elem, list):
                elem = clean_list(elem)
                if len(elem) > 0:
                    ret.append(elem)
            else:
                ret.append(elem)
        except TypeError:  # elem is not an iterable
            ret.append(elem)
    return ret


def split_oneof(d):
    """
    CAT -> This is one major function that read the data file and split the initial combinations for oneofs and also removes the key "Oneof" and map the dicts to the actual values.
    CAT -> Eg: If oneof contains two variables and if user fill even a single data for both, that results in two function calls each with one "Oneof"
    CAT -> if sample_dict = {'a':1, 'Oneof':{'b':2, 'c':3}, 'e':{'Oneof':{'f':5, 'g':6}} } => {'a': 1, 'c': 3, 'e': {'g': 6}}, {'a': 1, 'c': 3, 'e': {'f': 5}}, {'a': 1, 'b': 2, 'e': {'g': 6}}, {'a': 1, 'b': 2, 'e': {'f': 5}}
    """
    to_product = []  # [[('a', 1)], [('b', 2), ('c', 3)], ...]
    for k, v in d.items():
        if k == 'Oneof':
            to_product.append([(k2, v2)
                              for d2 in split_oneof(v)
                              for k2, v2 in d2.items()])
        elif isinstance(v, list) and all(isinstance(i, dict) for i in v):  # CAT -> This elif is to handle list of dicts specially.
            c = product(*list(split_oneof(i) for i in v))
            to_product.append([(k, list(l)) for l in c])
        elif isinstance(v, dict):
            to_product.append([(k, d2) for d2 in split_oneof(v)])
        else:
            to_product.append([(k, v)])
    lst = [dict(l) for l in product(*to_product)]
    unique = []
    [unique.append(item) for item in lst if item not in unique]
    return unique
