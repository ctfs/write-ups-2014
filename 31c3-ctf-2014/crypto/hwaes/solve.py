#!/usr/bin/env python

from Crypto.Cipher import AES
from array import array
import os
import socket

#### AES cipher implementation to expand the key
class custom_AES(object):
    block_size = 16

    def __init__(self, key):
        self.setkey(key)

    def setkey(self, key):
        """Sets the key and performs key expansion."""

        self.key = key
        self.key_size = len(key)

        if self.key_size == 16:
            self.rounds = 10
        elif self.key_size == 24:
            self.rounds = 12
        elif self.key_size == 32:
            self.rounds = 14
        else:
            raise ValueError("Key length must be 16, 24 or 32 bytes")

        self.expand_key()
        self.inverse_expand_key()


    def expand_key(self):
        # Performs AES key expansion on self.key and stores in self.exkey
        # Here's a description of AES key schedule:
        # http://en.wikipedia.org/wiki/Rijndael_key_schedule

        # The expanded key starts with the actual key itself
        exkey = array('B', self.key)

        # extra key expansion steps
        if self.key_size == 16:
            extra_cnt = 0
        elif self.key_size == 24:
            extra_cnt = 2
        else:
            extra_cnt = 3

        # 4-byte temporary variable for key expansion
        word = exkey[-4:]
        # Each expansion cycle uses 'i' once for Rcon table lookup
        for i in xrange(1, 11):

            #### key schedule core:
            # left-rotate by 1 byte
            word = word[1:4] + word[0:1]
            # apply S-box to all bytes
            for j in xrange(4):
                word[j] = aes_sbox[word[j]]
            # apply the Rcon table to the leftmost byte
            word[0] = word[0] ^ aes_Rcon[i]
            #### end key schedule core

            for z in xrange(4):
                for j in xrange(4):
                    # mix in bytes from the last subkey
                    word[j] ^= exkey[-self.key_size + j]
                exkey.extend(word)

            # Last key expansion cycle always finishes here
            if len(exkey) >= (self.rounds+1) * self.block_size:
                break

            # Special substitution step for 256-bit key
            if self.key_size == 32:
                for j in xrange(4):
                    # mix in bytes from the last subkey XORed with S-box of
                    # current word bytes
                    word[j] = aes_sbox[word[j]] ^ exkey[-self.key_size + j]
                exkey.extend(word)

            # Twice for 192-bit key, thrice for 256-bit key
            for z in xrange(extra_cnt):
                for j in xrange(4):
                    # mix in bytes from the last subkey
                    word[j] ^= exkey[-self.key_size + j]
                exkey.extend(word)

        self.exkey = exkey
        


    def inverse_expand_key(self):
        # Performs inverse AES key expansion on self.key and stores in self.invexkey

        invexkey = array('B', self.key)
        # extra key expansion steps
        if self.key_size == 16:
            extra_cnt = 0
        elif self.key_size == 24:
            extra_cnt = 2
        else:
            extra_cnt = 3

        # 4-byte temporary variable for key expansion
        word = invexkey[-4:]
        temp = []
        # Each expansion cycle uses 'i' once for Rcon table lookup
        for i in xrange(10, 0, -1):
            
            for z in xrange(3):
                for j in xrange(4):
                    # unmix the bytes from the last subkey
                    word[j] ^= invexkey[j - (z+2)*4]
                temp[:0] = word
                word = invexkey[-(z+2)*4:-(z+1)*4]
                

            word = temp[-4:]            
            #### key schedule core:
            # left-rotate by 1 byte
            word = word[1:4] + word[0:1]    
            # apply S-box to all bytes
            for j in xrange(4):
                word[j] = aes_sbox[word[j]]
            # apply the Rcon table to the leftmost byte
            word[0] = word[0] ^ aes_Rcon[i]
            #### end key schedule core

            for j in xrange(4):
                # unmix the bytes from the last subkey
                word[j] ^= invexkey[-self.key_size + j]

            temp[:0] = word
            invexkey.extend(temp)
            temp = []
            word = invexkey[-4:]

            # Last key expansion cycle always finishes here
            if len(invexkey) >= (self.rounds+1) * self.block_size:
                break

        self.invexkey = invexkey




# The S-box is a 256-element array, that maps a single byte value to another
# byte value. Since it's designed to be reversible, each value occurs only once
# in the S-box
#
# More information: http://en.wikipedia.org/wiki/Rijndael_S-box
aes_sbox = array('B',
    '637c777bf26b6fc53001672bfed7ab76'
    'ca82c97dfa5947f0add4a2af9ca472c0'
    'b7fd9326363ff7cc34a5e5f171d83115'
    '04c723c31896059a071280e2eb27b275'
    '09832c1a1b6e5aa0523bd6b329e32f84'
    '53d100ed20fcb15b6acbbe394a4c58cf'
    'd0efaafb434d338545f9027f503c9fa8'
    '51a3408f929d38f5bcb6da2110fff3d2'
    'cd0c13ec5f974417c4a77e3d645d1973'
    '60814fdc222a908846eeb814de5e0bdb'
    'e0323a0a4906245cc2d3ac629195e479'
    'e7c8376d8dd54ea96c56f4ea657aae08'
    'ba78252e1ca6b4c6e8dd741f4bbd8b8a'
    '703eb5664803f60e613557b986c11d9e'
    'e1f8981169d98e949b1e87e9ce5528df'
    '8ca1890dbfe6426841992d0fb054bb16'.decode('hex')
)

# This is the inverse of the above. In other words:
# aes_inv_sbox[aes_sbox[val]] == val
aes_inv_sbox = array('B',
    '52096ad53036a538bf40a39e81f3d7fb'
    '7ce339829b2fff87348e4344c4dee9cb'
    '547b9432a6c2233dee4c950b42fac34e'
    '082ea16628d924b2765ba2496d8bd125'
    '72f8f66486689816d4a45ccc5d65b692'
    '6c704850fdedb9da5e154657a78d9d84'
    '90d8ab008cbcd30af7e45805b8b34506'
    'd02c1e8fca3f0f02c1afbd0301138a6b'
    '3a9111414f67dcea97f2cfcef0b4e673'
    '96ac7422e7ad3585e2f937e81c75df6e'
    '47f11a711d29c5896fb7620eaa18be1b'
    'fc563e4bc6d279209adbc0fe78cd5af4'
    '1fdda8338807c731b11210592780ec5f'
    '60517fa919b54a0d2de57a9f93c99cef'
    'a0e03b4dae2af5b0c8ebbb3c83539961'
    '172b047eba77d626e169146355210c7d'.decode('hex')
)

# The Rcon table is used in AES's key schedule (key expansion)
# It's a pre-computed table of exponentation of 2 in AES's finite field
#
# More information: http://en.wikipedia.org/wiki/Rijndael_key_schedule
aes_Rcon = array('B',
    '8d01020408102040801b366cd8ab4d9a'
    '2f5ebc63c697356ad4b37dfaefc59139'
    '72e4d3bd61c29f254a943366cc831d3a'
    '74e8cb8d01020408102040801b366cd8'
    'ab4d9a2f5ebc63c697356ad4b37dfaef'
    'c5913972e4d3bd61c29f254a943366cc'
    '831d3a74e8cb8d01020408102040801b'
    '366cd8ab4d9a2f5ebc63c697356ad4b3'
    '7dfaefc5913972e4d3bd61c29f254a94'
    '3366cc831d3a74e8cb8d010204081020'
    '40801b366cd8ab4d9a2f5ebc63c69735'
    '6ad4b37dfaefc5913972e4d3bd61c29f'
    '254a943366cc831d3a74e8cb8d010204'
    '08102040801b366cd8ab4d9a2f5ebc63'
    'c697356ad4b37dfaefc5913972e4d3bd'
    '61c29f254a943366cc831d3a74e8cb'.decode('hex')
)


# the block size for the cipher object; must be 16, 24, or 32 for AES
BLOCK_SIZE = 16
# the character used for padding--with a block cipher such as AES, the value
# you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
# used to ensure that your value is always a multiple of BLOCK_SIZE
PADDING = '\x00'
# one-liner to sufficiently pad the text to be encrypted
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING 
# one-liners to encrypt/encode and decrypt/decode a string
# encrypt with AES, encode with base64
EncodeAES = lambda c, s: c.encrypt(pad(s)).encode("hex")
DecodeAES = lambda c, e: c.decrypt(e.decode("hex")).rstrip(PADDING)


print "START\n"
# connect to the service
s = socket.socket()
s.connect(("188.40.18.66", 2786))
print s.recv(2048)

# get the encrypted flag and expanded key
print ("Encrypt flag")
s.send("flag\n")
encrflag = s.recv(2048)
print "Server encrypted flag = %s" %encrflag
s.send("getkey\n")
key = s.recv(2048)
print "Key = %s" %key

# inverse expand the key
key = key[:-1].decode('hex')
cipher = custom_AES(key)
inverse_expandedkey = ''.join('{:02x}'.format(x) for x in cipher.invexkey)
invexpkey = map(''.join, zip(*[iter(inverse_expandedkey)]*32))
print "Inverse expanded key = %s" %invexpkey

# use the inverse expanded key to decrypt the flag
decrkey = invexpkey[10]
cipher = AES.new(decrkey.decode("hex"))
print "\nLocal decrypted flag = %s" % DecodeAES(cipher, encrflag[:-1])
print "DONE"



