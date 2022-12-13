#include "helpers.h"
#include <math.h>


// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            // place colours in temporary variable
            int red_value = image[h][w].rgbtRed;
            int blue_value = image[h][w].rgbtBlue;
            int green_value = image[h][w].rgbtGreen;
            int sum_values = red_value + blue_value + green_value;
            int average = round(sum_values / 3.0);
            image[h][w].rgbtRed = average;
            image[h][w].rgbtBlue = average;
            image[h][w].rgbtGreen = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            // temporary variables for original colours
            int originalRed = image[h][w].rgbtRed;
            int originalBlue = image[h][w].rgbtBlue;
            int originalGreen = image[h][w].rgbtGreen;
            // formula for new colours
            int sepiacolors[3];
            int sepiaRed = round(0.393 * originalRed + 0.769 * originalGreen+ 0.189 * originalBlue);
            sepiacolors[0] = sepiaRed;
            int sepiaGreen = round(0.349 * originalRed + 0.686 * originalGreen + 0.168 * originalBlue);
            sepiacolors[1] = sepiaGreen;
            int sepiaBlue = round(0.272 * originalRed + 0.534 * originalGreen + 0.131 * originalBlue);
            sepiacolors[2] = sepiaBlue;
            for (int i = 0; i < 3; i++)
            {
                if (sepiacolors[i] > 255)
                {
                    sepiacolors[i] = 255;
                }
            }
            image[h][w].rgbtRed = sepiacolors[0];
            image[h][w].rgbtGreen = sepiacolors[1];
            image[h][w].rgbtBlue = sepiacolors[2];
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE reverseimage[height][width];
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            reverseimage[h][w] = image[h][width-w-1];
        }
    }
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            image[h][w] = reverseimage[h][w];
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    // make a copy of image
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            copy[h][w] = image[h][w];
        }
    }

    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            int sumRed = 0;
            int sumBlue = 0;
            int sumGreen = 0;
            float counter = 0;

            for (int i = -1; i < 2; i++)
            {
                for (int j = -1 ; j < 2; j++)
                {
                    if ( h + i < 0 || h + i > height -1 || w + j < 0 || w + j > width -1)
                    {
                        continue;
                    }
                    sumRed += copy[h+i][w+j].rgbtRed;
                    sumGreen += copy[h+i][w+j].rgbtGreen;
                    sumBlue += copy[h+i][w+j].rgbtBlue;
                    counter ++;
                }
            }
            int newRed = round(sumRed / counter);
            int newBlue = round(sumBlue / counter);
            int newGreen = round(sumGreen / counter);

            image[h][w].rgbtRed = newRed;
            image[h][w].rgbtBlue = newBlue;
            image[h][w].rgbtGreen = newGreen;
        }
    }
    return;
}
