CC     = gcc
CFLAGS = -Wall -Wextra -std=c11
TARGET = task

all: $(TARGET)

$(TARGET): main.c storage.c
	$(CC) $(CFLAGS) -o $(TARGET) main.c storage.c

clean:
	rm -f $(TARGET) tasks.bin

.PHONY: all clean