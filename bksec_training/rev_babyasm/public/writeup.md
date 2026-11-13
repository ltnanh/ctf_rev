# babyasm

## 1 Overview

The challenge provides an x86 32-bit Assembly function

```asm
.intel_syntax noprefix
.globl babyasm

babyasm:
    push ebp
    mov ebp, esp
    xor eax, eax
    mov ah, BYTE PTR [ebp+0x9]
    shl ax, 0x10
    sub al, BYTE PTR [ebp+0xe]
    add ah, BYTE PTR [ebp+0xf]
    xor ax, WORD PTR [ebp+0x12]
    pop ebp
    ret
```
and asks us to calculate its return value for the following three arguments, in order:

- `0x4a8101c7`
- `0x80e5ef50`
- `0x47f303e2`

This chall is really simple cause we only need to assemble chall.S to chall.o by using `gcc -masm=intel -m32 -c babyasm.S -o babyasm.o` . Then decompile it to read pseudo code C . But this simple chal is realley a good opportunity to practice read assembly:v 

## 2 Analyzing the Assembly Code

The return value will be in `eax` , a 32 bit register contain :
- 16 bit `AX` at its low bits
- 8 bit `AH` at `AX` high bits
- 8 bit `AL` at `AX` low bits 

### Instruction breakdown

- `push ebp`: Saves the previous EBP value on the stack. ESP decreases by 4 bytes.
- `mov ebp, esp`: Establishes EBP as the stack frame reference.
- `xor eax, eax`: Clears EAX by setting it to zero.
- `mov ah, BYTE PTR [ebp+0x9]`: Reads one byte from address EBP + 9 into AH.
- `shl ax, 0x10`: Shifts the 16-bit AX register left by 16 bits, resulting in zero.
- `sub al, BYTE PTR [ebp+0xe]`: Subtracts the byte at EBP + 0xE from AL.
- `add ah, BYTE PTR [ebp+0xf]`: Adds the byte at EBP + 0xF to AH.
- `xor ax, WORD PTR [ebp+0x12]`: XORs AX with a 16-bit word starting at EBP + 0x12.
- `pop ebp`: Restores the previous EBP value.
- `ret`: Returns execution to the caller.



## 3. Mapping the Arguments to Stack Memory

Assuming the function uses the 32-bit x86 cdecl calling convention, the arguments are located at `[ebp+8]`, `[ebp+12]`, and `[ebp+16]`.The memory look like this

```bash
             
+---------------------------+
| Argument 2                |  EBP + 12  (0x1008)
+---------------------------+
| Argument 1                |  EBP + 8   (0x1004)
+---------------------------+
| Return address            |  EBP + 4   (0x1000)
+---------------------------+
| old EBP                   |  EBP + 0   (0x0FFC)  <- EBP
+---------------------------+
|                           |  EBP - 4   (0x0FF8)
+---------------------------+
|                           |  EBP - 8   (0x0FF4)
+---------------------------+
```

x86 uses LSB , so that we have
- Argument 1: `0x4a8101c7`

    | Offset | Byte value |
    |---|---|
    | `[ebp+0x8]` | `0xc7` |
    | `[ebp+0x9]` | `0x01` |
    | `[ebp+0xa]` | `0x81` |
    | `[ebp+0xb]` | `0x4a` |

- Argument 2: `0x80e5ef50`

    | Offset | Byte value |
    |---|---|
    | `[ebp+0xc]` | `0x50` |
    | `[ebp+0xd]` | `0xef` |
    | `[ebp+0xe]` | `0xe5` |
    | `[ebp+0xf]` | `0x80` |

- Argument 3: `0x47f303e2`

    | Offset | Byte value |
    |---|---|
    | `[ebp+0x10]` | `0xe2` |
    | `[ebp+0x11]` | `0x03` |
    | `[ebp+0x12]` | `0xf3` |
    | `[ebp+0x13]` | `0x47` |

The function accesses the following values:

- `[ebp+0x9]` = `0x01`
- `[ebp+0xe]` = `0xe5`
- `[ebp+0xf]` = `0x80`
- `WORD PTR [ebp+0x12]` = `0x47f3`



## 4 Compute return value 

- Initialize EAX

    ```asm
    xor eax, eax
    ```

    The result is:

    ```text
    EAX = 0x00000000
    AX  = 0x0000
    AH  = 0x00
    AL  = 0x00
    ```


- Read the byte at `[ebp+0x9]`

    ```asm
    mov ah, BYTE PTR [ebp+0x9]
    ```

    The byte at this address is `0x01`.

    ```text
    AH  = 0x01
    AL  = 0x00
    AX  = 0x0100
    EAX = 0x00000100
    ```

- Shift AX left by 16 bits

    ```asm
    shl ax, 0x10
    ```


    ```text
    AX  = 0x0000
    EAX = 0x00000000
    ```


- Subtract the byte at `[ebp+0xe]`

    ```asm
    sub al, BYTE PTR [ebp+0xe]
    ```


    Since AL is an 8-bit register, the result wraps around modulo 256:

    ```text
    AL = (0x00 - 0xe5) mod 0x100 = 0x1b
    ```

    The resulting register values are:

    ```text
    AX = 0x001b
    ```

- Add the byte at `[ebp+0xf]`

    ```asm
    add ah, BYTE PTR [ebp+0xf]
    ```



    ```text
    AH = 0x00 + 0x80 = 0x80
    ```

    Combining AH and AL gives:

    ```text
    AH  = 0x80
    AL  = 0x1b
    AX  = 0x801b
    EAX = 0x0000801b
    ```

- XOR with the word at `[ebp+0x12]`

    ```asm
    xor ax, WORD PTR [ebp+0x12]
    ```



    Perform the XOR operation:

    ```text
        0x801b
    XOR 0x47f3
    -----------
        0xc7e8
    ```

    The final register values are:

    ```text
    AX  = 0xc7e8
    EAX = 0x0000c7e8
    ```

## 5. Conclusion

The function returns the value stored in EAX , which is

```text
0x0000c7e8
```

The flag to submit is:

```text
BKSEC{0xc7e8}
```