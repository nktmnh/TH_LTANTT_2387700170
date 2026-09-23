# LAB 1: INPUT VALIDATION & SANITIZATION
*(Theo hướng dẫn giáo trình Trang 11 – 19)*

## 1. Mục tiêu
- Áp dụng nguyên tắc **"Không tin tưởng dữ liệu đầu vào của người dùng" (Never trust user input)**.
- Phân biệt và kết hợp 2 kỹ thuật:
  - **Validation**: Đảm bảo dữ liệu đúng định dạng mong đợi (Email, URL, Filename).
  - **Sanitization & Escaping**: Loại bỏ và mã hóa các ký tự nguy hiểm (SQL Injection, XSS).

## 2. Triển khai kỹ thuật (securevalidator/core.py)
- **alidate_email**: Dùng Regex `r'^[\w\.-]+@[\w\.-]+\.\w+$'` và loại trừ `..` (RFC 5322).
- **alidate_url**: Dùng `urllib.parse.urlparse`, chỉ cho phép scheme `http`, `https` và có domain/netloc (chống SSRF cơ bản).
- **alidate_filename**: Chặn `..`, `/`, `\\` và so sánh `os.path.basename(filename) == filename` (chống Path Traversal).
- **sanitize_sql_input**: Lọc bỏ dấu nháy (`'`, `"`), dấu chú thích (`--`, `#`), dấu chấm phẩy (`;`) và các từ khóa SQL.
- **sanitize_html_input**: Dùng `html.escape()` chuyển đổi ký tự đặc biệt sang HTML Entities để vô hiệu hóa mã JavaScript độc hại.

## 3. Cấu trúc thư mục
- `app.py`: Web Flask tiếp nhận dữ liệu.
- `securevalidator/core.py`: Thư viện bảo mật lõi chứa 5 hàm xử lý.
- `templates/index.html`: Giao diện web sử dụng PicoCSS.
- `tests/test_validators.py`: Bộ 10 Unit Tests.

## 4. Hướng dẫn chạy và kiểm thử
### Khởi chạy ứng dụng Web
`ash
pip install -r requirements.txt
python app.py
`
Truy cập: http://127.0.0.1:5000

### Chạy Unit Test
`ash
python -m unittest discover tests
`
-> Kết quả mong đợi: 10/10 test cases PASS (OK).
