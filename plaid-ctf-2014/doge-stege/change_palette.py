#!/usr/bin/env python

import sys
import struct
from zlib import crc32
import os

# PNG file format signature
pngsig = '\x89PNG\r\n\x1a\n'

def swap_palette(filename, n):
    # open in read+write mode
    with open(filename, 'r+b') as f:
        f.seek(0)
        # verify that we have a PNG file
        if f.read(len(pngsig)) != pngsig:
            raise RuntimeError('not a png file!')

        while True:
            chunkstr = f.read(8)
            if len(chunkstr) != 8:
                # end of file
                break

            # decode the chunk header
            length, chtype = struct.unpack('>L4s', chunkstr)
            # we only care about palette chunks
            if chtype == 'PLTE':
                curpos = f.tell()
                paldata = f.read(length)
		# replace palette entry n with white, the rest with black
                paldata = ("\x00\x00\x00" * n) + "\xff\xff\xff" + ("\x00\x00\x00" * (256 - n - 1))
		# replace palette entry 127 to 127 + n with white, the rest with black
                #paldata = ("\x00\x00\x00" * 127) + ("\xff\xff\xff"*n) + ("\x00\x00\x00" * (256 - (127 + n)))

                # go back and write the modified palette in-place
                f.seek(curpos)
                f.write(paldata)
                f.write(struct.pack('>L', crc32(chtype+paldata)&0xffffffff))
            else:
                # skip over non-palette chunks
                f.seek(length+4, os.SEEK_CUR)

if __name__ == '__main__':
    import shutil
    shutil.copyfile(sys.argv[1], sys.argv[2])
    swap_palette(sys.argv[2], int(sys.argv[3]))

