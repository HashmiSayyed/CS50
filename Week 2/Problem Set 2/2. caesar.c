#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include "cs50.h"

bool only_digits(string arg);
char rotate(char c, int i);

int main(int argc, string argv[])
{
    // validate key
    if (argc < 2 || argc > 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else if (!(only_digits(argv[1])))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // convert key to int
    int key = atoi(argv[1]);

    // ask for plaintext
    string plaintext = get_string("plaintext: ");

    // print ciphertext
    printf("ciphertext: ");
    for (int i = 0; i < strlen(plaintext); i++)
    {
        printf("%c", rotate(plaintext[i], key));
    }
    printf("\n");
}

bool only_digits(string s)
{
    // return true if all characters are digits
    // else return false

    bool test = false;

    for (int i = 0; i < strlen(s); i++)
    {
        if (s[i] >= 48 && s[i] <= 57)
        {
            test = true;
        }
        else
        {
            return false;
        }
    }

    return test;
}

char rotate(char c, int i)
{
    // rotate given character by i then return rotated character

    char rotated_char;

    if (i > 26)
    {
        i = i % 26;
    }

    if (isupper(c))
    {
        if ((c + i) > 90)
        {
            rotated_char = (c + i) - 26;
        }
        else
        {
            rotated_char = c + i;
        }
    }
    else if (islower(c))
    {
        if ((c + i) > 122)
        {
            rotated_char = (c + i) - 26;
        }
        else
        {
            rotated_char = c + i;
        }
    }
    else
    {
        rotated_char = c;
    }

    return rotated_char;
}