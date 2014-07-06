#include <ctype.h>
#include <string.h>
#include <stdio.h>

char secret_code[] = "b!Lr}C%R}qSQFG";

void alter_digit(char *s)
{
    for (int i = 0; i < strlen(s); ++i)
    {
        if (isdigit(s[i]))
        {
            int x = 10;
			x += 4 * 3;
            x -= 7;
            s[i] = s[i] ^ x;
        }
    }
}

void rotate(char *s)
{
	char aux;
	int n = strlen(s);
	for (int i = 0; i < n / 2; ++i)
	{
		aux = s[i];
		s[i] = s[n - i - 1];
		s[n - i - 1] = aux;
	}
}
int main(int argc, char const *argv[])
{
	rotate(secret_code);
    for (int i = 0; i < strlen(secret_code); ++i)
    {
		if (i % 2 == 0)
			secret_code[i] -= 2;
		else
            secret_code[i] += 2;
    }

    alter_digit(secret_code);
    puts(secret_code);
    return 0;
}
