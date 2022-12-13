#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>


int main(int argc, string argv[])
{
    // check only 1 command like argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else
    {
    // check command line argument is numeric
        int i;
        int n;
        for (i = 0, n = strlen(argv[1]); i < n; i++)
        {
            if (!isdigit(argv[1][i]))
            {
               printf("Usage: ./caesar key\n");
               return 1;
            }
        }
        int intkey = atoi(argv[1]);
        // user to input plaintext
        string plaintext = get_string("plaintext:  ");
        //if key > 26
        if (intkey > 26)
        {
            intkey %= 26;
        }
        int count;
        printf("ciphertext: ");
        for (i = 0, n = strlen(plaintext); i < n; i++)
        {
            int x = (int)plaintext[i];
            // if uppercase letter
            if (x >= 65 && x <= 90)
            {
                x += intkey;
                if(x > 90)
                    x -=26;
                char newchar = (char)x;
                printf("%c", newchar);
            }
            else
            {
                // if lowercase letter
                if (x >= 97 && x <= 122)
                {
                    x += intkey;
                    if(x > 122)
                        x -=26;
                    char newchar = (char)x;
                    printf("%c", newchar);
                }
                else
                // if not letter
                {
                    printf("%c", plaintext[i]);
                }
            }
        }
        printf("\n");


    }
    return 0;
}

