# Pwnium CTF 2014: Altered code

**Category:** Stegano
**Points:** 150
**Description:**
> Our Spy got spotted in Japan, but before they catch him he send us this file. find out the secret code hidden in the code. [http://41.231.53.40/main.c](main.c)

## Write-up

Written by Tasteless for ctftime.org
```
We got a C source code. If we look carefully at it we will notice that some 
lines are indented with tabs while others are indented with spaces.The solution 
is just to comment or delete the lines indented with tabs and execute the code 
to get the flag.

Flag: D0nT_e4t_Sushi
```
Source: https://ctftime.org/writeup/1177

## Other write-ups

* http://pastebin.com/kr6uDrN3
