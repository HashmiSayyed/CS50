a_z = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def main():
    # ask for text
    text = input("Text: ")

    # counts letters, words and sentences
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    l = (letters * 100) / words
    s = (sentences * 100) / words

    # apply formula
    grade = round((0.0588 * l) - (0.296 * s) - 15.8)

    # print grade
    if grade < 1:
        print("Before Grade 1")
    elif grade > 16:
        print("Grade 16+")
    else:
        print(f"Grade {grade}")


def count_letters(text):
    '''count letters in given text'''
    count = 0
    for n in range(len(text)):
        if text[n] in a_z:
            count += 1
    return count


def count_words(text):
    '''count words in given text'''
    count = 0
    for n in range(len(text)):
        if text[n] == " ":
            count += 1
    return count + 1


def count_sentences(text):
    '''count sentences in given text'''
    count = 0
    for n in range(len(text)):
        if text[n] == "." or text[n] == "!" or text[n] == "?":
            count += 1
    return count


main()