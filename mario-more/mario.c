#include <cs50.h>
#include <stdio.h>

int main(void)
{
// n is an integer
    int n;
// get height
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1 || n > 8);
// repeat n times
    for (int i = 1; i <= n; i++)
    {
// print (n-i) dots
        for (int k = 1; k <= (n - i); k++)
        {
            printf(" ");
        }
// print i dots
        for (int j = 1; j <= i; j++)
        {
            printf("#");
        }
// print two spaces
        printf("  ");
// print i dots
        for (int j = 1; j <= i; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}