#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "task.h"
#include "storage.h"

/* ── helpers ─────────────────────────────────────────────── */

static int next_id(Task tasks[], int count) {
    int max = 0;
    for (int i = 0; i < count; i++)
        if (tasks[i].id > max) max = tasks[i].id;
    return max + 1;
}

static int parse_priority(const char *s) {
    if (strcmp(s, "high")   == 0) return 2;
    if (strcmp(s, "medium") == 0) return 1;
    return 0;
}

static const char *priority_label(int p) {
    if (p == 2) return "high";
    if (p == 1) return "medium";
    return "low";
}

static const char *priority_color(int p) {
    if (p == 2) return COLOR_RED;
    if (p == 1) return COLOR_YELLOW;
    return COLOR_CYAN;
}

/* ── commands ────────────────────────────────────────────── */

static void cmd_add(Task tasks[], int *count, const char *title, int priority) {
    if (*count >= MAX_TASKS) {
        fprintf(stderr, "Error: task list is full (%d max).\n", MAX_TASKS);
        return;
    }
    Task t;
    t.id       = next_id(tasks, *count);
    t.done     = 0;
    t.priority = priority;
    strncpy(t.title, title, TITLE_LEN - 1);
    t.title[TITLE_LEN - 1] = '\0';
    tasks[(*count)++] = t;
    save_tasks(tasks, *count);
    printf(COLOR_GREEN "Added" COLOR_RESET " [%d] %s (%s)\n",
           t.id, t.title, priority_label(t.priority));
}

static void cmd_list(Task tasks[], int count, const char *filter) {
    if (count == 0) {
        printf("No tasks yet. Use:  ./task add \"title\" [low|medium|high]\n");
        return;
    }
    printf(COLOR_BOLD "%-4s  %-6s  %-8s  %s\n" COLOR_RESET,
           "ID", "STATUS", "PRIORITY", "TITLE");
    printf("────  ──────  ────────  ──────────────────────────────\n");

    int shown = 0;
    for (int i = 0; i < count; i++) {
        Task *t = &tasks[i];
        if (filter) {
            if (strcmp(filter, "pending") == 0 && t->done)  continue;
            if (strcmp(filter, "done")    == 0 && !t->done) continue;
        }
        const char *status_color = t->done ? COLOR_GREEN : COLOR_YELLOW;
        const char *status_label = t->done ? "done   " : "pending";
        printf("%-4d  %s%-7s%s  %s%-8s%s  %s\n",
               t->id,
               status_color, status_label, COLOR_RESET,
               priority_color(t->priority), priority_label(t->priority), COLOR_RESET,
               t->title);
        shown++;
    }
    if (shown == 0)
        printf("No tasks match filter \"%s\".\n", filter);
}

static void cmd_done(Task tasks[], int count, int id) {
    for (int i = 0; i < count; i++) {
        if (tasks[i].id == id) {
            if (tasks[i].done) {
                printf("Task [%d] is already marked done.\n", id);
                return;
            }
            tasks[i].done = 1;
            save_tasks(tasks, count);
            printf(COLOR_GREEN "Done" COLOR_RESET "  [%d] %s\n", id, tasks[i].title);
            return;
        }
    }
    fprintf(stderr, "Error: task [%d] not found.\n", id);
}

static void cmd_delete(Task tasks[], int *count, int id) {
    for (int i = 0; i < *count; i++) {
        if (tasks[i].id == id) {
            printf(COLOR_RED "Deleted" COLOR_RESET " [%d] %s\n", id, tasks[i].title);
            for (int j = i; j < *count - 1; j++)
                tasks[j] = tasks[j + 1];
            (*count)--;
            save_tasks(tasks, *count);
            return;
        }
    }
    fprintf(stderr, "Error: task [%d] not found.\n", id);
}

static void print_usage(void) {
    printf(COLOR_BOLD "Usage:\n" COLOR_RESET);
    printf("  ./task add \"title\" [low|medium|high]\n");
    printf("  ./task list [pending|done]\n");
    printf("  ./task done   <id>\n");
    printf("  ./task delete <id>\n");
}

/* ── main ────────────────────────────────────────────────── */

int main(int argc, char *argv[]) {
    if (argc < 2) { print_usage(); return 1; }

    Task tasks[MAX_TASKS];
    int  count = 0;
    load_tasks(tasks, &count);

    const char *cmd = argv[1];

    if (strcmp(cmd, "add") == 0) {
        if (argc < 3) { fprintf(stderr, "Usage: ./task add \"title\" [low|medium|high]\n"); return 1; }
        int priority = (argc >= 4) ? parse_priority(argv[3]) : 0;
        cmd_add(tasks, &count, argv[2], priority);

    } else if (strcmp(cmd, "list") == 0) {
        const char *filter = (argc >= 3) ? argv[2] : NULL;
        cmd_list(tasks, count, filter);

    } else if (strcmp(cmd, "done") == 0) {
        if (argc < 3) { fprintf(stderr, "Usage: ./task done <id>\n"); return 1; }
        cmd_done(tasks, count, atoi(argv[2]));

    } else if (strcmp(cmd, "delete") == 0) {
        if (argc < 3) { fprintf(stderr, "Usage: ./task delete <id>\n"); return 1; }
        cmd_delete(tasks, &count, atoi(argv[2]));

    } else {
        fprintf(stderr, "Unknown command: %s\n", cmd);
        print_usage();
        return 1;
    }

    return 0;
}