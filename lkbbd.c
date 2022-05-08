#include <unistd.h>
#include <errno.h>

int main(int argc, char *argv[]) {
    setgid(993);
    return execv("./main.py", argv);
}