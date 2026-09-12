# TỔNG QUAN TOÀN DIỆN VỀ WINDOWS DLL (DYNAMIC LINK LIBRARY)
*Tài liệu tổng hợp kiến trúc hệ thống, cơ chế bộ nhớ, quy trình biên dịch và phân tích dịch ngược (Reverse Engineering)*

---

## 1. DLL Là Gì và Tác Dụng Của DLL?

### 1.1. Bản chất
**DLL (Dynamic Link Library - Thư viện liên kết động)** là định dạng file thực thi dạng thư viện chuẩn PE/PE32+ trên Windows (tương đương file `.so` trên Linux). 
* DLL chứa mã máy (code), dữ liệu (data) và tài nguyên (resources).
* DLL **không thể tự chạy độc lập** mà phải được nạp vào không gian địa chỉ bộ nhớ ảo của một tiến trình `.exe` khác.

### 1.2. Tác dụng cốt lõi
* **Tiết kiệm tài nguyên RAM & Ổ cứng:** Thay vì nhúng cứng (Static Link) cùng một đoạn code vào hàng trăm file `.exe`, các tiến trình dùng chung một file DLL hệ thống (như `kernel32.dll`, `user32.dll`).
* **Kiến trúc Module hóa (Modularity):** Cho phép chia nhỏ dự án phần mềm thành nhiều module/plugin. Khi cần sửa lỗi hoặc nâng cấp tính năng, chỉ cần cập nhật riêng file `.dll` mà không cần biên dịch lại toàn bộ ứng dụng.
* **Tái sử dụng mã đa ngôn ngữ:** Viết thư viện bằng C/C++, biên dịch ra DLL và có thể gọi từ C#, Python, Rust, Go qua cơ chế FFI/PInvoke.

---

## 2. Cơ Chế Quản Lý Bộ Nhớ Của Hệ Điều Hành Khi Nạp DLL

```
+---------------------------------------------------------------+
|                    TIẾN TRÌNH A (RAM ẢO)                     |
|  [ Mã thực thi A ]  [ .data riêng của A ]  [ Ánh xạ DLL (0x1800) ]
+---------------------------------------------------------------+
                                                    │
                                (Page Table A)      │
                                                    ▼
+---------------------------------------------------------------+
|                     RAM VẬT LÝ (HARDWARE)                     |
|  [ Mã máy DLL (.text) ] <── DÙNG CHUNG DUY NHẤT 1 BẢN TRÊN RAM|
|  [ Trang .data của A  ] <── Tách riêng nhờ Copy-on-Write (CoW) |
|  [ Trang .data của B  ] <── Tách riêng nhờ Copy-on-Write (CoW) |
+---------------------------------------------------------------+
                                                    ▲
                                (Page Table B)      │
                                                    │
+---------------------------------------------------------------+
|                    TIẾN TRÌNH B (RAM ẢO)                     |
|  [ Mã thực thi B ]  [ .data riêng của B ]  [ Ánh xạ DLL (0x7FFF) ]
+---------------------------------------------------------------+
```

### 2.1. Quá trình nạp từ Ổ cứng lên RAM (Demand Paging)
* **Thời điểm nạp:** Khi có **tiến trình đầu tiên** yêu cầu sử dụng DLL, Windows mở file và tạo một đối tượng ánh xạ bộ nhớ (**Section Object / Memory-Mapped File**).
* **Nạp theo nhu cầu (Demand Paging):** Windows không đọc toàn bộ file DLL vào RAM ngay lập tức. Khi CPU chạy tới lệnh đầu tiên chạm vào trang nhớ của DLL, ngắt **Page Fault** xuất hiện, lúc này OS mới thực sự nạp trang 4KB dữ liệu tương ứng từ ổ cứng vào RAM vật lý.
* **Tái sử dụng:** Nếu tiến trình thứ hai cùng nạp DLL này, Windows chỉ cần ánh xạ bảng trang (Page Table) của tiến trình đó vào vùng RAM vật lý đã có sẵn mà không cần đọc lại từ ổ cứng.

### 2.2. RAM Ảo (Virtual Memory) & Cơ chế Copy-on-Write (CoW)
* **Địa chỉ ảo:** Chương trình không bao giờ làm việc trực tiếp với địa chỉ RAM vật lý. Mọi lệnh `CALL`, `JMP`, `MOV` đều thao tác trên **Địa chỉ ảo (Virtual Address)**. Bộ vi xử lý phần cứng (**MMU**) kết hợp Bảng trang (**Page Table**) của OS để dịch sang RAM vật lý.
* **Phân vùng mã lệnh (`.text`):** Đặt cờ `PAGE_EXECUTE_READ` (chỉ đọc/thực thi). Hàng trăm tiến trình cùng trỏ chung vào **1 bản copy duy nhất trên RAM vật lý**.
* **Phân vùng dữ liệu (`.data`, biến toàn cục):** Sử dụng cơ chế **Copy-on-Write (CoW)**:
  * Ban đầu, các tiến trình vẫn đọc chung dữ liệu tĩnh.
  * Ngay khi một tiến trình ghi dữ liệu (ví dụ: gán biến toàn cục `DAT_180004650 = 1`), OS sẽ chặn lại, tự động nhân bản trang RAM đó thành một bản copy riêng cho tiến trình đó rồi mới thực hiện ghi. Các tiến trình khác hoàn toàn không bị ảnh hưởng.

### 2.3. OS và DllMain cập nhật cái gì khi thực thi?
* **Cấp độ OS (Hệ thống):**
  * Cập nhật danh sách module nạp trong cấu trúc `PEB_LDR_DATA` (Process Environment Block) của tiến trình.
  * Tăng/giảm **Reference Count** của module. Nếu `RefCount == 0` (khi gọi `FreeLibrary`), OS mới gỡ bỏ ánh xạ DLL khỏi không gian ảo của tiến trình.
* **Cấp độ DLL:**
  * File DLL vật lý trên đĩa cứng **không bao giờ bị thay đổi**.
  * `DllMain` chạy để khởi tạo/cập nhật các biến toàn cục, bảng trạng thái (state array), cấp phát bộ nhớ động trên **RAM ảo của riêng tiến trình hiện tại**.

---

## 3. Quy Trình Gọi Hàm Trong DLL (Pipeline)

### 3.1. Nạp động trong Runtime (`LoadLibrary` + `GetProcAddress`)
```
[Tiến trình EXE]                      [Hệ Điều Hành Windows]                 [File DLL]
       │                                       │                                 │
       ├── 1. LoadLibrary("prob.dll") ────────>│                                 │
       │                                       ├── 2. Nạp/Ánh xạ vào RAM ảo ────>│
       │                                       │     (Gán Base Address)          │
       │                                       ├── 3. Tự động gọi DllMain ──────>│
       │                                       │      (fdwReason = 1)            │
       │                                       │<─── 4. Trả về TRUE ─────────────┤
       │<── 5. Trả về HMODULE (Base Address) ──┤                                 │
       │                                       │                                 │
       ├── 6. GetProcAddress(h, "Func") ──────>│                                 │
       │                                       ├── 7. Tra bảng Export (EAT) ────>│
       │<── 8. Trả về Virtual Address (VA) ────┤                                 │
       │                                                                         │
       └── 9. Lệnh CALL trực tiếp tới Virtual Address của hàm ──────────────────>│ (Chạy hàm)
```

### 3.2. Nạp tĩnh lúc khởi động (Static / Load-Time Linking)
1. Linker nhúng tên DLL và các hàm cần dùng vào bảng **Import Address Table (IAT)** của file `.exe`.
2. Khi bật `.exe`, Windows Loader duyệt IAT trước khi vào hàm `main()`.
3. Loader nạp các DLL phụ thuộc, gọi `DllMain` của từng DLL (`DLL_PROCESS_ATTACH`), rồi điền địa chỉ ảo của các hàm vào IAT của `.exe`.
4. Khi chạy, file `.exe` gọi hàm qua cú pháp `CALL [IAT_Entry]`.

### 3.3. Kỹ thuật DLL Injection (Ngữ cảnh bài CTF)
* Tiến trình can thiệp (Injector) mở tiến trình nạn nhân (`OpenProcess`), ghi chuỗi đường dẫn DLL vào bộ nhớ nạn nhân (`VirtualAllocEx` + `WriteProcessMemory`), và ép nạn nhân gọi `LoadLibrary` từ xa (`CreateRemoteThread`).
* Khi DLL được nạp vào tiến trình nạn nhân, **Windows tự động kích hoạt `DllMain` với mã `DLL_PROCESS_ATTACH`**. Tác giả CTF thường đặt toàn bộ logic kiểm tra và giải mã flag tại đây mà không cần export bất kỳ hàm nào.

---

## 4. Chi Tiết Về Điểm Nhập Cuộc `DllMain`

### 4.1. Khai báo chuẩn
```c
BOOL WINAPI DllMain(
    HINSTANCE hinstDLL,  // Base Address của DLL trong RAM ảo
    DWORD fdwReason,     // Lý do Windows kích hoạt hàm
    LPVOID lpReserved    // Trạng thái nạp Tĩnh hay Động
);
```

### 4.2. Ý nghĩa 3 tham số do Windows truyền vào
* **`hinstDLL` (`HMODULE`):** Địa chỉ cơ sở nơi DLL được ánh xạ vào RAM ảo của tiến trình (trỏ tới vị trí bắt đầu `IMAGE_DOS_HEADER`, nhận diện bằng chữ ký `MZ` / `0x5A4D`). DLL dùng handle này để tự truy cập tài nguyên nội bộ (`FindResource`, `LoadResource`).
* **`fdwReason` (Mã sự kiện 32-bit):**
  * `1` (**`DLL_PROCESS_ATTACH`**): DLL vừa được nạp vào tiến trình. Dùng để khởi tạo tài nguyên toàn cục, cấp phát bộ nhớ.
  * `0` (**`DLL_PROCESS_DETACH`**): DLL chuẩn bị bị gỡ khỏi tiến trình. Dùng để giải phóng RAM, đóng file handle/socket.
  * `2` (**`DLL_THREAD_ATTACH`**): Tiến trình vừa tạo một Thread mới (`CreateThread`). Dùng để cấp phát Thread-Local Storage (TLS).
  * `3` (**`DLL_THREAD_DETACH`**): Một Thread vừa kết thúc bình thường (`ExitThread`). Dùng để dọn dẹp TLS của luồng.
* **`lpReserved`:**
  * Khi `ATTACH`: `NULL` nếu nạp động qua `LoadLibrary()`; `non-NULL` nếu nạp tĩnh lúc khởi động `.exe`.
  * Khi `DETACH`: `NULL` nếu bị gỡ bởi `FreeLibrary()`; `non-NULL` nếu bị gỡ do toàn bộ tiến trình đang bị đóng (Terminate).

### 4.3. Ý nghĩa giá trị trả về (`return TRUE / FALSE`)
* **Với `DLL_PROCESS_ATTACH`:**
  * `return TRUE`: Nạp thành công, cho phép tiến trình tiếp tục.
  * `return FALSE`: Khởi tạo thất bại. Windows lập tức gỡ DLL khỏi bộ nhớ. Hàm `LoadLibrary()` trả về `NULL`. Nếu là nạp tĩnh, chương trình `.exe` sẽ crash ngay lập tức trước khi kịp chạy `main()`.
* **Với các sự kiện khác (`DETACH`, `THREAD_*`):** Giá trị trả về bị Windows bỏ qua.

---

## 5. Quá Trình Biên Dịch DLL (MSVC Toolchain) & Các Lớp Mã CRT Boilerplate

Khi biên dịch file C/C++ thành DLL bằng Microsoft Visual C++ (`cl.exe` + `link.exe`), trình biên dịch chèn thêm rất nhiều đoạn mã phụ trợ (C Runtime Glue Code) khiến mã dịch ngược bị phân mảnh.

```
[Mã nguồn C của tác giả] 
       │
       ▼ (cl.exe /LD /GS /guard:cf /O2)
[File đối tượng .obj] + [Thư viện msvcrt.lib / vcruntime.lib]
       │
       ▼ (link.exe)
[File prob_rev.dll hoàn chỉnh]
```

### 5.1. Các cờ biên dịch và dấu vết trong Decompiler
| Cờ biên dịch | Tính năng bảo vệ / Tối ưu | Dấu vết nhận diện trong Decompiler (IDA / Ghidra) |
| :--- | :--- | :--- |
| **/GS** | Buffer Security Check (Stack Canary) | Xuất hiện `__security_init_cookie`, `__GSHandlerCheck`, `__report_gsfailure`. |
| **/guard:cf** | Control Flow Guard (CFG) | Xuất hiện `_guard_check_icall`, `_guard_dispatch_icall`. |
| **/DYNAMICBASE**| ASLR (Address Space Randomization) | Phân vùng `.reloc` xuất hiện để hỗ trợ đổi Base Address khi nạp. |
| **/MD** | Dynamic C Runtime | Xuất hiện các import từ `API-MS-WIN-CRT-RUNTIME-...` |
| **/O2** | Tối ưu hóa tốc độ cao nhất | Các hàm ngắn bị Inline; các phép xoay bit dịch thành lệnh ASM `ROL`/`ROR`. |

### 5.2. Bóc tách luồng thực thi: CRT Boilerplate vs Mã người dùng

```
[Windows Loader: LdrLoadDll]
        │
        ▼
1. entry()                                <── Điểm nhập cuộc thực tế do Linker gán
   ├── __security_init_cookie()           <── [CRT] Sinh Stack Canary ngẫu nhiên
   └── dllmain_dispatch()                 <── [CRT] Điều phối khởi tạo môi trường
           │
           ▼
2. __scrt_dllmain_crt_process_attach()    <── [CRT] Khởi tạo C Runtime, bảng luồng
   ├── _initterm_e() / _initterm()        <── [CRT] Gọi các hàm khởi tạo biến C++ toàn cục
   └── (*(code *)*plVar6)()               <── Gọi con trỏ hàm lưu tại DAT_180004690
           │
           ▼
3. DllMain của lập trình viên (FUN_1800011a0) <── [USER CODE] BẮT ĐẦU LOGIC THỰC SỰ
   ├── GetModuleFileNameA()               <── Kiểm tra tên tiến trình ("dreamhack.exe")
   ├── ROL bit từ chuỗi "drea"            <── Khởi tạo 16 giá trị seed
   ├── FUN_180001010()                    <── Nạp Seed vào State Array
   ├── FUN_180001060() (x100 lần)         <── Thuật toán PRNG WELL512a (Warmup)
   ├── Phép XOR 5 khối dword              <── Giải mã ciphertext thành Flag
   └── MessageBoxA()                      <── Hiển thị Flag
```

---

## 6. Chiến Lược Reverse Engineering Nhanh Cho File DLL

1. **Không đi tuần tự từ `entry()`:** Tránh bị lạc vào hàng chục hàm khởi tạo CRT của Microsoft (`__scrt_*`, `_initterm`, `startup_lock`).
2. **Quét bảng Imports:** Tìm các Win32 API quan trọng thể hiện hành vi:
   * Chống dịch ngược/Debug: `IsDebuggerPresent`, `CheckRemoteDebuggerPresent`.
   * Kiểm tra môi trường: `GetModuleFileNameA`, `PathFindFileNameA`, `CreateToolhelp32Snapshot`.
   * Tương tác/Xuất dữ liệu: `MessageBoxA`, `WriteProcessMemory`, `CreateFileA`, `InternetOpenA`.
3. **Sử dụng Xref (Cross-References - `Ctrl + X`):** 
   * Tìm đến chuỗi nghi vấn (`flag`, `error`, `license`) hoặc các API quan trọng.
   * Nhấn `Ctrl + X` để nhảy thẳng vào hàm logic của người ra đề (thường nằm ở dải địa chỉ thấp như `FUN_180001000` -> `FUN_180001300`).
4. **Tách biệt thuật toán để Re-script:** Nhận diện các cấu trúc mật mã / PRNG (như WELL512a, RC4, AES S-Box, XOR key loop) và viết lại bằng Python để giải mã tĩnh (Static Solve) thay vì phải setup môi trường chạy động phức tạp.