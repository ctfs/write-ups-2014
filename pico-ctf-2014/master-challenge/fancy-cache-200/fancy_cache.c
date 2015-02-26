#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

struct string {
  size_t length;
  size_t capacity;
  char *data;
};

struct cache_entry {
  struct string *key;
  struct string *value;
  // The cache entry expires after it has been looked up this many times.
  int lifetime;
};

#define CACHE_GET 0
#define CACHE_SET 1

const size_t kCacheSize = 32;

const uint8_t kNotFound = 0x0;
const uint8_t kFound = 0x1;
const uint8_t kCacheFull = 0x2;

struct cache_entry cache[32];
size_t num_cache_entries = 0;

// The goal of this challenge is to get a shell. Since this machine has
// ASLR enabled, a good first step is to get the ability to read memory
// from the server. Once you have that working, read this string for a
// (flag|hint next steps).
const char *kSecretString = "[REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED REDACTED]";

void *xmalloc(size_t size) {
  void *ptr = malloc(size);

  if (ptr == NULL) {
    perror("malloc");
    exit(1);
  }
  return ptr;
}

void *xrealloc(void *ptr, size_t size) {
  void *newptr = realloc(ptr, size);

  if (newptr == NULL) {
    perror("realloc");
    exit(1);
  }
  return newptr;
}

// Initializes a struct string to an empty string.
void string_init(struct string *str) {
  str->length = 0;
  str->capacity = 0;
  str->data = NULL;
}

// Returns an empty string.
struct string *string_create(void) {
  struct string *str = xmalloc(sizeof(*str));
  fprintf(stderr, "malloc(%zu) = %p (string_create)\n", sizeof(*str), str);
  string_init(str);
  return str;
}

// Frees a string.
void string_destroy(struct string *str) {
  fprintf(stderr, "free(%p) (string_destroy str)\n", str);
  free(str);
}

// Returns 1 if the two strings are equal and 0 otherwise.
int string_eq(struct string *a, struct string *b) {
  if (a->length != b->length) {
    return 0;
  }
  return memcmp(a->data, b->data, a->length) == 0;
}

// Reads a string into an existing struct string.
void read_into_string(struct string *str) {
  size_t length;
  read(STDIN_FILENO, &length, sizeof(length));

  str->length = length;
  if (length > str->capacity) {
    char *old_data = str->data;
    str->data = xrealloc(old_data, length);
    fprintf(stderr, "realloc(%p, %zu) = %p (read_into_string)\n", old_data, length, str->data);
    str->capacity = length;
  }

  read(STDIN_FILENO, str->data, length);
}

int read_int(void) {
  int value;
  read(STDIN_FILENO, &value, sizeof(value));
  return value;
}

void write_string(struct string *str) {
  write(STDOUT_FILENO, &str->length, sizeof(str->length));
  write(STDOUT_FILENO, str->data, str->length);
}

struct cache_entry *cache_lookup(struct string *key) {
  size_t i;
  for (i = 0; i < kCacheSize; ++i) {
    struct cache_entry *entry = &cache[i];

    // Skip expired cache entries.
    if (entry->lifetime == 0) {
      continue;
    }

    if (string_eq(entry->key, key)) {
      return entry;
    }
  }

  return NULL;
}

struct cache_entry *find_free_slot(void) {
  size_t i;
  for (i = 0; i < kCacheSize; ++i) {
    if (cache[i].lifetime == 0) {
      return &cache[i];
    }
  }
  return NULL;
}

void do_cache_get(void) {
  struct string key;
  string_init(&key);
  read_into_string(&key);

  struct cache_entry *entry = cache_lookup(&key);
  if (entry == NULL) {
    write(STDOUT_FILENO, &kNotFound, sizeof(kNotFound));
    return;
  }

  write(STDOUT_FILENO, &kFound, sizeof(kFound));
  write_string(entry->value);

  --entry->lifetime;
  if (entry->lifetime <= 0) {
    // The cache entry is now expired.
    fprintf(stderr, "Destroying key\n");
    string_destroy(entry->key);
    fprintf(stderr, "Destroying value\n");
    string_destroy(entry->value);
  }
}

void do_cache_set(void) {
  struct string *key = string_create();
  read_into_string(key);

  struct cache_entry *entry = cache_lookup(key);
  if (entry == NULL) {
    // There's no existing entry for this key. Find a free slot to put
    // a new entry in.
    entry = find_free_slot();
  }

  if (entry == NULL) {
    // No free slots, tell the client the cache is full :-(
    write(STDOUT_FILENO, &kCacheFull, sizeof(kCacheFull));
    return;
  }

  write(STDOUT_FILENO, &kFound, sizeof(kFound));

  entry->key = key;

  if (entry->value == NULL) {
    entry->value = string_create();
  }

  read_into_string(entry->value);
  entry->lifetime = read_int();
}

int main(int argc, char **argv) {
  int rc;
  uint8_t command;

  fprintf(stderr, "Cache server starting up (secret = %s)\n", kSecretString);

  while (1) {
    if (read(STDIN_FILENO, &command, 1) != 1) {
      exit(1);
    }

    switch (command) {
      case CACHE_GET:
        do_cache_get();
        break;
      case CACHE_SET:
        do_cache_set();
        break;
      default:
        // Invalid command.
        return 1;
        break;
    }
  }
  return 0;
}
