#include <stdio.h>
#include "storage.h"

int load_tasks(Task tasks[], int *count) {
    FILE *fp = fopen(DATA_FILE, "rb");
    if (!fp) {
        *count = 0;
        return 0;
    }
    fread(count, sizeof(int), 1, fp);
    if (*count > MAX_TASKS) *count = MAX_TASKS;
    fread(tasks, sizeof(Task), *count, fp);
    fclose(fp);
    return 1;
}

int save_tasks(Task tasks[], int count) {
    FILE *fp = fopen(DATA_FILE, "wb");
    if (!fp) {
        fprintf(stderr, "Error: could not open %s for writing.\n", DATA_FILE);
        return 0;
    }
    fwrite(&count, sizeof(int), 1, fp);
    fwrite(tasks, sizeof(Task), count, fp);
    fclose(fp);
    return 1;
}