#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include "cs50.h"

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text: ");

    // counting letters,words and sentences
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    // calculating average letters and sentences
    float l = (letters * 100) / (float)words;
    float s = (sentences * 100) / (float)words;

    // calculating grade
    int grade = round((0.0588 * l) - (0.296 * s) - 15.8);

    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}

int count_letters(string text)
{
    // Counts how many letters are there in given string

    int counter = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        if (isupper(text[i]) || islower(text[i]))
        {
            counter++;
        }
    }

    return counter;
}

int count_words(string text)
{
    // Counts how many words are there in given string

    int counter = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == ' ')
        {
            counter++;
        }
    }
    counter++;

    return counter;
}

int count_sentences(string text)
{
    // Counts how many sentences are there in given string

    int counter = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            counter++;
        }
    }

    return counter;
}