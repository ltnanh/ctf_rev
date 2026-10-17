# Ring Zero Whisper

> `REV-02` · Dịch ngược · 180-240 phút

## Bối cảnh

Trình nạp giám sát hợp lệ cài nhiều chương trình eBPF. Không lâu sau, nội dung một số phiên SSH xuất hiện trong lưu lượng DNS. Không phải tất cả lệnh đều bị ghi — chỉ những lệnh khớp một bộ tiêu chí nhất định.

Xác định quy tắc chọn lệnh, khôi phục dữ liệu đã bị truyền đi, và chứng minh toàn bộ chuỗi hoạt động.

## Tệp được cấp

`loader` · `programs.bpf` · `vmlinux.btf` · `bpftool.json` · `ringbuf.dump` · `dns.pcapng` · `flag.enc` · `verify.py` · `FORMAT.md`

## Nộp

`verify.py --proof proof.json --payload recovered.bin`

## Gợi ý

- T+100′: Đừng phân tích rời từng chương trình — dựng đồ thị xuyên chuỗi.
- T+170′: Một số mảnh DNS bị mất nhưng có thể khôi phục.
