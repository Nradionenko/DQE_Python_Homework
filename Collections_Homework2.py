from string import ascii_lowercase # we will use it to generate keys as letters
from random import randint, choice # we will use it to generate random integer for dictionary values and list length; choice will be used to select random letter for keys

rand_lst = [{choice(ascii_lowercase): randint(0,100) for i in range(len(ascii_lowercase))} for j in range(randint(2,10))] # list of random dicts
final_dict = {} # start with empty dictionary to add max values and updated keys in each iteration

for i in range(len(rand_lst)): # take each index in the list
    for key in rand_lst[i].keys(): # take each key in dictionary of iterated list index (=dictionary)
        if key not in [key2[0] for key2 in final_dict.keys()]: # check if key doesn't yet exist in final_dict (check by 1st symbol cause key might exist as a_1 etc)
            final_dict[key] = rand_lst[i][key] # add value to final list with original key if didn't exist before
        else: # if such key exists in final dictionary
            for key2 in list(final_dict):
                if key2[0] == key and final_dict[key2] < rand_lst[i][key]: # find matching key in final dict and check if it's value is < than current iteration key value in rand dictionary
                    final_dict[key2] = rand_lst[i][key] # if it less, update this key value with the value from random list
                    final_dict[key + '_' + str(i)] = final_dict.pop(key2) # update key name adding index to he key letter

print(f"Final dictionary: \n{final_dict}") # print final result




