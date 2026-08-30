# Secret Message 

- category : rev 
- Dreamhack 
- Difficulty : easy - level 1 


## 1 , Tổng quan về challenge 

- challenge đưa cho chúng ta 3 file , file thực thi `prob` , `imageviewer` và `secretMessage.enc`

- `imageviewer`
    ```python
    import sys
    # pip install pillow
    from PIL import Image

    if len(sys.argv) != 2:
        print(f"python {sys.argv[0]} <secretMessage.raw>")
    else:
        with open(sys.argv[1], "rb") as f:
            output = f.read()
            Image.frombytes("1", (500, 50), output).show()
    ```
    - Khả năng cao là file secretMessage.raw chính là file ảnh chứa flag mà ta cần khôi phục từ secretMessage.enc được cho , và logic khôi phục nằm trong file prob  


- Khảo sát file : 
```bash
file prob
prob: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=afc20364a7c42c723bd1715bf513330d7ad5db86, stripped
```

## 2 , Decompile and solve 
sau khi decompile ra các function , hàm entry dẫn ta tới 1 hàm 

```c
undefined8 FUN_00100911(void)

{
  FILE *__stream;
  FILE *__stream_00;
  
  __stream = fopen("secretMessage.raw","rb");
  __stream_00 = fopen("secretMessage.enc","wb");
  FUN_001007fa(__stream,__stream_00);
  remove("secretMessage.raw");
  puts("done!");
  fclose(__stream_00);
  fclose(__stream);
  return 0;
}
```
=>Có thể thấy secretMessage.raw là thứ ta cần tìm , ta sẽ đi tiếp để tìm logic 

```c
undefined8 FUN_001007fa(FILE *param_1,FILE *param_2)

{
  int iVar1;
  int *piVar2;
  undefined8 uVar3;
  byte local_11;
  int local_10;
  int local_c;
  
  if ((param_1 == (FILE *)0x0) || (param_2 == (FILE *)0x0)) {
    piVar2 = __errno_location();
    *piVar2 = 2;
    uVar3 = 0xffffffff;
  }
  else {
    local_c = -1;
    local_11 = 0;
    do {
      local_10 = fgetc(param_1);
      if (local_10 == -1) goto LAB_0010090a;
      fputc(local_10,param_2);
      iVar1 = local_10;
      if (local_10 == local_c) {
        local_11 = 0;
        do {
          local_10 = fgetc(param_1);
          iVar1 = local_c;
          if (local_10 == -1) goto LAB_001008d7;
          if (local_10 != local_c) {
            fputc((uint)local_11,param_2);
            fputc(local_10,param_2);
            iVar1 = local_10;
            goto LAB_001008d7;
          }
          local_11 = local_11 + 1;
        } while (local_11 != 0xff);
        fputc(0xff,param_2);
        local_c = -1;
        iVar1 = local_c;
      }
LAB_001008d7:
      local_c = iVar1;
    } while (local_10 != -1);
    fputc((uint)local_11,param_2);
LAB_0010090a:
    uVar3 = 0;
  }
  return uVar3;
}
```

Thuật toán trong hàm FUN_001007fa thực chất là một biến thể của Run-Length Encoding (RLE) (nén độ dài lặp):

- Khi có 2 byte liên tiếp giống nhau được ghi ra, byte thứ 3 kế tiếp trong file .enc chính là số lượng byte lặp lại thêm (tối đa 0xFF = 255).

- Nếu byte đếm này bằng 0, nghĩa là chỉ có đúng 2 byte đó; nếu bằng k, nghĩa là có 2 + k byte giống nhau.


Ta có thể dễ dàng khôi phục lại secretMessage.raw từ secretMessage.enc qua đoạn code 
```python
def decompress_rle(enc_data: bytes) -> bytes:
    raw = bytearray()
    prev = -1
    i = 0
    n = len(enc_data)

    while i < n:
        b = enc_data[i]
        i += 1
        raw.append(b)

        # Khi gặp 2 byte liên tiếp giống nhau, byte kế tiếp là số lượng byte lặp thêm
        if b == prev:
            if i < n:
                count = enc_data[i]
                i += 1
                raw.extend([b] * count)
            prev = -1  # Reset trạng thái
        else:
            prev = b

    return bytes(raw)
```

Sau khi mà khôi phục được file raw,  xem ảnh flag qua đoạn code mà chal cho 
```python
def main():
    enc_file = "secretMessage.enc"
    raw_file = "secretMessage.raw"

    try:
        with open(enc_file, "rb") as f:
            enc_data = f.read()
    except FileNotFoundError:
        print(f"[-] Không tìm thấy file {enc_file}")
        return

    raw_data = decompress_rle(enc_data)

    with open(raw_file, "wb") as f:
        f.write(raw_data)
    print(
        f"[+] Đã khôi phục thành công {raw_file} ({len(raw_data)} bytes)!"
    )

    # 4. Hiển thị ảnh chứa Flag 
    try:
        img = Image.frombytes("1", (500, 50), raw_data)
        img.show()
        img.save("flag.png")
    except Exception as e:
        print(f"[-] Lỗi khi hiển thị ảnh: {e}")


if __name__ == "__main__":
    main()
```

Chạy code và ảnh flag sẽ hiện lên 



