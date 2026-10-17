# Handout manifest — Ring Zero Whisper

Thư mục này chỉ chứa hiện vật được phát cho đội chơi. Không đặt cờ rõ, lời giải,
source generator, seed, dữ liệu chuẩn đối chiếu hoặc tệp debug tại đây.

| Tệp bắt buộc | Mô tả bổ sung | Trạng thái |
|---|---|---|
| `loader` | stripped ELF | `2a14745e054942fb6f85c1b2a55272a9b60dce5029968c0d81dc490f29cbcb44` |
| `programs.bpf` | — | `6ee2aa176944cad9763647c6e879a3a66e27958bfc9e830942f5c93a6dd0c1be` |
| `vmlinux.btf` | — | `63d577ac268ff572f26c527950fae2b2a84fe9559350d14a88f583cfdec6d934` |
| `bpftool.json` | — | `eaf76a818ee935297ebea2f0208b2ba3da681dabb29e42e40fdbc67516d707c5` |
| `ringbuf.dump` | — | `6608ddbde3a6f04660096397c093b736382ae135fc2590ee7cc342738e8b1052` |
| `dns.pcapng` | — | `5e5ba89f39097e1737059e316009ecfc592aec241167fce535654a412cd6b943` |
| `flag.enc` | — | `25aaf1a0af91a86875f8a119b635238c81dc44239552dbb6d304f1ba4d1e7b47` |
| `verify.py` | — | `271fd13d5162b78c3788f584db25e8327a22ca631028ce5674dca77218487e7a` |
| `FORMAT.md` | — | `070e7687d9cf37325d49ece506b121a5cf709e628ca3c551088d305f199d9261` |
| `SHA256SUMS` | SHA-256 của toàn bộ handout | `71314890d4b7a1673db736d47a5bca2008ef2e3c60b0fe7231bf89071e1ab621` |

Các cột trạng thái đã được thay bằng SHA-256 sau khi generator tạo hiện vật cuối.
Trình đóng gói sẽ từ chối phát hành nếu còn thiếu bất kỳ tệp bắt buộc nào.
