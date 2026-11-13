
DAT_00102060 = "0b021a0c0a322a217a2a2216227a30162a3b7d2a227a2d167f2f782d7d7f2a2d7f7c7c7e7d7a712b7c707f717d2c7d2a7e787e2b2a717d2d792d7d702d7b7b34" 

DAT_001020a0 = "49494949494949494949494949494949"

data = bytes.fromhex(DAT_00102060)
key = bytes.fromhex(DAT_001020a0)

flag = ''
for i in range(64):
    flag += chr(data[i] ^ key[i % 16])

print(flag) 