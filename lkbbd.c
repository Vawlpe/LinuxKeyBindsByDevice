#include <unistd.h>
#include <stdio.h>
#include <limits.h>
#include <string.h>
#include <libgen.h>

int main(int argc, char *argv[]) {
    setgid(993);
    char execPath[PATH_MAX];
    readlink("/proc/self/exe", execPath, sizeof(execPath));
    dirname(execPath);
    strcat(execPath, "/main.py");

    return execv(execPath, argv);
}
