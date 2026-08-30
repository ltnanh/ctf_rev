#include <windows.h>
#include <stdio.h>

int main() {
    printf("[*] Loading prob_rev.dll...\n");
    HMODULE h = LoadLibraryA("prob_rev.dll");
    if (h == NULL) {
        printf("[-] Load failed! Error: %lu\n", GetLastError());
    } else {
        printf("[+] Loaded successfully!\n");
    }
    return 0;
}