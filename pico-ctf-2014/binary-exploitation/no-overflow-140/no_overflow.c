#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

#define BUFSIZE 256

void greet(int length){
    char buf[BUFSIZE];
    puts("What is your name?");
    read(0, buf, length);
    printf("Hello, %s\n!", buf);
}

void be_nice_to_people(){
    gid_t gid = getegid();
    setresgid(gid, gid, gid);
}

int main(int argc, char **argv){
    int length;
    be_nice_to_people();

    puts("How long is your name?");
    scanf("%d", &length);

    if(length < BUFSIZE) //don't allow buffer overflow
        greet(length);
    else
        puts("Length was too long!");
}
