# FORMAT
proof.json fields: attach_points, prog_chain, map_ids, uid, parent_hash, session_bit. 

recovered.bin = the recovered stream bytes.

programs.bpf = eBPF object thật (ELF, clang -target bpf). Selector tuple nằm trong `.rodata` const: đọc bằng pyelftools — BTF xác định tập biến selector + bố cục kiểu (sel/parent_hash/attach_points thuộc datasec .rodata), còn *offset* trong `.rodata` lấy từ ELF symbol table (st_value = offset section). 

Lưu ý: clang BTF datasec offset cho global luôn bằng 0 ở object level — dùng `readelf -s` + `readelf -x .rodata`. `parent_hash` lưu dạng RAW 8 BYTE (không phải chuỗi ASCII) — đọc 8 byte rồi `.hex()` để lấy chuỗi 16 hex đáp án; `sel` = struct {u32 uid; u8 session_bit}.


The loader prints the boot id; run it. 

map_ids/prog_id come from bpftool.json.

Recover the stream: `dns.pcapng` is a REAL capture — parse the DNS queries; each QNAME carries a fragment label `f<seq>.c<count>.<base32>.rzw-frag.ctf` or the parity label `p<miss>.l<len>.<base32>.rzw-par.ctf`; Base32-decode each label, repair the erased fragment from parity (XOR erasure), concatenate in sequence order, then XOR-decrypt.

Stream key = SHA-256(canonical JSON of {uid, session_bit, parent_hash} + boot-id); keystream block i = SHA-256(key || i as 4-byte big-endian); payload = cipher XOR keystream. 

Write the payload bytes to recovered.bin.
