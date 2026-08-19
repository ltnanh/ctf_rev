# small_counter

* **Category:** Reverse Engineering
* **Difficulty:** Easy

---

## 1. Khảo sát ban đầu 

Kiểm tra thông tin file thực thi bằng lệnh `file`:

```bash
$ file chall
chall: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=7fc574299130abd55813b4512cc7e7f14ece2561, for GNU/Linux 3.2.0, not stripped
```


* Binary là **ELF 64-bit**, chạy trên kiến trúc x86-64.
* **`not stripped`**: Bảng ký hiệu hàm còn nguyên vẹn, giúp định vị hàm `main` và các hàm con dễ dàng.

Dò tìm chuỗi ký tự bằng `strings`:
```bash
$ strings -a chall | grep -iE "flag|ctf|{"
IM{50888H
flag_gen
```

Chạy thử chương trình qua `ltrace` để theo dõi các lời gọi hàm thư viện:
```bash
$ ltrace ./chall
puts("---Counter---") = 14
printf("%d\n", 10)    = 3
...
printf("%d\n", 3)     = 2
memcpy(0x7ffd1371f6e0, "IM{508889j32j87j9jg54650840428hj"..., 69) = 0x7ffd1371f6e0
printf("%d\n", 2)     = 2
printf("%d\n", 1)     = 2
puts("---END---")      = 10
+++ exited (status 0) +++
```

**Phát hiện quan trọng:**
* Chương trình chạy vòng lặp đếm từ 10 về 1.
* Tại bước đếm số **3**, chương trình gọi `memcpy` sao chép **69 bytes** của một chuỗi bắt đầu bằng `IM{50888...`.
* Format cờ yêu cầu là `DH{...}`, tiền tố `IM{...}` bị lệch ký tự gợi ý đây là ciphertext của flag.

---

## 2. Phân tích tĩnh với Ghidra

### A. Phân tích hàm `main`

Mã C giả của `main`:

```c
undefined8 main(void)
{
  ...
  local_c = 0;
  puts("---Counter---");
  for (local_c = 10; 0 < (int)local_c; local_c = local_c - 1) {
    printf("%d\n",(ulong)local_c);
    if (local_c == 3) {
      local_f8 = 0x38383830357b4d49; // "IM{50888"
      local_f0 = 0x6a37386a32336a39; // "9j32j87j"
      local_e8 = 0x3035363435676a39; // "9jg54650"
      local_e0 = 0x6a68383234303438; // "840428hj"
      local_d8 = 0x6838306969326968; // "hi2ii08h"
      local_d0 = 0x3833356a68693437; // "74ihj538"
      local_c8 = 0x3667376a33343568; // "h543j7g6"
      local_c0 = 0x68696a386b6a356b; // "k5kj8jih"
      local_b8 = 0x7d663232;         // "22f}"
      local_b4 = 0;
      memcpy(local_58,&local_f8,0x45); // 0x45 = 69 bytes
    }
  }
  if (local_c == 5) {
    puts("Nice!");
    local_10 = local_c;
    flag_gen(local_58,local_a8,local_c);
    printf("\n%s\n",local_a8);
  }
  else {
    puts("---END---");
  }
  return 0;
}
```


- Khi `local_c == 3`, toàn bộ 69 bytes ciphertext được ghi vào `local_58`.
- Vòng lặp chỉ dừng khi `local_c == 0`.
- Câu lệnh `if (local_c == 5)` không bao giờ được kích hoạt $\rightarrow$ Hàm `flag_gen` bị bỏ qua và chương trình nhảy thẳng vào `else` để in `---END---`.
- Tham số truyền vào `flag_gen` gồm:
   - `param_1` (`local_58`): Con trỏ tới chuỗi ciphertext 69 bytes.
   - `param_2` (`local_a8`): Buffer nhận kết quả giải mã (flag).
   - `param_3` (`local_c`): Key giải mã chuẩn có giá trị bằng **`5`**.

---

### B. Phân tích hàm `flag_gen`

Mã C giả của `flag_gen`:

```c
void flag_gen(char *param_1, long param_2, int param_3)
{
  ...
  for (local_20 = 0; local_20 < 0x1a; local_20 = local_20 + 1) {
    auStack_88[(local_20 + param_3) % 0x1a] = *(undefined1 *)((long)&local_48 + (long)local_20); 
    auStack_a8[(local_20 + param_3) % 0x1a] = *(undefined1 *)((long)&local_68 + (long)local_20); 
  }
  
  local_24 = 0;
  while (true) {
    if (strlen(param_1) <= (ulong)local_24) break;
    local_25 = param_1[local_24];
    ppuVar1 = __ctype_b_loc();
    
    if (((*ppuVar1)[local_25] & 0x200) == 0) {       
      if (((*ppuVar1)[local_25] & 0x100) == 0) {     
        if (((*ppuVar1)[local_25] & 0x800) == 0) {   
          *(char *)(local_24 + param_2) = local_25;  
        }
        else {                                    
          local_1c = ((int)local_25 * (param_3 + 3)) % 9;
          if ((local_1c < 8) || (9 < local_1c)) {
            local_1c = local_1c + 0x32;
          } else {
            local_1c = local_1c + 0x28;
          }
          *(char *)(param_2 + local_24) = (char)local_1c;
        }
      }
      else { 
        *(undefined1 *)(local_24 + param_2) = auStack_a8[local_25 + -0x41];
      }
    }
    else {   
      *(undefined1 *)(local_24 + param_2) = auStack_88[local_25 + -0x61];
    }
    local_24 = local_24 + 1;
  }
  *(undefined1 *)(strlen(param_1) + param_2) = 0;
  return;
}
```


* Hàm `flag_gen` thực chất là hàm **giải mã thuận (decryption routine)**, nhận đầu vào là chuỗi `IM{...}` và tạo ra flag hoàn chỉnh tại `local_a8`.
* Không cần phân tích đảo ngược thuật toán (reverse math), chỉ cần trích xuất đúng ciphertext, gán `key = 5` và tái hiện lại logic của hàm `flag_gen`.

---

## 3. Khai thác & Giải mã (Re-implementation bằng C)

Trích xuất chuỗi ciphertext từ Little-Endian stack hex trong `main`:
`IM{508889j32j87j9jg54650840428hjhi2ii08h74ihj538h543j7g6k5kj8jih22f}`

Viết mã C độc lập để giải mã:

```c
#include <stdio.h>
#include <string.h>
#include <ctype.h>

void solve() {
    char ciphertext[] = "IM{508889j32j87j9jg54650840428hjhi2ii08h74ihj538h543j7g6k5kj8jih22f}";
    char flag[100] = {0};
    int key = 5;


    char lower_table[27] = {0};
    char upper_table[27] = {0};

    for (int i = 0; i < 26; i++) {
        lower_table[(i + key) % 26] = 'a' + i;
        upper_table[(i + key) % 26] = 'A' + i;
    }

    for (size_t i = 0; i < strlen(ciphertext); i++) {
        char c = ciphertext[i];
        if (islower(c)) {
            flag[i] = lower_table[c - 'a'];
        } 
        else if (isupper(c)) {
            flag[i] = upper_table[c - 'A'];
        } 
        else if (isdigit(c)) {
            int val = (c * (key + 3)) % 9;
            if (val < 8 || val > 9) {
                val += 0x32; /
            } else {
                val += 0x28; 
            }
            flag[i] = (char)val;
        } 
        else {
            flag[i] = c; 
        }
    }

    printf("[+] Flag: %s\n", flag);
}

int main() {
    solve();
    return 0;
}
```

```bash
Flag: DH{389998e56e90e8eb34238948469ce98dd6dc04dce359c345e0b2f3fe9edc66a}
```