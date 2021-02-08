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


# capitalize first words after given pattern:
def set_to_capital(m):
    return m.group(1) + m.group(2).capitalize()


# normalize text
def normalize(strng):
    pattern = re.compile(r"([?!.:]\s+)(\S+)")  # first word or first word preceded by ending char + whitespaces
    normalized = re.sub(pattern, set_to_capital, strng.capitalize())  # set text to capitalize first (to handle Homework) and then replace first words with capitalized
    return normalized


# count whitespaces
def count_whitespaces (strng):
    cnt = 0
    for i in strng:
        if i.isspace():
            cnt += 1
    print(f"\n\n\n  I got {cnt} whitespaces in the updated string.")


original_str = '''homEwork:

  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.'''

if __name__ == '__main__':
    last_words = collect_last_words(original_str)
    string_with_new_sentence = add_new_sentence(original_str, 'add it to the end of this paragraph', last_words)
    fixed_spelling = fix_spelling(string_with_new_sentence, "iz", "is")
    final_string = normalize(fixed_spelling)
    print(final_string)
    count_whitespaces(final_string)
