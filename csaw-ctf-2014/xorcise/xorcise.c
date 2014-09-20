/* 
    --------------------------
    XORCISE ENTERPRISE EDITION 
    --------------------------
*/

#include <time.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define BLOCK_SIZE 8
#define MAX_BLOCKS 16

#define FILE_ERROR "Unable to open file."
#define AUTH_ERROR "Authentication Required."

struct cipher_data
{
    uint8_t length;
    uint8_t key[8];
    uint8_t bytes[128];
};
typedef struct cipher_data cipher_data;

struct request
{
    uint32_t opcode;
    uint32_t checksum;
    uint8_t data[100];
};
typedef struct request request;

char password[16];
time_t start_time;

void hexdump(unsigned char *buf, size_t len, FILE *fd)
{
    size_t loop = 0, diff = 0, left=0;
    unsigned char *p = NULL;
    char tmp[24];

    p = buf;
    memset(tmp, 0, sizeof(tmp));

    for (loop = 0; loop < len; ++loop, ++p)
    {
        if (loop && !(loop % 16))
        {
            fprintf(fd, "| %s\n", tmp);
            memset(tmp, 0, 16);
        }

        fprintf(fd, "%02x ", *p);
        tmp[loop % 16] = isprint(*p)?*p:'.';
    }
    diff = loop % 16;

    if (!diff)
    {
        fprintf(fd, "| %s\n", tmp);
        return;
    }
    left = 16 - diff;

    for (loop = 0; loop < left; ++loop)
    {
        fprintf(fd, "   ");
    }
    fprintf(fd, "| %s\n", tmp);
}

uint32_t cluster_f(uint8_t *data, uint32_t length)
{
    uint32_t hash;
    uint32_t iv;
    uint32_t temp;
    uint32_t rounds;
    uint8_t cluster[]={  0x31, 0x24, 0x13, 0x41,
                         0x37, 0x6D, 0x73, 0xFF,
                         0x00, 0xCC, 0x99, 0x01};
    uint8_t cluster2[]={ 0x11, 0x01, 0x22, 0x06,
                         0x33, 0x20, 0x44, 0xD0,
                         0x55, 0x0F, 0x6E, 0x00};

    rounds = length < 16 ? 16: length;
    iv = 0x10F00F01;
    hash = iv;
    while (rounds)
    {
        iv ^= data[rounds % length];
        iv <<= 8;
        iv ^= cluster[rounds % sizeof(cluster)];
        iv <<= 3;
        iv ^= cluster2[rounds%sizeof(cluster2)];
        hash ^= iv;
        temp = hash;
        temp ^= cluster2[(temp<<2) % sizeof(cluster2)];
        hash <<= 1;
        hash += cluster[iv % sizeof(cluster)];
        hash <<= 1;
        hash ^= cluster[(temp & 0xFF00)%sizeof(cluster)];
        temp <<= 1;
        temp ^= cluster[(temp<<2) % sizeof(cluster2)];
        hash += temp;
        --rounds;
    }

    return hash;
}

uint32_t decipher(cipher_data *data, uint8_t *output)
{
    uint8_t buf[MAX_BLOCKS * BLOCK_SIZE];    
    uint32_t loop;
    uint32_t block_index;
    uint8_t xor_mask = 0x8F;

    memcpy(buf, data->bytes, sizeof(buf));
    if ((data->length / BLOCK_SIZE) > MAX_BLOCKS)
    {
        data->length = BLOCK_SIZE * MAX_BLOCKS;
    }

    for (loop = 0; loop < data->length; loop += 8)
    {
        for (block_index = 0; block_index < 8; ++block_index)
        {
            buf[loop+block_index]^=(xor_mask^data->key[block_index]);
        }
    }
    memcpy(output, buf, sizeof(buf));
}

uint32_t is_authenticated(request *packet, uint8_t *key)
{
    char buf[128];
    uint32_t hash_a;
    uint32_t hash_b;
    uint32_t auth_checksum;
    
    memset(buf, 0, sizeof(buf));
    memcpy(buf, password, 16);
    memcpy(buf+16, key, 8);
    hash_a = cluster_f(buf, 24);
    /*printf("hash_a [%08x] from: ", hash_a);
    hexdump(buf, 24, stdout);*/
    
    memset(buf, 0, sizeof(buf));
    memcpy(buf, password, 16);    
    memcpy(buf+16, packet->data, 100);
    hash_b = cluster_f(buf, 116);
    /*printf("hash_b [%08x] from: \n", hash_b);
    hexdump(buf, 116, stdout);*/
    
    memset(buf, 0, sizeof(buf));
    memcpy(buf, (uint8_t *)&hash_a, sizeof(hash_a));
    memcpy(buf+4, (uint8_t *)&hash_b, sizeof(hash_b));
    auth_checksum = cluster_f(buf, 8);
    printf("auth_checksum = %08x\n", auth_checksum);
    printf("packet->checksum = %08x\n", packet->checksum);
    
    if (auth_checksum == packet->checksum)
    {
        return 1;
    }

    return 0;
}

void reap_exited_processes(int sig_number)
{
    pid_t process_id;
    while (1)
    {
        process_id = waitpid(-1, NULL, WNOHANG);
        if ((0==process_id) || (-1==process_id))
        {
            break;
        }
    }
    return;
}

void read_file(int sockfd, uint8_t *name)
{
    FILE *fd;
    size_t bytes_read;
    uint8_t buf[128];

    fd = fopen(name, "r");

    if (NULL == fd)
    {
        printf("Error: %s\n", FILE_ERROR);
        send(sockfd, FILE_ERROR, strlen(FILE_ERROR), 0);
        return;
    }

    memset(buf, 0, sizeof(buf));
    while (1)
    {
        bytes_read = fread(buf, 1, sizeof(buf), fd);
        if (0 == bytes_read)
        {
            break;
        }
        send(sockfd, buf, bytes_read, 0);
    }
    fclose(fd);
    return;
}

void uptime(int sockfd)
{
    char buf[32];
    memset(buf, 0, sizeof(buf));    
    sprintf(buf, "%u seconds", (uint32_t )start_time);
    send(sockfd, buf, strlen(buf), 0);
}

void timestamp(int sockfd)
{
    char buf[32];
    time_t current_time;
    current_time = time(NULL);
    memset(buf, 0, sizeof(buf));
    sprintf(buf, "timestamp: %u", (uint32_t )current_time);
    send(sockfd, buf, strlen(buf), 0);
}

int process_connection(int sockfd)
{
    ssize_t bytes_read;
    cipher_data encrypted;
    uint8_t decrypted[128];
    request *packet;
    uint32_t authenticated;

    memset(&encrypted, 0, sizeof(encrypted));
    memset(&decrypted, 0, sizeof(decrypted));

    bytes_read = recv(sockfd, (uint8_t *)&encrypted, sizeof(encrypted), 0);
    if (bytes_read <= 0)
    {
        printf("Error: failed to read socket\n");
        return -1;
    }

    if (encrypted.length > bytes_read)
    {
        printf("Error: invalid length in packet\n");
        return -1;
    }

    decipher(&encrypted, decrypted);

    //printf("encrypted->length: %02x\n", encrypted.length);
    //printf("encrypted->key: ");
    //hexdump(encrypted.key, sizeof(encrypted.key), stdout);
    //printf("encrypted->bytes:\n");
    //hexdump(encrypted.bytes, sizeof(encrypted.bytes), stdout);
    //printf("deciphered to: \n");
    //hexdump(decrypted, sizeof(decrypted), stdout);

    packet = (request *)&decrypted;
    authenticated = is_authenticated(packet, encrypted.key);

    if (1 == authenticated)
    {
        printf("Packet is authenticated\n");
    }
    else
    {
        printf("Packet is NOT authenticated\n");
    }

    switch (packet->opcode)
    {
     
    /* 
        functions:
            - timestamp
            - uptime
            - read file
            - execute command
    */

        case 0x01:
            printf("Timestamp Request\n");
            timestamp(sockfd);
            break;

        case 0x24:
            printf("Uptime Request\n");
            uptime(sockfd);
            break;            

        case 0x3A:
            if (0 == authenticated)
            {
                send(sockfd, AUTH_ERROR, strlen(AUTH_ERROR), 0);
                return -1;
            }
            printf("Read File Request: %s\n", packet->data);
            read_file(sockfd, packet->data);
            break;

        case 0x5C:
            if (0 == authenticated)
            {
                send(sockfd, AUTH_ERROR, strlen(AUTH_ERROR), 0);
                return -1;
            }
            printf("Execute Command Request: %s\n", packet->data);
            system(packet->data);
            break;

        default:
            printf("Unknown opcode: %08x\n", packet->opcode);
            break;
    }
    return 0;
}

int tcp_server_loop(uint16_t port)
{
    int sd;
    int client_sd; 
    struct sockaddr_in server; 
    struct sockaddr_in client;
    socklen_t address_len;

    pid_t process_id;
    struct sigaction sig_manager;
    
    memset(&server, 0, sizeof(server)); 
    memset(&client, 0, sizeof(client));

    sig_manager.sa_handler = reap_exited_processes;
    sig_manager.sa_flags = SA_RESTART;
    
    if (-1 == sigfillset(&sig_manager.sa_mask))
    {
        printf("Error: sigfillset failed\n");
        return -1;
    }

    if (-1 == sigaction(SIGCHLD, &sig_manager, NULL))
    {
        printf("Error: sigaction failed\n");
        return -1;
    }

    sd = socket(AF_INET, SOCK_STREAM, 0); 
    if (sd < 0)
    {
        printf("Error: failed to acquire socket\n");
        return -1;
    }

    address_len = sizeof(struct sockaddr);
    server.sin_family = AF_INET;
    server.sin_port = htons(port);
    server.sin_addr.s_addr = INADDR_ANY;

    if (-1 == bind(sd, (struct sockaddr *)&server, address_len))
    {
        printf("Error: failed to bind on 0.0.0.0:%i\n", port);
        return -1;
    }

    if (-1 == listen(sd, SOMAXCONN))
    {
        printf("Error: failed to listen on socket\n");
        return -1;
    }

    printf("Entering main listening loop...\n");
    while (1)
    {
        client_sd = accept(sd, (struct sockaddr *)&client, &address_len);
        if (-1 == client_sd)
        {
            printf("Error: failed accepting connection, continuing\n");
            continue;
        }

        printf("Accepted connection from %s\n", inet_ntoa(client.sin_addr)); 
        
        process_id = fork();
        if (0 == process_id)
        {
            process_connection(client_sd);
            close(client_sd); 
            close(sd);
            exit(0);
        }

        close(client_sd);

    }
}

int main(int argc, char *argv[])
{
    FILE *fd; 
    char *newline;

    printf("           ---------------------------------------\n");
    printf("           --            XORCISE 1.1b           --\n");
    printf("           --   NOW WITH MORE CRYPTOGRAPHY!!!   --\n");
    printf("           ---------------------------------------\n");

    fd = fopen("password.txt", "rb");
    if (NULL == fd)
    {
        printf("Error: failed to open password.txt!\n");
        exit(1);
    }

    start_time = time(NULL);

    memset(password, 0, sizeof(password));
    fgets(password, sizeof(password), fd);
    fclose(fd);

    newline = strchr(password, 0x0a);
    if (NULL != newline)
    {
        *newline = 0x0;
    }

    tcp_server_loop(24001);
    return 0;
}

