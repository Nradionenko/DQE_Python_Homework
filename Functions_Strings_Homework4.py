import re


def make_new_sentence(strng, split_pattern, n):
    """Split string by pattern into substrings. Split each substring by spaces into words. Make new sentence from n word from each sub_string.
       n = 0 for 1st element, n = -1 for last element.
    """
    try:
        sentences = re.split(split_pattern, strng)
        temp_words = [sentences[i].split()[n] for i in range(len(sentences)-1)]
        words = [re.sub('\W', "", word) for word in temp_words]
        new_sentence  = ' '.join(words) + '.'
        return new_sentence
    except IndexError:
        print("No such element in sentence. New sentence can't be created.\n")
        return ""


def add_new_sentence(strng, split_pattern, position, new_words):
    """Split string by paragraphs.
    Add new sentence to the specified paragraph sequence(starting from 1)
    """
    lst = re.split(split_pattern, strng)
    if position > len(lst) or position < 1:
        print(f"Paragraph with defined position doesn't exist. Min position = 1, max position = {len(lst)}\n")
        str = strng
    else:
        output = []
        for i in range(len(lst)):
            if i == position - 1:  # position == paragraph sequence number
                output.append(lst[i].rstrip() + ' ' + f"{new_words}\n\n")
            else:
                output.append(lst[i])
        str = split_pattern.join(output)
    return str


def fix_spelling(strng, check_str, replace_str):
    """Fix spelling: replace "iz" with "is" whe is is a separate word not surrounded by any non-whitespace characters"""
    fixed_str = re.sub(rf'(?<!\S)(\b{check_str}\b)(?!\S)', replace_str, strng, flags = re.I)
    return fixed_str


def capitalize(strng, pattern):
    """Split string by pattern (in our case - ending chars + space or /n/n+space).
    Capitalize each element in split list and join back together into string.
    """
    temp_lst= re.split(pattern, strng)
    capitalized_lst = [i.capitalize() for i in temp_lst]
    final_str = ''.join(capitalized_lst)
    return final_str


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
sentence_pattern = '[?!.]'
paragraph_pattern = '\n\n '
capitalize_pattern = '([?!.][\s]|\s{2,})'  # brackets allow to split and keep split delimiters at the same time. This pattern reads as: ending characters+whitespace OR at least 2 whitespaces (for paragraphs)


if __name__ == '__main__':
    last_words = make_new_sentence(original_str, sentence_pattern, -1)
    string_with_new_sentence = add_new_sentence(original_str, paragraph_pattern, 3, last_words)
    fixed_spelling = fix_spelling(string_with_new_sentence, "iz", "is")
    final_string = capitalize(fixed_spelling, capitalize_pattern)
    print(final_string)
    count_whitespaces(final_string)
