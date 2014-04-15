// BUILD:
// gcc -D_FORTIFY_SOURCE=2 -fstack-protector --param ssp-buffer-size=4 -fPIE -pie -Wl,-z,relro,-z,now

#include <stdlib.h>
#include "https://bitbucket.org/jibsen/tinf/raw/d4327ed5fe3826620e2c53c292d456d5cb6b5932/src/tinflate.c"

void main() {
	char original[8192], compressed[8192];
	unsigned int compressed_len, original_len = 0;
	
	tinf_init();
	if (read(0, &compressed_len, sizeof(compressed_len)) != sizeof(compressed_len) || compressed_len > sizeof(compressed)) {
		exit(-1);
	}
	if (read(0, compressed, compressed_len) != compressed_len) {
		exit(-1);
	}
	tinf_uncompress(original, &original_len, compressed, compressed_len);
	write(1, original, original_len);
}