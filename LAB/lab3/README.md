# LAB 3: THỰC HÀNH GHI NHẬT KÝ ƯU TIÊN BẢO MẬT
*(Theo hướng dẫn giáo trình Trang 26 – 31)*

## 1. Mục tiêu
- Xây dựng hệ thống ghi nhật ký an toàn (`SecureLogger`) theo tiêu chuẩn lập trình bảo mật.
- Hỗ trợ đa cấp độ log (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
- Tự động phát hiện và che giấu thông tin định danh cá nhân (PII Data Masking).
- Quản lý luân phiên log (Log Rotation) kèm nén dữ liệu bằng GZip.
- Phát hiện thay đổi trái phép trên tập tin nhật ký (Tamper Detection qua chữ ký SHA-256).
- Ghi nhật ký theo cấu trúc JSON chống tấn công Log Injection / CRLF Injection.

## 2. Triển khai kỹ thuật (`securelogger/logger.py`)
- **`mask_pii(text)`**: Sử dụng Regex nhận diện Email và Password/Token, tự động thay thế bằng `<email_masked>`, `<token_masked>`.
- **`JSONFormatter`**: Chuyển đổi mọi bản ghi log thành chuỗi JSON một dòng duy nhất, lưu timestamp chuẩn ISO 8601 UTC.
- **`hash_line(line)` & `append_signature(line)`**: Tính mã băm SHA-256 cho từng dòng log và ghi vào file chữ ký `secure.log.sig`.
- **`GZipRotator` & `SecureRotatingFileHandler`**: Tự động luân phiên file khi dung lượng đạt 1MB và nén thành tệp `.gz`.

## 3. Cấu trúc thư mục
- `app.py`: API POST `/validate` tiếp nhận dữ liệu và ghi log.
- `securelogger/logger.py`: Module ghi nhật ký an toàn xử lý PII Masking, Hash, Rotation.
- `securevalidator/core.py`: Kế thừa module kiểm tra đầu vào từ Lab 1.
- `tests/test_logger.py`: Bộ 4 Unit Tests.

## 4. Hướng dẫn chạy và kiểm thử
### Khởi chạy API
`ash
pip install -r requirements.txt
python app.py
`
Gửi POST request tới: http://127.0.0.1:5000/validate với payload JSON để kiểm tra ứng dụng.

### Chạy Unit Test
`ash
python -m unittest discover tests
`
-> Kết quả mong đợi: 4/4 test cases PASS (OK).
