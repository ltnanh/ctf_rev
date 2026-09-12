# prob_rev.dll

- Category : Rev 
- Dreamhack 
- Difficulty : easy 

## 1. Tổng quan cấu trúc file DLL
```bashl
file prob_rev.dll
prob_rev.dll: PE32+ executable (DLL) (GUI) x86-64, for MS Windows, 6 sections
```

* **Định dạng file:** PE32+ (Windows 64-bit DLL), được biên dịch bằng Microsoft Visual C++ (MSVC).
* **Bảng Export (EAT):** File không xuất khẩu bất kỳ hàm nào . Điều này có nghĩa file `.exe` bên ngoài không thể gọi hàm theo tên hay ordinal, mà DLL được thiết kế để kích hoạt logic ngay khi được nạp vào bộ nhớ.
* **Cơ chế EntryPoint Wrapper:**
  * Windows Loader gọi trực tiếp địa chỉ **`entry`** (`AddressOfEntryPoint` trong PE Header, bản chất là `_DllMainCRTStartup`).
  * Hàm `entry` này đóng vai trò vỏ bọc của trình biên dịch: khởi tạo Stack Canary (`__security_init_cookie`), thiết lập bộ khóa CRT (`__scrt_initialize_crt`), sau đó chuyển tiếp quyền điều khiển qua `dllmain_dispatch` rồi mới gọi đến hàm `DllMain` thực sự do tác giả viết (**`FUN_180001410`**).

```
[Windows Loader] ──> entry() ──> dllmain_dispatch() ──> FUN_180001410() (DllMain gốc)
```

---

## 2. Phân tích luồng thực thi và Định vị logic Flag

Thay vì đi tuần tự (Top-down) từ `entry` qua hàng loạt hàm khởi tạo CRT của Microsoft:

- Quét chuỗi (Defined Strings) tìm thấy chuỗi `"flag"` và `"dreamhack.exe"`.
- Kiểm tra Xref từ chuỗi `"flag"`, lập tức định vị được hàm logic trung tâm: **`FUN_1800011a0`**.

### Phân tích hàm `FUN_1800011a0`

```c
GetModuleFileNameA((HMODULE)0x0, local_238, 0x104);
local_2d8 = PathFindFileNameA(local_238);
iVar2 = strncmp(local_2d8, "dreamhack.exe", 0xd);
```

* **Kiểm tra tiến trình:** DLL lấy tên file `.exe` đang chứa nó. Nếu tên tiến trình không khớp với `"dreamhack.exe"`, hàm lập tức thoát.
* **Khởi tạo mảng State (Seed):**
  * Lấy 4 byte đầu của tên tiến trình: `"drea"` $\rightarrow$ `0x61657264` (Little Endian).
  * Thực hiện xoay bit trái (`ROL`) giá trị này với bước nhảy từ `0` đến `15` bit để tạo mảng 16 phần tử `local_278[16]`.
  * Gọi `FUN_180001010((longlong)local_278)` để nạp mảng này vào vùng nhớ trạng thái PRNG toàn cục (`DAT_180004650`).
* **Khởi động PRNG (Warmup):**
  * Chạy vòng lặp 100 lần gọi `FUN_180001060()` để bỏ qua 100 giá trị giả ngẫu nhiên đầu tiên.
* **Giải mã dữ liệu Flag:**
  * Có 5 hằng số DWORD mã hóa: `0x7ed39c88`, `0x436e8879`, `0x3080393e`, `0x79fd35cc`, `0xf50f300c`.
  * Mỗi DWORD được XOR lần lượt với 5 giá trị tiếp theo sinh ra từ `FUN_180001060()`.
  * Kết quả được ghi vào mảng `local_290` (chứa $5 \times 4 = 20\text{ bytes}$ chuỗi Flag) và hiển thị qua `MessageBoxA(0, local_290, "flag", 0)`.

---

## 3. Khôi phục thuật toán (Method 1: Static Reversing & Solver Script)

Hai hàm con phụ trách sinh khóa:

* **`FUN_180001010`:** Đặt con trỏ chỉ mục `DAT_180004640 = 0` và sao chép 16 DWORD từ seed vào mảng `DAT_180004650`.
* **`FUN_180001060`:** Triển khai thuật toán sinh số giả ngẫu nhiên chu kỳ dài **WELL512a**.

Ta mô phỏng lại toàn bộ thuật toán PRNG và phép XOR bằng Python để trích xuất Flag trực tiếp mà không cần chạy file trên Windows:

```python
import struct

# 1. Khởi tạo mảng State từ chuỗi "drea"
seed_str = b"drea"
seed_val = struct.unpack("<I", seed_str)[0]  # 0x61657264

def rol32(val, n):
    n %= 32
    return ((val << n) | (val >> (32 - n))) & 0xFFFFFFFF

state = [rol32(seed_val, i) for i in range(16)]
idx = 0

# 2. Bộ sinh số ngẫu nhiên WELL512a (FUN_180001060)
def next_rand():
    global idx, state
    uVar1 = (state[idx] ^ ((state[idx] << 16) & 0xFFFFFFFF) ^ state[(idx + 13) & 0xF]) & 0xFFFFFFFF
    uVar2 = (state[(idx + 9) & 0xF] ^ (state[(idx + 9) & 0xF] >> 11)) & 0xFFFFFFFF
    uVar3 = (uVar1 ^ ((state[(idx + 13) & 0xF] << 15) & 0xFFFFFFFF) ^ uVar2) & 0xFFFFFFFF
    
    state[idx] = uVar3
    idx = (idx + 15) & 0xF
    
    term = (state[idx] ^ 
            ((state[idx] << 2) & 0xFFFFFFFF) ^ 
            ((uVar1 << 18) & 0xFFFFFFFF) ^ 
            uVar2 ^ 
            ((uVar2 << 28) & 0xFFFFFFFF) ^ 
            (((uVar3 & 0x6D22169) << 5) & 0xFFFFFFFF)) & 0xFFFFFFFF
            
    state[idx] = term
    return state[idx]

# 3. Chạy 100 lần warmup
for _ in range(100):
    next_rand()

# 4. Giải mã 5 khối dữ liệu bị mã hóa
encrypted = [
    0x7ed39c88,
    0x436e8879,
    0x3080393e,
    0x79fd35cc,
    0xf50f300c
]

flag_bytes = bytearray()
for enc in encrypted:
    k = next_rand()
    dec = enc ^ k
    flag_bytes += struct.pack("<I", dec)

print("FLAG:", flag_bytes.decode(errors="ignore"))
```

## 4. Thực thi động (Method 2: Dynamic Analysis / DLL Injection)

Ngoài cách dịch ngược thuật toán và viết script giải mã tĩnh, ta có thể thu được Flag trực tiếp bằng cách thỏa mãn điều kiện thực thi của file DLL trên môi trường Windows 64-bit.

### 4.1. Phân tích điều kiện kích hoạt
Hàm `FUN_1800011a0` đặt ra 2 ràng buộc:
- DLL phải được nạp vào một tiến trình (kích hoạt sự kiện `DLL_PROCESS_ATTACH`).
- Tiến trình đích phải có tên file thực thi chính xác là **`dreamhack.exe`**.

### 4.2. Các bước khai thác thực tế

- **Chuẩn bị tiến trình mồi:**
   * Tìm một file thực thi 64-bit bất kỳ trên Windows  hoặc viết một file C dummy giữ tiến trình sống .
   * Đổi tên file này thành **`dreamhack.exe`**.
- **Khởi chạy tiến trình:**
   * Chạy file `dreamhack.exe` vừa tạo.
- **Tiêm DLL (DLL Injection):**
   * Sử dụng các công cụ Injector (như *Process Hacker*, *Xenos Injector*, *Cheat Engine*) hoặc viết script Python/C để inject:
     * Chọn tiến trình mục tiêu: `dreamhack.exe`.
     * Chọn file DLL cần nạp: `prob_rev.dll`.
     * Thực hiện Inject (gọi `CreateRemoteThread` $\rightarrow$ `LoadLibraryA("prob_rev.dll")`).
- **Nhận Flag:**
   * Sau khi inject thành công, Windows Loader trong tiến trình `dreamhack.exe` sẽ kích hoạt `DllMain` $\rightarrow$ vượt qua bước kiểm tra tên file $\rightarrow$ hộp thoại `MessageBoxA` hiện lên chứa Flag hoàn chỉnh.

### 4.3 Exploit example 
- code loader.c tự load prob_rev.dll 
```c
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
```
- Biên dịch thành dreamhack.exe 
```
x86_64-w64-mingw32-gcc loader.c -o dreamhack.exe
```
- chạy và nhận flag 
```
wine dreamhack.exe
```

