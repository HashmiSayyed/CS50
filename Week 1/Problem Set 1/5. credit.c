#include <stdio.h>
#include "cs50.c"

int main(void)
{
    long long num = 4003600000000014;
    long long gp = num;
    int count = 0;

    do
    {
        gp /= 10;
        count++;
    } while (gp != 0);

    long long snd = (num % 100) / 10;

    printf("%i %lld\n", count, snd);
}