#include <stdio.h>
#include <string.h>
#include <ctype.h>

void solve() {
    char ciphertext[] = "IM{508889j32j87j9jg54650840428hj80ii2ih74ihj538h543j7g6k5kj8jih22f}";
    char flag[100] = {0};
    int param_3 = 5; // key = 5

    char lower_table[27] = {0};
    char upper_table[27] = {0};

    for (int i = 0; i < 26; i++) {
        lower_table[(i + param_3) % 26] = 'a' + i;
        upper_table[(i + param_3) % 26] = 'A' + i;
    }

    for (int i = 0; i < strlen(ciphertext); i++) {
        char c = ciphertext[i];
        if (islower(c)) {
            flag[i] = lower_table[c - 'a'];
        } else if (isupper(c)) {
            flag[i] = upper_table[c - 'A'];
        } else if (isdigit(c)) {
            int val = (c * (param_3 + 3)) % 9;
            if (val < 8 || val > 9) {
                val += 0x32;
            } else {
                val += 0x28;
            }
            flag[i] = (char)val;
        } else {
            flag[i] = c; 
        }
    }

    printf("Flag: %s\n", flag);
}

int main() {
    solve();
    return 0;
}