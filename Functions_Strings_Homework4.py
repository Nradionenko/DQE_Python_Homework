import re


# make sentence from the last words
def collect_last_words(strng):
    last_elements = ' '.join(re.findall(r'\w+(?=\.!?)', strng)) + '.'  # find all words in text preceded by ending characters (.?!) join them into sentence
    return last_elements


# add last words sentence to the text. Identify where to position new sentence by 'after words' parameter
def add_new_sentence(strng, after_words, new_words):
    position = re.search(after_words, strng.lower()).end() + 1  # search string position where new sentence should start
    new_string = strng[:position] + ' ' + new_words + strng[position:]  # split string into "before" and "after" position and insert new sentence between them
    return new_string


# fix spelling: replace "iz" with "is" whe is is a separate word not surrounded by any non-whitespace characters
def fix_spelling(strng, check_str, replace_str):
    fixed_str = re.sub(rf'(?<!\S)(\b{check_str}\b)(?!\S)', replace_str, strng, flags = re.I)  # find "iz" not surrounded by any nonwhitespace chars and replzce it with "is"
    return fixed_str


# split text into sentences and sentences into 'words - nonwords' parts
def split_string(strng):
    sentences = re.split(r'[.?!]', strng) # split text into sentences
    matches = [re.compile(r'(?<=\s)\w+').search(sentences[i]).start() for i in range(len(sentences)-1)]  # find first word preceded by space in each sentence
    sub_sentences =[[sentences[i][:matches[j]], sentences[i][matches[j]:]] for i in range(len(sentences)-1) for j in range(len(matches)) if i == j]  # slice into words part - non words part
    flat_list = [sub_list for list in sub_sentences for sub_list in list]  # generate list of all sub_parts (=flatten list of lists generated in previous line)
    return flat_list


# capitalize each sub_sentence and add them to the new string
def capitalize(list_of_strings):
    updated_str = ''
    for i in list_of_strings:
        new_sub_string = i.capitalize()
        if new_sub_string[-1].isspace() is False:
            new_sub_string = new_sub_string + '.'
        updated_str += new_sub_string
    return updated_str


# just to try to use decorators:)
def separate_mycount_from_text(func):
    def wrapper(*args):
        print("\n  --- \n")
        func(*args)
    return wrapper

# count whitespaces
@separate_mycount_from_text
def count_whitespaces (strng):
    cnt = 0
    for i in strng:
        if i.isspace():
            cnt += 1
    print(f"  I got {cnt} whitespaces in the updated string.")


original_str = '''homEwork:

  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.'''

if __name__ == '__main__':
    last_words = collect_last_words(original_str)
    string_with_new_sentence = add_new_sentence(original_str, 'add it to the end of this paragraph', last_words)
    fixed_spelling = fix_spelling(string_with_new_sentence, "iz", "is")
    list_of_fixed_sentences = split_string(fixed_spelling)
    final_string = capitalize(list_of_fixed_sentences)
    print(final_string)
    count_whitespaces(final_string)
