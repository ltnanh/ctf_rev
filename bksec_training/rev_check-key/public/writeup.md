# check key 

- Category : rev 

Challenge give me a .exe file , I tried running the file 
```bash
Enter password: 12233143
Try again to be handsome
```

It seem that we need to find the password ( for flag?). So I used Ghidra to decompile the .exe . The excutable file is quite small , and from the function graph call , `FUN_00101110` called by `entry` seem to contain the whole logic 

```c++
bool FUN_00101110(void)

{
    undefined1 (*pauVar1) [16];
    undefined1 (*pauVar2) [16];
    int iVar3;
    int iVar4;
    undefined1 auVar5 [13];
    undefined1 auVar6 [14];
    undefined1 auVar7 [15];
    undefined1 auVar8 [15];
    undefined1 auVar9 [15];
    undefined1 auVar10 [13];
    undefined1 auVar11 [13];
    undefined1 auVar12 [13];
    undefined1 auVar13 [14];
    undefined1 auVar14 [15];
    undefined1 auVar15 [13];
    undefined1 auVar16 [14];
    undefined1 auVar17 [15];
    undefined1 auVar18 [15];
    undefined1 auVar19 [15];
    undefined1 auVar20 [15];
    unkuint9 Var21;
    undefined1 auVar22 [11];
    undefined1 auVar23 [13];
    undefined1 auVar24 [13];
    undefined1 auVar25 [14];
    undefined1 auVar26 [15];
    undefined1 auVar27 [15];
    istream *piVar28;
    long lVar29;
    long in_FS_OFFSET;
    bool bVar30;
    uint uVar31;
    undefined1 auVar32 [16];
    undefined1 auVar33 [16];
    undefined1 auVar34 [14];
    undefined1 auVar35 [16];

    undefined1 *local_48;
    long local_40;
    undefined1 local_38 [24];
    long local_20;
    
    local_20 = *(long *)(in_FS_OFFSET + 0x28);
    local_48 = local_38;
    local_38[0] = 0;
    local_40 = 0;

    std::__ostream_insert<>((ostream *)std::cout,"Enter password: ",0x10);
    piVar28 = std::operator>>((istream *)std::cin,(string *)&local_48);

    if ((((byte)piVar28[*(long *)(*(long *)piVar28 + -0x18) + 0x20] & 5) == 0) && (local_40 == 0x40))
    {
        lVar29 = 0;
        auVar35 = (undefined1  [16])0x0;

        do {
            pauVar1 = (undefined1 (*) [16])(&DAT_00102060 + lVar29);
            pauVar2 = (undefined1 (*) [16])(local_48 + lVar29);
            lVar29 = lVar29 + 0x10;
            auVar32 = *pauVar1 ^ _DAT_001020a0 ^ *pauVar2;

            uVar31 = CONCAT13(0,CONCAT12(auVar32[9],(ushort)auVar32[8]));
            auVar7[0xd] = 0;
            auVar7._0_13_ = auVar32._0_13_;
            auVar7[0xe] = auVar32[7];
            auVar8[0xc] = auVar32[6];
            auVar8._0_12_ = auVar32._0_12_;
            auVar8._13_2_ = auVar7._13_2_;
            auVar9[0xb] = 0;
            auVar9._0_11_ = auVar32._0_11_;
            auVar9._12_3_ = auVar8._12_3_;
            auVar14[10] = auVar32[5];
            auVar14._0_10_ = auVar32._0_10_;
            auVar14._11_4_ = auVar9._11_4_;
            auVar17[9] = 0;
            auVar17._0_9_ = auVar32._0_9_;
            auVar17._10_5_ = auVar14._10_5_;
            auVar18[8] = auVar32[4];
            auVar18._0_8_ = auVar32._0_8_;
            auVar18._9_6_ = auVar17._9_6_;
            auVar20._7_8_ = 0;
            auVar20._0_7_ = auVar18._8_7_;
            Var21 = CONCAT81(SUB158(auVar20 << 0x40,7),auVar32[3]);
            auVar26._9_6_ = 0;
            auVar26._0_9_ = Var21;
            auVar22._1_10_ = SUB1510(auVar26 << 0x30,5);
            auVar22[0] = auVar32[2];
            auVar27._11_4_ = 0;
            auVar27._0_11_ = auVar22;
            auVar23._1_12_ = SUB1512(auVar27 << 0x20,3);
            auVar23[0] = auVar32[1];
            auVar19[1] = 0;
            auVar19[0] = auVar32[0];
            auVar19._2_13_ = auVar23;
            auVar5._1_3_ = 0;
            auVar5[0] = auVar32[0xc];
            auVar5[4] = auVar32[0xd];
            auVar5._5_3_ = 0;
            auVar5[8] = auVar32[0xe];
            auVar5._9_3_ = 0;
            auVar5[0xc] = auVar32[0xf];
            auVar10[0xc] = auVar32[0xb];
            auVar10._0_12_ = ZEXT112(auVar32[0xc]) << 0x40;
            auVar11._10_3_ = auVar10._10_3_;
            auVar11._0_10_ = (unkuint10)auVar32[10] << 0x40;
            auVar24._5_8_ = 0;
            auVar24._0_5_ = auVar11._8_5_;
            auVar12[4] = auVar32[9];
            auVar12._0_4_ = uVar31;
            auVar12[5] = 0;
            auVar12._6_7_ = SUB137(auVar24 << 0x40,6);
            auVar15._4_9_ = auVar12._4_9_;
            auVar15._0_4_ = uVar31 & 0xffff;
            auVar33._13_3_ = 0;
            auVar33._0_13_ = auVar5 | auVar15;
            auVar34._2_2_ = 0;
            auVar34._0_2_ = auVar18._8_2_;
            auVar34._4_2_ = auVar14._10_2_;
            auVar34._6_2_ = 0;
            auVar34._8_2_ = auVar8._12_2_;
            auVar34._10_2_ = 0;
            auVar34[0xc] = auVar32[7];
            auVar34[0xd] = 0;
            auVar6._10_2_ = 0;
            auVar6._0_10_ = auVar19._0_10_;
            auVar6._12_2_ = (short)Var21;
            auVar25._2_4_ = auVar6._10_4_;
            auVar25._0_2_ = auVar22._0_2_;
            auVar25._6_8_ = 0;
            auVar13._4_2_ = auVar23._0_2_;
            auVar13._0_4_ = auVar19._0_4_;
            auVar13._6_8_ = SUB148(auVar25 << 0x40,6);
            auVar16._4_10_ = auVar13._4_10_;
            auVar16._0_4_ = auVar19._0_4_ & 0xffff;
            auVar32._14_2_ = 0;
            auVar32._0_14_ = auVar34 | auVar16;
            auVar35 = auVar35 | auVar33 | auVar32;
        } while (lVar29 != 0x40);

        auVar35 = auVar35 | auVar35 >> 0x40;
        iVar3 = auVar35._0_4_;
        iVar4 = auVar35._4_4_;

        if (iVar3 == 0 && iVar4 == 0) {
            std::__ostream_insert<>((ostream *)std::cout,"You are handsome\n",0x11);
        }
        else {
            std::__ostream_insert<>((ostream *)std::cout,"Try again to be handsome\n",0x19);
        }
        bVar30 = iVar3 != 0 || iVar4 != 0;
    }


    else {
        std::__ostream_insert<>((ostream *)std::cout,"Try again to be handsome\n",0x19);
        bVar30 = true;
    }


    std::__cxx11::string::_M_dispose();

    if (local_20 == *(long *)(in_FS_OFFSET + 0x28)) {
        return bVar30;
    }
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
}
```

The deompiled C++ code is complicated . However  , the logic of the code look like this C++ code for simplification 

```c
#include <iostream>
#include <string>

int main() {
    std::string password;
    std::cout << "Enter password: ";
    std::cin >> password;

    if (password.length() != 64) {
        std::cout << "Try again to be handsome\n";
        return 1;
    }

    unsigned char DAT_00102060[64] // A global variable 
    unsigned char _DAT_001020a0[16] //A global variable 

    unsigned char auVar35 = 0; 


    for (int i = 0; i < 64; i += 16) {
        for (int j = 0; j < 16; j++) {    
            unsigned char auVar32 = password[i + j] ^ DAT_00102060[i + j] ^ _DAT_001020a0[j];        
            auVar35 = auVar35|auVar32; 
        }
    }

    // if (iVar3 == 0 && iVar4 == 0)
    if (auVar35 == 0) {
        std::cout << "You are handsome\n";
    } else {
        std::cout << "Try again to be handsome\n";
    }

    return 0;
}
```

So that , to success (`You are handsome`) , we need to give a password ( may be this is flag) so that after the loop , `auVar35` will be `0`. This mean that for each interation , `auVar32 = password[i + j] ^ DAT_00102060[i + j] ^ _DAT_001020a0[j] = 0 `

The thing we need is find value of `DAT_00102060` and `_DAT_001020a0` in file to reverse the true passowrd 


```python
DAT_00102060 = "0b021a0c0a322a217a2a2216227a30162a3b7d2a227a2d167f2f782d7d7f2a2d7f7c7c7e7d7a712b7c707f717d2c7d2a7e787e2b2a717d2d792d7d702d7b7b34" 

DAT_001020a0 = "49494949494949494949494949494949"

data = bytes.fromhex(DAT_00102060)
key = bytes.fromhex(DAT_001020a0)

flag = ''
for i in range(64):
    flag += chr(data[i] ^ key[i % 16])

print(flag) 
```

And as I guess , password is the flag 

```
BKSEC{ch3ck_k3y_cr4ck3d_6f1d46cd6557438b59684e4c717bc84d0d49d22}
```
