#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define BLOCK_SIZE 512

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        printf("./recover filename.raw\n");
        return 1;
    }

    FILE *raw_file = fopen(argv[1], "r");
    if (raw_file == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    BYTE buff[BLOCK_SIZE];
    FILE *img = NULL;
    int counter = 0;
    while (fread(buff, 1, BLOCK_SIZE, raw_file) == BLOCK_SIZE)
    {
        if (counter != 0 && !(buff[0] == 255 && buff[1] == 216 && buff[2] == 255 && buff[3] >= 224 && buff[3] <= 239))
        {
            fwrite(buff, 1, BLOCK_SIZE, img);
        }
        else if (buff[0] == 255 && buff[1] == 216 && buff[2] == 255 && buff[3] >= 224 && buff[3] <= 239)
        {
            char name[8] = "\0";
            sprintf(name, "%03i.jpg", counter);
            printf("%s\n", name);
            img = fopen(name, "a");
            fwrite(buff, 1, BLOCK_SIZE, img);
            counter++;
        }
    }

    fclose(raw_file);
}