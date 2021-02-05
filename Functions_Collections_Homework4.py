from string import ascii_lowercase  # we will use it to generate keys as letters
from random import randint, choice  # we will use it to generate random integers for dictionary values and list length; choice will be used to select random letter for keys


# create new dicts where key = key from random list and value = list of values for this key
def values_to_list(my_list):
    flat_dict = {}
    for dct in my_list:
        for k in dct.keys():
            values_lst = [d[k] for d in my_list if k in d.keys()]
            new_dict = dict.fromkeys(k, values_lst)
            flat_dict.update(new_dict)
    return flat_dict


# find max value for each key and its occurrence
def find_max_value(my_dict, my_key):
    max_value, max_occurrence = my_dict[my_key][0], 1
    for i in range(len(my_dict[my_key])):
            if my_dict[my_key][i] > max_value:
                max_value = my_dict[my_key][i]
                max_occurrence = i + 1
    return max_value, max_occurrence


# put together final dict with max values for each key and renaming the key based on occurrence
def create_new_dict_and_rename(my_dict):
    final_dict = {}
    for key, values_list in my_dict.items():
        if len(values_list) == 1:
            final_dict[key] = values_list[0]
        else:
            max_value, max_position = find_max_value(my_dict, key)
            final_dict[key + '_' + str(max_position)] = max_value
    print(final_dict)


rand_lst = [{choice(ascii_lowercase): randint(0,100) for i in range(len(ascii_lowercase))} for j in range(randint(2,10))]  # list of random dicts

if __name__ == '__main__':
    temp_dict = values_to_list(rand_lst)
    create_new_dict_and_rename(temp_dict)
