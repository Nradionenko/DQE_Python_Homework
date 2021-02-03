import re

original_str = '''homEwork:

  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
  '''

sentences = re.split(r'[.?!]', original_str) # create a list consisting of sentences from original string
last_words = ' '.join([sentences[i].strip().split()[-1] for i in range(len(sentences)-1)]) # create list of last elements (=words) of each sentence and convert this list to string separated by spaces
normalized_str = '' # declare empty string: we'll add normalized text from original string here

for i in range(len(sentences)): # take each sentence
    if 'add it to the end of this paragraph' in sentences[i].lower(): # check if there is 'add it to this paragraph' phrase in the sentence
        sentences.insert(i+1, ' ' + last_words) # if there is, insert 'last words' string into the next element of the list with sentences
    first_word_match = re.compile(r'(?<=\s)\w+').search(sentences[i]) # in each sentence, find the first word preceded by space.  We need this to separate 'words' in sentence from preceding whitespaces (like multiple newlines in most cases)
    sliced_sentences = [sentences[i][:first_word_match.start()], sentences[i][first_word_match.start():]] # slice each sentence into 'words part' and 'everything else'
    for sub_str in sliced_sentences: # for each part of sliced sentence:
        if sub_str.isspace() is True: # if this part consists only of whitespaces
            normalized_str += sub_str # add this part as is to the normalized string
        else: # if this is 'words part' of the sentence
            normalized_str += re.sub(r"""(?<!\S)(\biz\b)(?!\S)""", 'is', sub_str, flags = re.I).capitalize() # replace 'iz' with 'is' if 'iz' is a separate word and is not surrounded by special characters, ignore cases. Capitalize this updated string and add it to normalized string
            if normalized_str[-1].isspace() is False: # check if the last character added to normalized string is whitespace:
                normalized_str += "." # if it's not whitespace (= we assume it's the end of the sentence then), add '.' to the normalized string.

cnt_whitespaces = 0 # declare count of whitespaces as 0. We'll add to it iteratively
for character in normalized_str: # check each character in generated normalized string
    if character.isspace() is True: # check if this character is whitespace
        cnt_whitespaces += 1 # if this character is whitespace, add 1 to the count of whitespaces

print(normalized_str)
print(f"\n\n\n\n  I've got {cnt_whitespaces} whitespaces in the updated string.")
