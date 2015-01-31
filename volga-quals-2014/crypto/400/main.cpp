//
//  main.cpp
//  SPnet
//
//  Created by Alexander Verichev on 3/29/14.
//  Copyright (c) 2014 Alexander Verichev. All rights reserved.
//

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>



const uint8_t S1[] = {   3,  10,  13,   0,   6,   5,  15,   8,   4,   7,  14,   9,  11,   2,   1,  12};
const uint8_t S2[] = {   3,  10,   9,   0,   6,   5,  15,   8,  11,   2,   1,  12,   4,   7,  14,  13};
const uint8_t S3[] = {   5,   6,   3,  14,   9,  13,  10,   0,  15,   2,   7,   4,   1,  12,  11,   8};
const uint8_t S4[] = {   7,   5,  13,   2,  10,  15,   0,   9,  14,   1,   4,   6,   3,  12,   8,  11};
const uint8_t S1_inv[] = {   3,  14,  13,   0,   8,   5,   4,   9,   7,  11,   1,  12,  15,   2,  10,   6};
const uint8_t S2_inv[] = {   3,  10,   9,   0,  12,   5,   4,  13,   7,   2,   1,   8,  11,  15,  14,   6};
const uint8_t S3_inv[] = {   7,  12,   9,   2,  11,   0,   1,  10,  15,   4,   6,  14,  13,   5,   3,   8};
const uint8_t S4_inv[] = {   6,   9,   3,  12,  10,   1,  11,   0,  14,   7,   4,  15,  13,   2,   8,   5};




std::string show_usage();


void encrypt_round(uint8_t plaintext[], size_t length, uint64_t key, uint8_t ciphertext[]);
void decrypt_round(uint8_t ciphertext[], size_t length, uint64_t key, uint8_t plaintext[]);

uint16_t gen_Subkey(uint64_t key, int round);
uint16_t xor_Subkey(uint16_t P, uint16_t sybkey);
uint16_t S(uint16_t P, const uint8_t S1[], const uint8_t S2[], const uint8_t S3[], const uint8_t S4[]);
uint16_t P(uint16_t P);






int main(int argc, const char * argv[])
{
    //precess input parameters
    if (argc != 5)
    {
        show_usage();
        return 0;
    }
    if (std::string(argv[1]) != "encrypt" &&
        std::string(argv[1]) != "decrypt")
    {
        show_usage();
        return 0;
    }
    if (std::strlen(argv[2]) < 8)
    {
        show_usage();
        return 0;
    }
    
    
    //retrieve the key
    uint64_t key[2];
    std::stringstream ss;
    ss  << std::hex << std::string(argv[2], 0, 16) << " "
    << std::hex << std::string(argv[2], 16, -1);
    ss >> key[0] >> key[1];
    
    
    
    //open files and read data
    std::ifstream fin(argv[3], std::ios::binary);
    if (!fin)
    {
        std::cerr << "Failed to open file " << argv[3] << std::endl;
        return -1;
    }
    std::ofstream fout(argv[4], std::ios::binary);
    if (!fout)
    {
        std::cerr << "Failed to open file " << argv[4] << std::endl;
        return -2;
    }
    
    fin.seekg(0, std::ios::end);
    size_t length = fin.tellg();
    size_t length_with_padding = ((length + 1) >> 1) << 1;
    fin.seekg(0, std::ios::beg);
    uint8_t* in_data = new uint8_t[length_with_padding]{0};
    uint8_t* out_data = new uint8_t[length_with_padding]{0};
    
    fin.read((char*)in_data, length);
    
    
    
    
    //encrypt or decrypt
    if (std::string(argv[1]) == "encrypt")
    {
        encrypt_round(in_data, length_with_padding, key[0], out_data);
        encrypt_round(out_data, length_with_padding, key[1], out_data);
    }
    else if (std::string(argv[1]) == "decrypt")
    {
        //swap keys first
        uint64_t temp = key[0];
        key[0] = key[1];
        key[1] = temp;
        
        decrypt_round(in_data, length_with_padding, key[0], out_data);
        decrypt_round(out_data, length_with_padding, key[1], out_data);
    }
    
    
    //write data
    fout.write((char*)out_data, length_with_padding);
    
    
    fin.close();
    fout.close();
    delete [] in_data;
    delete [] out_data;
    return 0;
    
    
}

std::string show_usage()
{
    return "usage: encrypt|decrypt <hex_encoded_key> <path_to_input_file> <path_to_output_file>";
}




void encrypt_round(uint8_t plaintext[], size_t length, uint64_t key, uint8_t ciphertext[])
{
    for (int j = 0; j < length; j+=2)
    {
        uint16_t temp = ((uint16_t)plaintext[j] << 8) | plaintext[j+1];
        for (int i = 0; i < 3; i++)
        {
            temp = xor_Subkey(temp, gen_Subkey(key, i));
            temp = S(temp, S1, S2, S3, S4);
            temp = P(temp);
        }
        temp = xor_Subkey(temp, gen_Subkey(key, 3));
        temp = S(temp, S1, S2, S3, S4);
        temp = xor_Subkey(temp, gen_Subkey(key, 4));
        ciphertext[j] = temp >> 8;
        ciphertext[j+1] = temp & ((1 << 8) - 1);
    }
}
void decrypt_round(uint8_t ciphertext[], size_t length, uint64_t key, uint8_t plaintext[])
{
    
    for (int j = 0; j < length; j+=2)
    {
        uint16_t temp = ((uint16_t)ciphertext[j] << 8) | ciphertext[j+1];
        temp = xor_Subkey(temp, gen_Subkey(key, 4));
        for (int i = 1; i < 4; i++)
        {
            temp = S(temp, S1_inv, S2_inv, S3_inv, S4_inv);
            temp = xor_Subkey(temp, gen_Subkey(key, 4-i));
            temp = P(temp);
        }
        temp = S(temp, S1_inv, S2_inv, S3_inv, S4_inv);
        temp = xor_Subkey(temp, gen_Subkey(key, 0));
        plaintext[j] = temp >> 8;
        plaintext[j+1] = temp & ((1 << 8) - 1);
    }
    
}


uint16_t gen_Subkey(uint64_t key, int round)
{
    uint64_t temp = key;
    for (int i = 0; i < round; i++)
        temp = P(temp);
    return temp & 0xFFFF;
}
uint16_t xor_Subkey(uint16_t P, uint16_t sybkey)
{
    return P ^ sybkey;
}
uint16_t S(uint16_t P, const uint8_t S1[], const uint8_t S2[], const uint8_t S3[], const uint8_t S4[])
{
    uint16_t ret = 0;
    ret |= S4[P         & 0b1111];
    ret |= S3[(P >> 4)  & 0b1111] << 4;
    ret |= S2[(P >> 8)  & 0b1111] << 8;
    ret |= S1[(P >> 12) & 0b1111] << 12;
    
    
    return ret;
}
uint16_t P(uint16_t P)
{
    uint8_t p3 =  P        & 0b1111;
    uint8_t p2 = (P >> 4)  & 0b1111;
    uint8_t p1 = (P >> 8)  & 0b1111;
    uint8_t p0 = (P >> 12) & 0b1111;
    
    uint8_t c0 = 0, c1 = 0, c2 = 0, c3 = 0;
    
    
    c0 |=  p0 & 0b1000;
    c0 |= (p1 & 0b1000) >> 1;
    c0 |= (p2 & 0b1000) >> 2;
    c0 |= (p3 & 0b1000) >> 3;
    
    c1 |= (p0 & 0b0100) << 1;
    c1 |=  p1 & 0b0100;
    c1 |= (p2 & 0b0100) >> 1;
    c1 |= (p3 & 0b0100) >> 2;
    
    c2 |= (p0 & 0b0010) << 2;
    c2 |= (p1 & 0b0010) << 1;
    c2 |=  p2 & 0b0010;
    c2 |= (p3 & 0b0010) >> 1;
    
    c3 |= (p0 & 0b0001) << 3;
    c3 |= (p1 & 0b0001) << 2;
    c3 |= (p2 & 0b0001) << 1;
    c3 |=  p3 & 0b0001;
    
    
    return (c0 << 12) | (c1 << 8) | (c2 << 4) | (c3);
}




