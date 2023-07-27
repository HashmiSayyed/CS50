#include <stdio.h>
#include <cs50.h>

void print_x_times(int x, char y)
{
    // print provided character provided number of times
    for (int i = 1; i <= x; i++)
    {
        printf("%c", y);
    }
}

int main(void)
{
    int num;
    do
    {
        num = get_int("Height: ");
    } while (num < 1 || num > 8);

    for (int i = 1; i <= num; i++)
    {
        print_x_times(num - i, ' ');
        print_x_times(i, '#');
        printf("  ");
        print_x_times(i, '#');
        printf("\n");
    }
}