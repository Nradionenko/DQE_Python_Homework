import random
from statistics import mean

random_list = sorted([random.randint(0,1000) for n in range (0,100)]) # create and sort the list of 100 random integers between 0 and 1000 using list comprehension
even_mean = mean([value for value in random_list if value % 2 == 0]) # apply mean function to list of even numbers from randomlist. Even number is identified as the one that returns 0 remainder when divided by 2
odd_mean = mean([value for value in random_list if value % 2 != 0]) # apply mean function to list of odd numbers from randomlist. Odd number is identified as the one that returns <> 0 remainder when divided by 2

print (f"Average odd value: {odd_mean},\nAverage even value: {even_mean}.") #average values

## ALTERNATIVE SOLUTION (with loops instead of list comprehensions and statistical functions)
#
# random_list = [] ## start with empty random list
# for n in range (0,100):
#     number = random.randint(0,1000)
#     random_list.append(number) ## add every random integer in the range from 0 to 1000 to the list until it's the 100th element in the list
#
# random_list.sort() ## sort created random list from min to max: sorting is ascending by default

# to calculate average odd and even value we want to identify the number of such values (oddlen = count of odd number, evenlen - count of even numbers) and their totals (oddsum, evensum)
# start with assigning 0 to all these aggregations
# odd_len = odd_sum = even_len = even_sum = 0
#
# for value in random_list:
#     if value % 2 == 0: ## idenfify even numbers
#         even_len += 1 ## add 1 to count of even numbers every time even number is found by loop
#         even_sum += value ## add even number to sum of even numbers every time even number is found by loop
#     else:
#         odd_len += 1
#         odd_sum += value
# odd_mean = odd_sum/odd_len
# even_mean = even_sum/even_len
#
# print (f"Average of odd values: {odd_mean},\nAverage of even values: {even_mean}.")
