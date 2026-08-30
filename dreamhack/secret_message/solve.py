import sys
from PIL import Image


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