#include <iostream>

template <int f, int exp> struct tpow {
	static const int r = f * tpow<f, exp-1>::r;
};

template <int f> struct tpow<f, 0> {
	static const int r = 1;
};

template <int i> struct key {
	static const int r = 0;
};

// Save the makefile-key using template specialization of `key`, field r contains ASCII char value.
#define K(i,v)				\
	template <> struct key<i>	\
	{				\
		static const int r = v; \
	};

#include "key.h"

#define MUL_AND_ADD_MOD(s,t,u,v,w,x,y,z) (((s)*(w) + (t)*(x) + (u)*(y) + (v)*(z)) % 257)


// ------------------------ THIS ENCODES THE `HIDDEN` KEY (used to check if our key is valid) ---------------------------

// In the end, hiddenkey<f, n> is just used as a backbox. We do so as well.

template <int f, int n>
struct hiddenkey
{
	static const int r = hiddenkey<	((f+1)&7) ? ((f+1)&7) : 8,
					((f)>>3)>::r;
};

static const int hiddenkey_table[] = {
	15, 25, 172, 31, 100, 17, 225, 137,
	162, 71, 187, 191, 11, 105, 176, 94
};

// convert byte s, t, u, and v to a unique number.
#define RRRP(s,t,u,v,w) \
	MUL_AND_ADD_MOD(s, t, u, v,			\
		((tpow<f,w>::r) % 257),		\
		((tpow<f,w+1>::r) % 257),	\
		((tpow<f,w+2>::r) % 257),	\
		((tpow<f,w+3>::r) % 257))

template <int f>
struct hiddenkey<f,1>
{
	static const int r = RRRP(26,43,192,42,0)+RRRP(246,8,221,155,4);
};

template <int f>
struct hiddenkey<f,0>
{
	static const int r = RRRP(132,141,229,162,4)+RRRP(48,222,109,0,0);
};

// ------------------------ THIS ENCODES THE `MAKEFILE` KEY (which we must find) ---------------------------

template <int b> struct lookup {
	static const int r = ((3 + lookup<b-1>::r*7) ^ (lookup<b-1>::r*2)) & 255;
};
template <> struct lookup<0> {
	static const int r = 13;
};

static const int lookup_table[] = {
	13, 68, 87, 202, 29, 244, 71, 122,
	173, 228, 247, 42, 125, 148, 39, 90
};

// key  a * 4 + b
template <int a, int b> struct makefilekey
{
	// We see that the chars spaced 4 bytes from each other are always related. We will need to crack
	// those 4 key chars simultaneously. We extract the formula, then brute force over all chars.
	static const int rr = MUL_AND_ADD_MOD(lookup<(a)*4>::r,
				lookup<(a)*4+1>::r,
				lookup<(a)*4+2>::r,
				lookup<(a)*4+3>::r,
				key<b>::r,
				key<b+4>::r,
				key<b+8>::r,
				key<b+12>::r);
};

static int calc_makefilekey(const char *password, int n)
{
	int a = n / 4;
	int b = n % 4;

	return MUL_AND_ADD_MOD(
		lookup_table[a*4],
		lookup_table[a*4+1],
		lookup_table[a*4+2],
		lookup_table[a*4+3],
		password[b],
		password[b+4],
		password[b+8],
		password[b+12]);
}

// ------------------------ VERIFY THAT ENCODED AND MAKEFILE KEY MATCH ---------------------------

// n \in [0, 15]
template <int n>
struct keybyte_diff
{
	// first part is encoded password in this file - password given in the makefile
	static const int r = (((hiddenkey<n,n|2>::r)) % 257) - makefilekey<(n>>2),((n)&3)>::rr;
};

// Execute keybyte_diff<n>::r for all 0 <= n < 16
template <int n> struct keyword_diff {
	static const int r = keybyte_diff<n>::r | keybyte_diff<n+1>::r | keybyte_diff<n+2>::r | keybyte_diff<n+3>::r;
};
struct key_diff {
	static const int r = keyword_diff<0>::r | keyword_diff<4>::r | keyword_diff<8>::r | keyword_diff<12>::r;
};

// ------------------------ WE ATTACK DEFINES WITH OUR OWN DEFINES ---------------------------

#define SPITOUTHIDDEN(n) \
	printf("hiddenkey<%2d, %2d>::r = %3d (MOD 257) = %3d  -  makefilekey<%d, %d>::r = %3d  (%4d) -  runtime makefile %2d = %3d\n",\
		n, n | 2, (((hiddenkey<n,n|2>::r)) % 257), hiddenkey_table[n],							\
		(n>>2), ((n)&3), makefilekey<(n>>2),((n)&3)>::rr,								\
		keybyte_diff<n>::r,												\
		n, calc_makefilekey(testpw, n));

#define SPITOUTLOOKUP(n) \
	printf("lookup<%2d>::r = %3d\n", n, lookup<n>::r);

#define SPITOUT(n) SPITOUTHIDDEN(n)

int main()
{
	//		   AAAAbbbbCCCC
	char testpw[20] = "XuesX_a_key";
	char crackedpw[20] = {0};

	SPITOUT(0);
	SPITOUT(1);
	SPITOUT(2);
	SPITOUT(3);
	SPITOUT(4);
	SPITOUT(5);
	SPITOUT(6);
	SPITOUT(7);
	SPITOUT(8);
	SPITOUT(9);
	SPITOUT(10);
	SPITOUT(11);
	SPITOUT(12);
	SPITOUT(13);
	SPITOUT(14);
	SPITOUT(15);

	// Crack key in groups of 4 chars at once
	for (int off = 0; off < 4; ++off) {
		bool found = false;
		printf("Cracking at offset %d...\n", off);

		for (int c1 = ' '; !found && c1 <= '~'; ++c1) {
		for (int c2 = ' '; !found && c2 <= '~'; ++c2) {
		for (int c3 = ' '; !found && c3 <= '~'; ++c3) {
		for (int c4 = ' '; !found && c4 <= '~'; ++c4) {
			// STUFF
			crackedpw[off] = c1;
			crackedpw[off+4] = c2;
			crackedpw[off+8] = c3;
			crackedpw[off+12] = c4;

			if (calc_makefilekey(crackedpw, off) == hiddenkey_table[off]
				&& calc_makefilekey(crackedpw, off+4) == hiddenkey_table[off+4]
				&& calc_makefilekey(crackedpw, off+8) == hiddenkey_table[off+8]
				&& calc_makefilekey(crackedpw, off+12) == hiddenkey_table[off+12])
				{
				found = true;
			}
		}}}}

		printf("Cracked password: %s\n", crackedpw);
	}

	printf("Cracked password: %s\n", crackedpw);

	if (!key_diff::r)
	{
		int i;
		char skey[] = {
			key<0>::r,
			key<1>::r,
			key<2>::r,
			key<3>::r,
			key<4>::r,
			key<5>::r,
			key<6>::r,
			key<7>::r,
			key<8>::r,
			key<9>::r,
			key<10>::r,
			key<11>::r,
			key<12>::r,
			key<13>::r,
			key<14>::r,
			key<15>::r
		};

		for (i = 0; i < 16; i++)
			std::cout << skey[i];

		std::cout << "\n";
	}
	else
	{
		std::cout << "Wrong\n";
	}

	return 0;
}
