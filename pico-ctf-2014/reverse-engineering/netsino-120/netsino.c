#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <limits.h>

long boss_cash = 999999999;
long player_cash = 0;

const char *wins[10] = {
    "Pfft, keep the change.",
    "Small pickings, eh?",
    "Winner!",
    "You win!",
    "Ya earned it.",
    "I'll win it back.",
    "Darn, you won.",
    "Gotta give it to ya.",
    "Haxx",
    "Uber haxx!",
};

const char *loses[10] = {
    "Ouch, rough luck.",
    "Oops.",
    "Ya win some ya loose some.",
    "Ya lose!",
    "Loser!",
    "Keep it up, maybe next time.",
    "Make that bet again!",
    "Like that was ever gonna happen.",
    "You seem to enjoy loosing.",
    "Snake eyes! ...not.",
};

int is_digit(char c) {
    return '0' <= c && c <= '9';
}

long getnum() {
    printf("> "); fflush(stdout);
    uint64_t num = 0;

    char c = 0;
    while(!is_digit(c)) {
        c = getchar();
        if(c == EOF) {
            puts("Ya left!");
            exit(0);
        }
    }

    while(is_digit(c)) {
        if(num >= LONG_MAX) {
            num = LONG_MAX;
            break;
        }
        num *= 10;
        num += c - '0';
        c = getchar();
        if(c == EOF) {
            puts("Ya left!");
            exit(0);
        }
    }

    while(c != '\n') {
        c = getchar();
        if(c == EOF) {
            puts("Ya left!");
            exit(0);
        }
    }

    return num;
}

long getbet() {
    while(1) {
        printf("You've got $%lu. How much you wanna bet on this next toss?\n", player_cash);
        long bet = getnum(); 
        if(bet <= player_cash) {
            return bet;
        } else {
            puts("Yerr can't bet more than ya got!");
        }
    }
}

long getchoice(long bet) {
        printf("1: EVEN. Win your bet back plus an additional $%lu if the dice sum even.\n", bet);
        printf("2: ODDS. Win your bet back plus an additional $%lu if both dice roll odd.\n", 3*bet);
        printf("3: HIGH. Win your bet back plus an additional $%lu if the dice sum to 10 or more.\n", 5*bet);
        printf("4: FOUR. Win your bet back plus an additional $%lu if the dice sum to four.\n", 8*bet);
        printf("5: EYES. Win your bet back plus an additional $%lu on snake eyes.\n", 35*bet);
        while(1) {
            puts("What'll it be?");
            long choice = getnum();
            if(1 <= choice && choice <= 5) {
                return choice;
            } else {
                puts("That ain't a choice, buddy!");
            }
        }
}

void grantFlag() {
    char buffer[100];
    FILE *f = fopen("/home/netsino/flag.txt", "r");
    if(!f) {
        puts("BIG PROBLEM, I MISPLACED MY FLAG T_T");
    } else {
        size_t count = fread(buffer, 1, sizeof(buffer), f);
        fclose(f);
        fwrite(buffer, 1, count, stdout);
    }
}

int rand1_6() {
    return (rand()%6)+1;
}

int oneRoll() {
    int i;
    printf("%d", rand1_6());
    for(i = 0; i < 50; i++) {
        fflush(stdout);
        usleep(10000);
        printf("\x08%d", rand1_6());
    }
    int ret = rand1_6();
    printf("\x08%d", ret);
    fflush(stdout);
    return ret;
}

void play(long choice, long bet, int x, int y) {
    switch(choice) {
        case 1: if((x+y)%2 == 0) {
                player_cash += 2*bet;
                boss_cash -= 2*bet;
                puts(wins[rand()%3+0]);
            } else {
                puts(loses[rand()%3+0]);
            }
            break;
        case 2: if(x%2 && y%2) {
                player_cash += 4*bet;
                boss_cash -= 4*bet;
                puts(wins[rand()%3+2]);
            } else {
                puts(loses[rand()%3+2]);
            }
            break;
        case 3: if(x+y >= 10) {
                player_cash += 6*bet;
                boss_cash -= 6*bet;
                puts(wins[rand()%3+3]);
            } else {
                puts(loses[rand()%3+3]);
            }
            break;
        case 4: if(x+y == 4) {
                player_cash += 9*bet;
                boss_cash -= 9*bet;
                puts(wins[rand()%3+5]);
            } else {
                puts(loses[rand()%3+5]);
            }
            break;
        case 5: if(x == 1 && y == 1) {
                player_cash += 36*bet;
                boss_cash -= 36*bet;
                puts(wins[rand()%3+7]);
            } else {
                puts(loses[rand()%3+7]);
            }
            break;
        default:
            puts("Ugh, what happened?");
            exit(0);
    }
}

void seedrand() {
    FILE *f = fopen("/dev/urandom", "r");
    unsigned seed;
    fread(&seed, sizeof(seed), 1, f);
    srand(seed);
    fclose(f);
}

int main(int argc, char *argv[]) {
    seedrand();
    setlinebuf(stdout);
    setlinebuf(stdin);

    puts("Arr, git ye into me casio, the hottest gamblin' sensation on the net!");

    switch(rand()%10) {
        case 0:
        case 1:
        case 2:
        case 3:
        case 4:
            puts("Here, have a fiver, and let's gamble!");
            boss_cash -= 5; player_cash += 5;
            break;
        case 5:
        case 6:
        case 7:
        case 8:
            puts("Here, take twenty, and let's gamble!");
            boss_cash -= 20; player_cash += 20;
            break;
        case 9:
            puts("Fifty bucks says you'll lose it back to me!");
            boss_cash -= 50; player_cash += 50;
            break;
    }

    long bet;
    long choice;
    while(player_cash > 0) {
        bet = getbet();
        player_cash -= bet;
        boss_cash += bet;
        choice = getchoice(bet);

        seedrand();

        puts("Lets rock 'n' roll!");
        int x = oneRoll();
        printf(" ");
        int y = oneRoll();
        puts("");

        play(choice, bet, x, y);

        if(boss_cash < 0) {
            puts("Great, I'm fresh outta cash. Take this flag instead.");
            grantFlag();
            puts("Git outta here.");
            exit(0);
        }
    }
    puts("You ain't got no money, get outta here!");
    return 0;
}
