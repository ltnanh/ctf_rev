import struct

gadgets = {
    0x0: 'ret',
    0x1: 'leave; ret',
    0x3: 'pop rax; ret',
    0x5: 'pop rdi; ret',
    0x7: 'pop rsi; ret',
    0x9: 'pop rdx; ret',
    0xb: 'syscall; ret',
    0xe: 'xor rax, rax; mov al, [rdi]; ret',
    0x14: 'sub al, dil; ret',
    0x18: 'pop rbp; ret',
    0x1a: 'imul rdi, rax; ret',
    0x1f: 'add rsp, rax; ret',
    0x23: 'mov rax, 0; mov rax, [rax]; ret',
    0x2e: 'xor rcx, rcx; ret',
    0x32: 'add rax, rcx; ret',
    0x36: 'mov rdi, rax; ret',
    0x3a: 'mov rcx, rax; ret',
    0x3e: 'mov rax, rcx; ret',
    0x42: 'pop rcx; ret',
    0x44: 'mov [rdi], al; ret',
    0x47: 'imul rax, rdx; ret',
    0x4c: 'mov rdx, rax; ret',
    0x50: 'mov rax, rdx; ret',
    0x54: 'idivl [rdi]; ret',
    0x57: 'nop; ret'
}

OPCODE_BASE = 0x1224000
CHAIN_BASE = 0x1225000

with open('chain', 'rb') as f:
    data = f.read()

entries = []
for i in range(0, len(data), 8):
    val = struct.unpack('<Q', data[i:i+8])[0]
    entries.append(val)

with open('chain_parsed.txt', 'w') as out:
    for idx, val in enumerate(entries):
        addr = CHAIN_BASE + idx * 8
        if OPCODE_BASE <= val < OPCODE_BASE + 0x60:
            offset = val - OPCODE_BASE
            gname = gadgets.get(offset, f'unknown_gadget_{offset:#x}')
            out.write(f'{addr:#x} [{idx:04d}]: {val:#x} -> GADGET: {gname}\n')
        else:
            out.write(f'{addr:#x} [{idx:04d}]: {val:#x}\n')
