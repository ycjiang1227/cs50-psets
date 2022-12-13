#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int count_characters(string text);
int letters = 0;
int count_words(string text);
int words = 1;
int count_sentences(string text);
int sentences = 0;

int main(void)
{
    //text to analyse
    string text = get_string("Text: ");
    int num_letters = count_characters(text);
    float fletters = (float) num_letters;
    int num_words = count_words(text);
    float fwords = (float) num_words;
    int num_sentences = count_sentences(text);
    float fsentences = (float) num_sentences;
    float L = (fletters / fwords)*100;
    float S = (fsentences / fwords)*100;
    int index = round((0.0588*L) - (0.296*S) - 15.8);
    if(index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        if(index >= 16)
        {
            printf("Grade 16+\n");
        }
        else printf("Grade %i\n", index);
    }
}

// count characters function
int count_characters(string text)
{
        for (int i = 0; text[i] != '\0'; i++)
    {
        // add 1 to letters if alphabetical
        if (isalpha(text[i]))
        {
            letters++;
        }
    }
    return letters;
}

// count words function
int count_words(string text)
{
    for (int i = 0; text[i] != '\0'; i++)
    {
        // add 1 to words after each space
        if ((int) text[i] == 32)
        {
            words++;
        }
    }
    return words;
}

// count sentences function
int count_sentences(string text)
{
    for (int i = 0; text[i] != '\0'; i++)
    {
        if ((int)text [i] == 33 || (int)text [i] == 46 || (int)text [i] == 63 )
        {
            sentences++;
        }
    }
    return sentences;
}