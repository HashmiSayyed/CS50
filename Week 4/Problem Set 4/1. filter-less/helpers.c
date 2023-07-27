#include <stdio.h>
#include <math.h>
#include "helpers.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            BYTE av = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtBlue = av;
            image[i][j].rgbtGreen = av;
            image[i][j].rgbtRed = av;
        }
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int tmp_sb = round((image[i][j].rgbtRed * 0.272) + (image[i][j].rgbtGreen * 0.534) + (image[i][j].rgbtBlue * 0.131));
            int tmp_sg = round((image[i][j].rgbtRed * 0.349) + (image[i][j].rgbtGreen * 0.686) + (image[i][j].rgbtBlue * 0.168));
            int tmp_sr = round((image[i][j].rgbtRed * 0.393) + (image[i][j].rgbtGreen * 0.769) + (image[i][j].rgbtBlue * 0.189));

            if (tmp_sb > 255)
            {
                tmp_sb = 255;
            }
            if (tmp_sg > 255)
            {
                tmp_sg = 255;
            }
            if (tmp_sr > 255)
            {
                tmp_sr = 255;
            }

            BYTE sepiaBlue = tmp_sb;
            BYTE sepiaGreen = tmp_sg;
            BYTE sepiaRed = tmp_sr;

            image[i][j].rgbtBlue = sepiaBlue;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtRed = sepiaRed;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            tmp[i][width - (1 + j)].rgbtBlue = image[i][j].rgbtBlue;
            tmp[i][width - (1 + j)].rgbtGreen = image[i][j].rgbtGreen;
            tmp[i][width - (1 + j)].rgbtRed = image[i][j].rgbtRed;
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtBlue = image[i][width - (1 + j)].rgbtBlue;
            image[i][j].rgbtGreen = image[i][width - (1 + j)].rgbtGreen;
            image[i][j].rgbtRed = image[i][width - (1 + j)].rgbtRed;
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][width - (1 + j)].rgbtBlue = tmp[i][width - (1 + j)].rgbtBlue;
            image[i][width - (1 + j)].rgbtGreen = tmp[i][width - (1 + j)].rgbtGreen;
            image[i][width - (1 + j)].rgbtRed = tmp[i][width - (1 + j)].rgbtRed;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmp[height][width];
    for (int a = 0; a < height; a++)
    {
        for (int b = 0; b < width; b++)
        {
            tmp[a][b].rgbtBlue = image[a][b].rgbtBlue;
            tmp[a][b].rgbtGreen = image[a][b].rgbtGreen;
            tmp[a][b].rgbtRed = image[a][b].rgbtRed;
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float counter = 0.0;
            int blue_sum = 0;
            int green_sum = 0;
            int red_sum = 0;

            if (i - 1 >= 0 && j - 1 >= 0)
            {
                blue_sum += tmp[i - 1][j - 1].rgbtBlue;
                green_sum += tmp[i - 1][j - 1].rgbtGreen;
                red_sum += tmp[i - 1][j - 1].rgbtRed;
                counter++;
            }
            if (i - 1 >= 0 && j >= 0)
            {
                blue_sum += tmp[i - 1][j].rgbtBlue;
                green_sum += tmp[i - 1][j].rgbtGreen;
                red_sum += tmp[i - 1][j].rgbtRed;
                counter++;
            }
            if (i - 1 >= 0 && j < width - 1)
            {
                blue_sum += tmp[i - 1][j + 1].rgbtBlue;
                green_sum += tmp[i - 1][j + 1].rgbtGreen;
                red_sum += tmp[i - 1][j + 1].rgbtRed;
                counter++;
            }
            if (i >= 0 && j - 1 >= 0)
            {
                blue_sum += tmp[i][j - 1].rgbtBlue;
                green_sum += tmp[i][j - 1].rgbtGreen;
                red_sum += tmp[i][j - 1].rgbtRed;
                counter++;
            }
            if (i >= 0 && j >= 0)
            {
                blue_sum += tmp[i][j].rgbtBlue;
                green_sum += tmp[i][j].rgbtGreen;
                red_sum += tmp[i][j].rgbtRed;
                counter++;
            }
            if (i >= 0 && j < width - 1)
            {
                blue_sum += tmp[i][j + 1].rgbtBlue;
                green_sum += tmp[i][j + 1].rgbtGreen;
                red_sum += tmp[i][j + 1].rgbtRed;
                counter++;
            }
            if (i < height - 1 && j - 1 >= 0)
            {
                blue_sum += tmp[i + 1][j - 1].rgbtBlue;
                green_sum += tmp[i + 1][j - 1].rgbtGreen;
                red_sum += tmp[i + 1][j - 1].rgbtRed;
                counter++;
            }
            if (i < height - 1 && j >= 0)
            {
                blue_sum += tmp[i + 1][j].rgbtBlue;
                green_sum += tmp[i + 1][j].rgbtGreen;
                red_sum += tmp[i + 1][j].rgbtRed;
                counter++;
            }
            if (i < height - 1 && j < width - 1)
            {
                blue_sum += tmp[i + 1][j + 1].rgbtBlue;
                green_sum += tmp[i + 1][j + 1].rgbtGreen;
                red_sum += tmp[i + 1][j + 1].rgbtRed;
                counter++;
            }

            image[i][j].rgbtBlue = round(blue_sum / counter);
            image[i][j].rgbtGreen = round(green_sum / counter);
            image[i][j].rgbtRed = round(red_sum / counter);
        }
    }
}