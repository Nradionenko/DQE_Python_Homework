import re

original_str = '''homEwork:

  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here? fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.'''

# identify and insert last words from each sentence
last_words = last_elements = ' '.join(re.findall(r'\w+(?=[.?!])', original_str)) + '.'  # create sentence consisting of words followed by ending characters
try:
    position_for_last_words = re.search('add it to the end of this paragraph', original_str.lower()).end() + 1  # search string position where new sentence should start
    temp_str1 = original_str[:position_for_last_words] + ' ' + last_words + original_str[position_for_last_words:]
except AttributeError:
    print("ERROR ENCOUNTERED: Can't identify the place where to insert last words sentence. New sentence not inserted. \n\n\n")
    temp_str1 = original_str

# fix spelling in new text
temp_str2 = re.sub(rf'(?<!\S)(\biz\b)(?!\S)', "is", temp_str1, flags = re.I)  # replace "iz" with "is" when its not surrounded by any non-whitespace characters

# capitalize
first_words_pattern = re.compile(r"(^|[?!.]\s+|\s{2,})(\S+)")  # find words preceded by ?!. and whitespaces OR by >= whitespaces (=paragraph)
normalized_str = re.sub(first_words_pattern, lambda x: x.group(1) + x.group(2).capitalize(), temp_str2.lower())  # first lower the string with fixed spelling; replace first words with their capitalized form + preceding characters

# count whitespaces in normalized string
cnt_whitespaces = 0 # declare count of whitespaces as 0. We'll add to it iteratively
for character in normalized_str: # check each character in generated normalized string
    if character.isspace() is True: # check if this character is whitespace
        cnt_whitespaces += 1 # if this character is whitespace, add 1 to the count of whitespaces

print(normalized_str)
print(f"\n\n\n\n  I've got {cnt_whitespaces} whitespaces in the normalized string.")
