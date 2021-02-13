from string import ascii_lowercase  # we will use it to generate keys as letters
from random import randint, choice  # we will use it to generate random integers for dictionary values and list length; choice will be used to select random letter for keys


def rand_list(min_int, max_int, min_count, max_count):
    """Generate list of dictionaries, where:
    dict key = random letter
    dict value = random integer from min_int to max_int
    number of list elements is random value from min_count to max_count
    """
    rand_lst = [{choice(ascii_lowercase): randint(min_int, max_int) for i in range(len(ascii_lowercase))} for j in range(randint(min_count, max_count))]
    return rand_lst


def values_to_list(my_list):
    """Create new dict where key = key from random list and value = list of values for this key"""
    flat_dict = {}
    for dct in my_list:
        for k in dct.keys():
            values_lst = [d[k] for d in my_list if k in d.keys()]
            new_dict = dict.fromkeys(k, values_lst)
            flat_dict.update(new_dict)
    return flat_dict


def find_max_value(my_list):
    """Find max value and its occurrence within the list"""
    max_value, max_occurrence = my_list[0], 1
    for i in range(len(my_list)):
        if my_list[i] > max_value:
            max_value = my_list[i]
            max_occurrence = i + 1
    return max_value, max_occurrence


def create_new_dict_and_rename(my_dict):
    """Put together final dict with max values for each key and renaming the key based on occurrence"""
    final_dict = {}
    for key, values_list in my_dict.items():
        if len(values_list) == 1:
            final_dict[key] = values_list[0]
        else:
            max_value, max_position = find_max_value(values_list)
            final_dict[key + '_' + str(max_position)] = max_value
    print(final_dict)


if __name__ == '__main__':
    rand_lst = rand_list(0, 100, 2, 10)
    temp_dict = values_to_list(rand_lst)
    create_new_dict_and_rename(temp_dict)
