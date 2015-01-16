// g++ -g3 -ggdb -O0 -DDEBUG -I/usr/include/cryptopp main.cpp -o storage.elf -lcryptopp -lpthread
#include <iostream>
using std::cout;
using std::cin;
using std::cerr;
using std::endl;

#include <string>
using std::string;

#include <cstdlib>
using std::exit;

#include "cryptlib.h"
using CryptoPP::Exception;

#include "hex.h"
using CryptoPP::HexEncoder;
using CryptoPP::HexDecoder;

#include "filters.h"
using CryptoPP::StringSink;
using CryptoPP::StringSource;
using CryptoPP::StreamTransformationFilter;

#include "des.h"
using CryptoPP::DES_EDE3;

#include "modes.h"
using CryptoPP::CBC_Mode;

#include "secblock.h"
using CryptoPP::SecByteBlock;

string encrypt_round( const string& key, const string& iv, const string& plain )
{
	string cipher;
	try
	{
	    CBC_Mode< DES_EDE3 >::Encryption e;
	    e.SetKeyWithIV((byte *)key.c_str(), key.size(), (byte *)iv.c_str());
	    StringSource ss1( plain, true, new StreamTransformationFilter(e, new StringSink(cipher) ) );
	}
	catch(const CryptoPP::Exception& e)
	{
	    cerr << e.what() << endl;
	    exit(1);
	}
	return cipher;
}

string encrypt( const string& key, const string& plain )
{
	string result = plain;
	for (int i = 0; i < 100; i++)
	{
		result = encrypt_round(key.substr(i*32, 24), key.substr(i*32 + 24, 8), result);
	}
	return result;
}

string decrypt_round( const string& key, const string& iv, const string& cipher )
{
	string plain;
	try
	{
		CBC_Mode< DES_EDE3 >::Decryption d;
		d.SetKeyWithIV((byte *)key.c_str(), key.size(), (byte*)iv.c_str());
		StringSource s(cipher, true, new StreamTransformationFilter(d,new StringSink(plain)));
	}
	catch(const CryptoPP::Exception& e)
	{
		cerr << e.what() << endl;
		exit(1);
	}
	return plain;
}

void decrypt()
{
	int rbox[800];
	FILE *f = fopen("key","rb");
	fread(&rbox, sizeof(rbox), 1, f);
	string key;
	key.assign((char *) &rbox[0], sizeof(rbox));
	fclose(f);
	f = fopen("secret","rb");
	char name[16];
	fread(&name, sizeof(name), 1, f);
	int size;
	fread(&size, 4, 1, f);
	char *temp_buf = (char *)malloc(size);
	fread(temp_buf, size, 1, f);
	fclose(f);
	string result;
	result.assign(temp_buf, size);
	string encoded;
	StringSource((byte*)result.c_str(), result.size(), true, new HexEncoder(new StringSink(encoded)));
	for (int i = 99; i >= 0; i--)
	{
		result = decrypt_round(key.substr(i*32, 24), key.substr(i*32+24, 8), result);
	}
	cout << "Decoded: " << result << endl;
}

void generate_key(string& key)
{
	srand(time(0));
	int rbox[800];
	for (int i = 0; i < 800; i++)
	{
		rbox[i] = rand();
	}
	key.assign((char *) &rbox[0], sizeof(rbox));
	FILE *f = fopen("key","wb");
	fwrite(&rbox, sizeof(rbox), 1, f);
	fclose(f);
}

void get_and_save_secret(const string &key)
{
	char name[16];
	cout << "Please enter your name (16 chars):" << endl;
	fgets(name, sizeof(name), stdin);
	string secret;
	cout << "Please enter your secret:" << endl;
	cin >> secret;
	secret = encrypt(key, secret);
	int size = secret.size();
	FILE *f = fopen("secret","wb");
	fwrite(name, sizeof(name), 1, f);
	fwrite(&size, 4, 1, f);
	fwrite(secret.c_str(), size, 1, f);
	fclose(f);
	cout << "Done" << endl;
}

int main()
{
	cout << "Super secure information storage" << endl;
	string key;
	generate_key(key);
	get_and_save_secret(key);
	string encoded;
	StringSource((byte*)key.c_str(), key.size(), true, new HexEncoder(new StringSink(encoded)));
	cout << "Please remember your key: " << encoded << endl;
	decrypt();
}