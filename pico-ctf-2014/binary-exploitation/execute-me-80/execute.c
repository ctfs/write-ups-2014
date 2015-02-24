#include <stdio.h>
#include <stdlib.h>

int token = 0;

typedef void (*function_ptr)();

void be_nice_to_people(){
    gid_t gid = getegid();
    setresgid(gid, gid, gid);
}

int main(int argc, char **argv){
    char buf[128];

    be_nice_to_people();

    read(0, buf, 128);

    ((function_ptr)buf)();
}
