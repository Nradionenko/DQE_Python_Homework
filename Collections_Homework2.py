from string import ascii_lowercase  # we will use it to generate keys as letters
from random import randint, choice  # we will use it to generate random integers for dictionary values and list length; choice will be used to select random letter for keys

rand_lst = [{choice(ascii_lowercase): randint(0,100) for i in range(len(ascii_lowercase))} for j in range(randint(2,10))]  # list of random dicts
final_dict = {}  # start with empty dictionary to add max values and updated keys in each iteration
occurrence = {}  # we'll write key and dictionary sequence number where it occurred for the first time

for i in range(len(rand_lst)):  # take each index in the list
    for key in rand_lst[i].keys():  # take each key in dictionary of iterated list index (=dictionary)
        if key not in [key2[0] for key2 in final_dict.keys()]:  # check if key doesn't yet exist in final_dict (check by 1st symbol cause key might exist as a_1 etc)
            final_dict[key] = rand_lst[i][key]  # add value to final list with original key if didn't exist before
            occurrence[key] = 1  # write down key and 1 as value as its 1st occurrence
        else:  # if such key exists in final dictionary
            occurrence[key] += 1  # add 1 every time key occurs
            for key2 in list(final_dict):  # check each key in final list
                if key2[0] == key:  # if key in final dict starts with the same letter
                    if final_dict[key2] < rand_lst[i][key]:  # find matching key in final dict and check if its value is < than current iteration key value in rand dictionary
                        final_dict[key2] = rand_lst[i][key]  # if it's less, update this key value with the value from random list
                        final_dict[key + '_' + str(occurrence[key])] = final_dict.pop(key2)  # update key name adding occurrence number to the key letter
                    elif key2 == key:  # if value in final dictionary is greater than in current iteration AND key names are equal (meaning there hasn't been any value greater yet):
                        final_dict[key + '_' + str(occurrence[key]-1)] = final_dict.pop(key2)  # update the key name in final dict adding first occurrence number

# ALTERNATIVE: for defining dictionary sequence in list (not occurrence sequence)
# for i in range(len(rand_lst)):  # take each index in the list
#     for key in rand_lst[i].keys():  # take each key in dictionary of iterated list index (=dictionary)
#         if key not in [key2[0] for key2 in final_dict.keys()]:  # check if key doesn't yet exist in final_dict (check by 1st symbol cause key might exist as a_1 etc)
#             final_dict[key] = rand_lst[i][key]  # add value to final list with original key if didn't exist before
#             occurrence[key] = i + 1  # write down key and dictionary number where it first occurred (where 0 dict in list = 1st dict etc)
#         else:  # if such key exists in final dictionary
#             for key2 in list(final_dict):  # check each key in final list
#                 if key2[0] == key:  # if key in final starts with the same letter
#                     if final_dict[key2] < rand_lst[i][key]:  # find matching key in final dict and check if its value is < than current iteration key value in rand dictionary
#                         final_dict[key2] = rand_lst[i][key]  # if it's less, update this key value with the value from random list
#                         final_dict[key + '_' + str(i+1)] = final_dict.pop(key2)  # update key name adding dictionary sequence number to the key letter
#                     elif key2 == key:  # if value in final dictionary is greater than in current iteration AND key names are equal (meaning there hasn't been any value greater yet):
#                         final_dict[key + '_' + str(occurrence[key])] = final_dict.pop(key2)  # update the key in final name adding first occurrence number

print(f"Final dictionary: \n{final_dict}") # print final result




