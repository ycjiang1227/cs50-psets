#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

int numdgt;
int getdigit(long crdnum, int numbit);
int crdtype;
int checkvalid(long crdnum);
int currentdigit;
long power(int exponent);
int prdeven;
int sumeven;
int sumodd;
int sum;
int result;

int main(void)
{
// get card number
    long crdnum = get_long("Number: ");
// check length of card number
    numdgt = floor(log10(crdnum))+1;
// check if length is valid - 16, 15 or 13
    if (numdgt != 16 & numdgt != 15 & numdgt != 13)
    {
        printf("INVALID\n");
    }
//first two digits for AMEX
    if (numdgt == 15)
    {
        crdtype = crdnum / pow(10,(numdgt-2));
        if (crdtype !=34 & crdtype!=37)
        {
            printf("INVALID\n");
        }
        else
        {
            result = checkvalid(crdnum);
            if (result == 1)
            {
                printf("AMEX\n");
            }
            else printf("INVALID\n");
        }
    }

//first digit for VISA 13 digit card
    if (numdgt == 13)
    {
        crdtype = crdnum / pow(10,(numdgt-1));
        if (crdtype !=4 & crdtype!=4)
        {
            printf("INVALID\n");
        }
        else
        {
            result = checkvalid(crdnum);
            if (result == 1)
            {
                printf("VISA\n");
            }
            else printf("INVALID\n");
        }

    }
//first digit for VISA 16 digit card
    if (numdgt == 16)
    {
        crdtype = crdnum / pow(10,(numdgt-1));
        if (crdtype == 4)
        {
            result = checkvalid(crdnum);
            if (result == 1)
            {
                printf("VISA\n");
            }
            else printf("INVALID\n");
        }
        else
        {
        crdtype = crdnum / pow(10,(numdgt-2));
        if (crdtype > 50 & crdtype < 56)
        {
            result = checkvalid(crdnum);
            if (result == 1)
            {
                printf("MASTERCARD\n");
            }
            else printf("INVALID\n");
        }
        else printf("INVALID\n");
        }
    }
}


//check Luhn's Algorithm, defining checkvalid function
int checkvalid(long crdnum)
{
 for(int i = 1; i <= 16; i++)
    {
        // extract digits
    currentdigit = ((crdnum/power(i-1))%10);
    //for even numbers
    if (i % 2 == 0)
    {
        // multiply digit by 2
        prdeven = currentdigit * 2;
        if (prdeven < 10)
        {
            sumeven += prdeven;
        }
        else
        {
            sumeven += (prdeven-9);
        }
    }
    // for odd numbers
    else
    {
        sumodd += currentdigit;
    }
    // add all digits
    sum = sumeven + sumodd;
    }
    if (sum%10==0)
        return 1;
    else return 0;
}

long power(int exponent)
{
    return pow(10, exponent);
}