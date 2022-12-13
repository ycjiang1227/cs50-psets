#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

long crdnum; // card number
int currentdigit;
long power(int exponent);
int prdeven;
int sumeven;
int sumodd;
int sum;
int modulo10;

int main(void)
{
    // get card number
    crdnum = get_long("Number: ");

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

long power(int exponent)
{
    return pow(10, exponent);
}


//modulo 10
modulo10 = sum % 10;
if (modulo10 != 0)
{
    printf("INVALID\n");
}

}