import pymorphy2

from emoji_dictionary import russian_to_emoji_dict


def text_to_emoji(string: str) -> str:
    morph = pymorphy2.MorphAnalyzer()
    string = "".join((char if char.isalpha() else f" {char} ") for char in string).split()  # separate none alphabetic
    # characters with spaces

    for i, word in enumerate(string):
        normal_word = morph.normal_forms(word)[0]  # get normal form of the word. What means "normal" form see in Wiki

        if normal_word in russian_to_emoji_dict.keys():

            if morph.parse(word)[0].tag.number == 'plur':  # if verb is plural it will be replaced with two emoji
                string[i] = 2 * russian_to_emoji_dict[normal_word]
            else:                                                                 # # else replace with one emoji
                string[i] = russian_to_emoji_dict[normal_word]

    return ' '.join(string)
