#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <errno.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdint.h>
#include <sys/stat.h>
#include <fcntl.h>

static uint32_t crc32_tab[] = {
  0x00000000, 0x77073096, 0xee0e612c, 0x990951ba, 0x076dc419, 0x706af48f,
  0xe963a535, 0x9e6495a3, 0x0edb8832, 0x79dcb8a4, 0xe0d5e91e, 0x97d2d988,
  0x09b64c2b, 0x7eb17cbd, 0xe7b82d07, 0x90bf1d91, 0x1db71064, 0x6ab020f2,
  0xf3b97148, 0x84be41de, 0x1adad47d, 0x6ddde4eb, 0xf4d4b551, 0x83d385c7,
  0x136c9856, 0x646ba8c0, 0xfd62f97a, 0x8a65c9ec, 0x14015c4f, 0x63066cd9,
  0xfa0f3d63, 0x8d080df5, 0x3b6e20c8, 0x4c69105e, 0xd56041e4, 0xa2677172,
  0x3c03e4d1, 0x4b04d447, 0xd20d85fd, 0xa50ab56b, 0x35b5a8fa, 0x42b2986c,
  0xdbbbc9d6, 0xacbcf940, 0x32d86ce3, 0x45df5c75, 0xdcd60dcf, 0xabd13d59,
  0x26d930ac, 0x51de003a, 0xc8d75180, 0xbfd06116, 0x21b4f4b5, 0x56b3c423,
  0xcfba9599, 0xb8bda50f, 0x2802b89e, 0x5f058808, 0xc60cd9b2, 0xb10be924,
  0x2f6f7c87, 0x58684c11, 0xc1611dab, 0xb6662d3d, 0x76dc4190, 0x01db7106,
  0x98d220bc, 0xefd5102a, 0x71b18589, 0x06b6b51f, 0x9fbfe4a5, 0xe8b8d433,
  0x7807c9a2, 0x0f00f934, 0x9609a88e, 0xe10e9818, 0x7f6a0dbb, 0x086d3d2d,
  0x91646c97, 0xe6635c01, 0x6b6b51f4, 0x1c6c6162, 0x856530d8, 0xf262004e,
  0x6c0695ed, 0x1b01a57b, 0x8208f4c1, 0xf50fc457, 0x65b0d9c6, 0x12b7e950,
  0x8bbeb8ea, 0xfcb9887c, 0x62dd1ddf, 0x15da2d49, 0x8cd37cf3, 0xfbd44c65,
  0x4db26158, 0x3ab551ce, 0xa3bc0074, 0xd4bb30e2, 0x4adfa541, 0x3dd895d7,
  0xa4d1c46d, 0xd3d6f4fb, 0x4369e96a, 0x346ed9fc, 0xad678846, 0xda60b8d0,
  0x44042d73, 0x33031de5, 0xaa0a4c5f, 0xdd0d7cc9, 0x5005713c, 0x270241aa,
  0xbe0b1010, 0xc90c2086, 0x5768b525, 0x206f85b3, 0xb966d409, 0xce61e49f,
  0x5edef90e, 0x29d9c998, 0xb0d09822, 0xc7d7a8b4, 0x59b33d17, 0x2eb40d81,
  0xb7bd5c3b, 0xc0ba6cad, 0xedb88320, 0x9abfb3b6, 0x03b6e20c, 0x74b1d29a,
  0xead54739, 0x9dd277af, 0x04db2615, 0x73dc1683, 0xe3630b12, 0x94643b84,
  0x0d6d6a3e, 0x7a6a5aa8, 0xe40ecf0b, 0x9309ff9d, 0x0a00ae27, 0x7d079eb1,
  0xf00f9344, 0x8708a3d2, 0x1e01f268, 0x6906c2fe, 0xf762575d, 0x806567cb,
  0x196c3671, 0x6e6b06e7, 0xfed41b76, 0x89d32be0, 0x10da7a5a, 0x67dd4acc,
  0xf9b9df6f, 0x8ebeeff9, 0x17b7be43, 0x60b08ed5, 0xd6d6a3e8, 0xa1d1937e,
  0x38d8c2c4, 0x4fdff252, 0xd1bb67f1, 0xa6bc5767, 0x3fb506dd, 0x48b2364b,
  0xd80d2bda, 0xaf0a1b4c, 0x36034af6, 0x41047a60, 0xdf60efc3, 0xa867df55,
  0x316e8eef, 0x4669be79, 0xcb61b38c, 0xbc66831a, 0x256fd2a0, 0x5268e236,
  0xcc0c7795, 0xbb0b4703, 0x220216b9, 0x5505262f, 0xc5ba3bbe, 0xb2bd0b28,
  0x2bb45a92, 0x5cb36a04, 0xc2d7ffa7, 0xb5d0cf31, 0x2cd99e8b, 0x5bdeae1d,
  0x9b64c2b0, 0xec63f226, 0x756aa39c, 0x026d930a, 0x9c0906a9, 0xeb0e363f,
  0x72076785, 0x05005713, 0x95bf4a82, 0xe2b87a14, 0x7bb12bae, 0x0cb61b38,
  0x92d28e9b, 0xe5d5be0d, 0x7cdcefb7, 0x0bdbdf21, 0x86d3d2d4, 0xf1d4e242,
  0x68ddb3f8, 0x1fda836e, 0x81be16cd, 0xf6b9265b, 0x6fb077e1, 0x18b74777,
  0x88085ae6, 0xff0f6a70, 0x66063bca, 0x11010b5c, 0x8f659eff, 0xf862ae69,
  0x616bffd3, 0x166ccf45, 0xa00ae278, 0xd70dd2ee, 0x4e048354, 0x3903b3c2,
  0xa7672661, 0xd06016f7, 0x4969474d, 0x3e6e77db, 0xaed16a4a, 0xd9d65adc,
  0x40df0b66, 0x37d83bf0, 0xa9bcae53, 0xdebb9ec5, 0x47b2cf7f, 0x30b5ffe9,
  0xbdbdf21c, 0xcabac28a, 0x53b39330, 0x24b4a3a6, 0xbad03605, 0xcdd70693,
  0x54de5729, 0x23d967bf, 0xb3667a2e, 0xc4614ab8, 0x5d681b02, 0x2a6f2b94,
  0xb40bbe37, 0xc30c8ea1, 0x5a05df1b, 0x2d02ef8d
};

// no. you're *not* supposed to bruteforce this challenge. 2^32 is still a
// bit much.
uint32_t hash_password(const char *p) {
  size_t size = strlen(p);
  uint32_t crc = 0;
  crc = crc ^ ~0U;

  while (size--)
    crc = crc32_tab[(crc ^ *p++) & 0xFF] ^ (crc >> 8);

  return crc ^ ~0U;
}

// usernames must match /^[a-zA-Z0-9_]{1,20}$/
bool username_sane(char *user) {
  if (strlen(user) > 20) return false;
  if (*user == '\0') return false;
  for (char *p = user; *p; p++) {
    if (*p >= 'a' && *p <= 'z') continue;
    if (*p >= 'A' && *p <= 'Z') continue;
    if (*p >= '0' && *p <= '9') continue;
    if (*p == '_') continue;
    return false;
  }
  return true;
}

void rtrim(char *str) {
  for (char *p = str+strlen(str)-1; p >= str; p--) {
    if (*p != '\r' && *p != '\n' && *p != ' ' && *p != '\t') return;
    *p = '\0';
  }
}

int open_userfile(char *user, int flags) {
  if (!username_sane(user)) { errno = EACCES; return -1; }

  // construct path: "users/{username}"
  char path[6+20+1] = "users/";
  strcpy(path+6, user);

  return open(path, flags, 0700);
}

struct userdata {
  uint32_t hash;
  unsigned int access_level;
  char description[512];
};

struct userdata *read_userfile(char *user) {
  struct userdata *res = calloc(1, sizeof(*res));
  if (res == NULL) return NULL;
  int fd = open_userfile(user, O_RDONLY);
  if (fd == -1) return NULL;
  FILE *f = fdopen(fd, "r");
  if (f == NULL) { close(fd); return NULL; }
  char line[256];
  while (fgets(line, sizeof(line), f)) {
    rtrim(line);
    char *key = line;
    char *eqsign = strchr(line, '=');
    if (!eqsign) continue;
    *eqsign = '\0';
    char *value = eqsign+1;

    if (!strcmp(key, "hash")) res->hash = atoll(value);
    else if (!strcmp(key, "access_level")) res->access_level = atoi(value);
    else if (!strcmp(key, "description")) strcpy(res->description, value);
    else printf("fatal error: bad key \"%s\" in config, aborting\n", key), exit(1);
  }
  return res;
}

void write_userfile(char *user, struct userdata *ud) {
  int fd = open_userfile(user, O_WRONLY|O_TRUNC);
  if (fd == -1) perror("can't open userdata"), exit(1);
  FILE *f = fdopen(fd, "w");
  if (f == NULL) perror("can't fdopen userdata"), exit(1);
  fprintf(f, "hash=%llu\n", (unsigned long long)ud->hash);
  fprintf(f, "access_level=%u\n", ud->access_level);
  fprintf(f, "description=%s\n", ud->description);
  fclose(f);
}

void handle(int s) {
  alarm(60);

  // Let's handle the socket like a normal terminal or so. Makes the code much
  // nicer. :)
  if (dup2(s, 0)==-1 || dup2(s, 1)==-1) exit(1);
  setbuf(stdout, NULL);

  char username[21] = "";
  struct userdata *ud = NULL;
  bool logged_in = false;

  char line[512]; /* last incoming command */
  while (printf("> "), fgets(line, sizeof(line), stdin)) {
    rtrim(line);
    char *cmd = line;
    char *params = strchr(line, ' ');
    if (params) {
      *params = '\0';
      params++;
    }
    if (!strcmp(cmd, "whoami")) {
      printf((logged_in?"You are logged in as %s.\n":"You are not logged in.\n"), username);
    } else if (!strcmp(cmd, "user")) {
      if (!params || !username_sane(params)) { printf("missing/bad username\n"); continue; }
      strcpy(username, params);
      free(ud);
      logged_in = false;
      ud = read_userfile(username);
      if (ud) {
        printf("username accepted, please provide password\n");
      } else {
        perror("username not accepted");
      }
    } else if (!strcmp(cmd, "pass")) {
      if (!ud) { printf("invalid request\n"); continue; }
      if (!params) { printf("missing password\n"); continue; }
      if (hash_password(params) == ud->hash) {
        printf("login ok\n");
        logged_in = true;
      } else {
        printf("you accidentially mistyped your password, please try again\n");
      }
    } else if (!strcmp(cmd, "register")) {
      if (!params) { printf("missing arguments\n"); continue; }
      char *pass = strchr(params, ':');
      if (!pass) { printf("missing password\n"); continue; }
      *pass = '\0';
      pass++;
      if (strlen(pass) < 8) { printf("password too short\n"); continue; }
      int fd = open_userfile(params, O_WRONLY|O_EXCL|O_CREAT);
      if (fd == -1) { printf("unable to create user: %s\n", strerror(errno)); close(fd); continue; }
      close(fd);

      strcpy(username, params);
      ud = calloc(1, sizeof(*ud));
      logged_in = true;
      ud->hash = hash_password(pass);
      printf("user created successfully\n");
    } else if (!strcmp(cmd, "logout")) {
      if (!logged_in) { printf("you're not even logged in, how could you log out?\n"); continue; }
      logged_in = false;
      write_userfile(username, ud);
      *username = '\0';
      free(ud); ud = NULL;
      printf("Uh, who are you again? I have forgotten.\n");
    } else if (!strcmp(cmd, "whois")) {
      if (!logged_in) { printf("you must be logged in for this\n"); continue; }
      if (!params) { printf("missing username"); continue; }
      struct userdata *ud_ = read_userfile(params);
      if (!ud_) {perror("unable to read userdata"); continue; }
      if (ud_->access_level >= ud->access_level) {
        printf("your access level is too low. sending bandit team to your location.\n");
        free(ud_);
        continue;
      }
      printf("user\t%s\nlevel\t%u\ndescr\t\"%s\"\n", params, ud_->access_level, ud_->description);
      free(ud_);
    } else if (!strcmp(cmd, "levelup")) {
      if (!logged_in) { printf("you must be logged in for this\n"); continue; }
      if (!params) { printf("missing username"); continue; }
      struct userdata *ud_ = read_userfile(params);
      if (!ud_) {perror("unable to read userdata"); continue; }
      if (ud_->access_level >= ud->access_level) {
        printf("your access level is too low for that! sending bandit team to your location.\n");
        free(ud_);
        continue;
      }
      ud_->access_level++;
      write_userfile(params, ud_);
      printf("user promoted to level %u\n", ud_->access_level);
      free(ud_);
    } else if (!strcmp(cmd, "set_description")) {
      if (!logged_in) { printf("you must be logged in for this\n"); continue; }
      if (!params) { printf("missing description\n"); continue; }
      strcpy(ud->description, params);
      printf("description set\n");
    } else {
      printf("unknown command\n");
    }
  }
}

int main(void) {
  int s = socket(AF_INET6, SOCK_STREAM, 0);
  if (s == -1) perror("unable to create server socket"), exit(1);
  struct sockaddr_in6 bind_addr = {
    .sin6_family = AF_INET6,
    .sin6_port = htons(1410)
  };
  if (bind(s, (struct sockaddr *)&bind_addr, sizeof(bind_addr))) perror("unable to bind socket"), exit(1);
  if (listen(s, 0x10)) perror("deaf"), exit(1);

  while (1) {
    int s_ = accept(s, NULL, NULL);
    if (s_ == -1) {
      perror("accept failed, is this bad?"); /* On Error Resume Next */
      continue;
    }
    pid_t child_pid = fork();
    if (child_pid == -1) {
      perror("can't fork! that's bad, I think.");
      close(s_);
      sleep(1);
      continue;
    }
    if (child_pid == 0) close(s), handle(s_), exit(0);
    close(s_);
  }
}
