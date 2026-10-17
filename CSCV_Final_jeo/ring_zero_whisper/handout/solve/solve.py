import base64
import hashlib
import json
from pathlib import Path


# 1. Khai báo các chuỗi Base32 nhận được từ DNS query
fragment_labels = [
    "DMMOG4EMDTGT2",
    "FBK3RWPYSKZV2",
    "W6KVUGZAOX43I"
]
parity_label = "R5PVZKUMKM5AC"

def decode_base32(b32_str):
    b32_str = b32_str.upper()
    missing_padding = len(b32_str) % 8
    if missing_padding:
        b32_str += '=' * (8 - missing_padding)
    return base64.b32decode(b32_str)


decoded_fragments = [decode_base32(frag) for frag in fragment_labels]
decoded_parity = decode_base32(parity_label)



# Khôi phục mảnh bị thiếu (XOR Erasure Repair)
block_size = len(decoded_parity)
erased_fragment = bytearray(block_size)

for i in range(block_size):
    xor_value = decoded_parity[i]
    for frag in decoded_fragments:
        xor_value ^= frag[i]
    erased_fragment[i] = xor_value

erased_fragment = bytes(erased_fragment)


# Concatenate in sequence order
all_fragments = [decoded_fragments[0], erased_fragment, decoded_fragments[1], decoded_fragments[2]]

cipher = b"".join(all_fragments)


# gen key stream 
uid = 1001
session_bit = 1
parent_hash = "ab77fe24675b6427"
boot_id = b"28f227e7-123e-e84f-c023-fc215e94e7d2"

data = {"uid": uid, "session_bit": session_bit, "parent_hash": parent_hash}
canonical_json = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()

key = hashlib.sha256(canonical_json + boot_id).digest()

keystream = b""
i = 0
while len(keystream) < len(cipher):
    counter_bytes = i.to_bytes(4, "big")
    block = hashlib.sha256(key + counter_bytes).digest()
    keystream += block
    i += 1

keystream = keystream[:len(cipher)]


# XOR cipher vs keystream để decrypt
payload = bytes(c ^ k for c, k in zip(cipher, keystream))

Path("/home/nhat-anh/ctf/cscv_2026/rev_final/REV04/handout/sovle/recovered.bin").write_bytes(payload)
print("Đã ghi payload ra file 'recovered.bin'")