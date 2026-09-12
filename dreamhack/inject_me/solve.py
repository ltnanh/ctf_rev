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