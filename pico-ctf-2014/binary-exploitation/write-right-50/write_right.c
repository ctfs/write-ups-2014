#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>

unsigned secret = 0xdeadbeef;

int main(int argc, char **argv){
    unsigned *ptr;
    unsigned value;

    char key[33];
    FILE *f;

    printf("Welcome! I will grant you one arbitrary write!\n");
    printf("Where do you want to write to? ");
    scanf("%p", &ptr);
    printf("Okay! What do you want to write there? ");
    scanf("%p", (void **)&value);

    printf("Writing %p to %p...\n", (void *)value, (void *)ptr);
    *ptr = value;
    printf("Value written!\n");

    if (secret == 0x1337beef){
        printf("Woah! You changed my secret!\n");
        printf("I guess this means you get a flag now...\n");

        f = fopen("flag.txt", "r");
        fgets(key, 32, f);
        fclose(f);
        puts(key);

        exit(0);
    }

    printf("My secret is still safe! Sorry.\n");
}
