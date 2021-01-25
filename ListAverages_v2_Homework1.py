# this solution is to satisfy the following criteria: sort without using sort() and catch exceptions
import random # import random module to generate random numbers

# create a list
random_list = [] # start with empty random list
for n in range (0,100): # we need 100 elements in a list
    number = random.randint(0,1000) # generate random integer from 0 to 1000 for each n in range 0-100
    random_list.append(number) # add every random integer generated to the list

# sort the list created
for index in range(len(random_list)): # list has len(list) elements; we want to iterate through each element and compare it to others
    for compared_index in range(index + 1, len(random_list)): # compared index = position of all other elements starting from the next element
        if random_list[index] > random_list[compared_index]: # compare value of the index to the value of each next index
            random_list[index], random_list[compared_index] = random_list[compared_index], random_list[index] # if current value is greater than compared value assign their values to each other indexes (swap their positions in a list)

# identify even and odd values, calculate sum and count of each
odd_sum = odd_cnt = even_sum = even_cnt = 0 # start with declaring odd/even sum/count as 0
for value in random_list:
    if value % 2 == 0: # if remainder of dividing by 2 equals 0, then the value is even, otherwise - odd
        even_sum += value # add value to the sum of even values
        even_cnt += 1 # add 1 to count of even values
    else:
        odd_sum += value
        odd_cnt += 1

# calculate and print average even and odd value
try:
    even_avg = even_sum / even_cnt
    print (f"Average even number: {even_avg}")
except ZeroDivisionError: # to cover cases when even_cnt will be 0 and division will through an exception
    print ("Can not calculate average even number as there are no even values on the list")
try:
    odd_avg = odd_sum / odd_cnt
    print (f"Average odd number: {odd_avg}")
except ZeroDivisionError: # to cover cases when odd_cnt will be 0 and division will through an exception
    print ("Can not calculate average odd number as there are no odd values on the list")

