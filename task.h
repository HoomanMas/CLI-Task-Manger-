#pragma once

#define MAX_TASKS  100
#define TITLE_LEN  128
#define DATA_FILE  "tasks.bin"

typedef struct {
    int  id;
    char title[TITLE_LEN];
    int  done;
    int  priority;  /* 0=low  1=medium  2=high */
} Task;

#define COLOR_RESET   "\033[0m"
#define COLOR_RED     "\033[31m"
#define COLOR_GREEN   "\033[32m"
#define COLOR_YELLOW  "\033[33m"
#define COLOR_CYAN    "\033[36m"
#define COLOR_BOLD    "\033[1m"