# BÁO CÁO THỰC HÀNH LAB: CƠ SỞ LẬP TRÌNH BẢO MẬT

- **Môn học**: Lập trình an toàn / Bảo mật ứng dụng Web
- **Học viên thực hiện**: Võ Nhật Minh
- **MSSV**: 2387700170
- **Các bài thực hành trong LAB**:
  - **Lab 1**: Xác thực & làm sạch dữ liệu đầu vào (Input Validation & Sanitization - Trang 11 đến 19)
  - **Lab 2**: An toàn mã nguồn với Git Hooks (Mục 1.4 Thực hành: Git Security Hook - Trang 20 đến 25)
  - **Lab 3**: Hệ thống ghi nhật ký ưu tiên bảo mật (Mục 1.6 Thực hành: Secure Logger - Trang 26 đến 31)

---

## 📁 CẤU TRÚC BÀI NỘP LAB

```text
LAB/
├── README.md                      # Báo cáo chi tiết toàn bộ Buổi 1 (Lab 1, Lab 2, Lab 3)
│
├── lab1/                          # LAB 1: XÁC THỰC & LÀM SẠCH ĐẦU VÀO (Trang 11-19)
│   ├── .gitignore
│   ├── requirements.txt           # Flask==2.3.3, gunicorn==21.2.0
│   ├── render.yaml                # Cấu hình deploy Cloud Render
│   ├── app.py                     # Web Flask tiếp nhận dữ liệu
│   ├── securevalidator/           # Thư viện bảo mật lõi
│   │   ├── __init__.py
│   │   └── core.py                # 5 hàm Regex, SSRF, Path Traversal, SQLi, XSS
│   ├── templates/
│   │   └── index.html             # Giao diện PicoCSS
│   └── tests/
│       └── test_validators.py     # Bộ 10 Unit Tests (PASS 10/10)
│
├── lab2/                          # LAB 2: MỤC 1.4 THỰC HÀNH GIT SECURITY HOOK (Trang 20-25)
│   ├── requirements.txt           # bandit
│   ├── .githooks/
│   │   └── pre-commit             # Script hook kiểm tra mã nguồn, secrets & permissions
│   └── pre-commit-hook-test/
│       └── bad.py                 # File mẫu kiểm thử vi phạm lộ password
│
└── lab3/                          # LAB 3: MỤC 1.6 THỰC HÀNH GHI NHẬT KÝ ƯU TIÊN BẢO MẬT (Trang 26-31)
    ├── .gitignore
    ├── requirements.txt           # Flask
    ├── app.py                     # API POST /validate
    ├── securevalidator/           # Kế thừa module kiểm tra từ Lab 1
    │   ├── __init__.py
    │   └── core.py
    ├── securelogger/              # Module ghi nhật ký an toàn
    │   ├── __init__.py
    │   └── logger.py              # PII Masking, Hash SHA-256, GZip Log Rotation
    └── tests/
        └── test_logger.py         # Bộ 4 Unit Tests (PASS 4/4)
```

---

# ================================================================
# BÀI THỰC HÀNH 1 (LAB 1): INPUT VALIDATION & SANITIZATION
# ================================================================
*(Theo hướng dẫn giáo trình Trang 11 – 19)*

### 1. Mục tiêu
- Áp dụng nguyên tắc **"Không tin tưởng dữ liệu đầu vào của người dùng" (Never trust user input)**.
- Phân biệt và kết hợp 2 kỹ thuật:
  - **Validation**: Đảm bảo dữ liệu đúng định dạng mong đợi (Email, URL, Filename).
  - **Sanitization & Escaping**: Loại bỏ và mã hóa các ký tự nguy hiểm (SQL Injection, XSS).

### 2. Triển khai kỹ thuật (`lab1/securevalidator/core.py`)
- **`validate_email`**: Dùng Regex `r'^[\w\.-]+@[\w\.-]+\.\w+$'` và loại trừ `..` (RFC 5322).
- **`validate_url`**: Dùng `urllib.parse.urlparse`, chỉ cho phép scheme `http`, `https` và có domain/netloc (chống SSRF cơ bản).
- **`validate_filename`**: Chặn `..`, `/`, `\\` và so sánh `os.path.basename(filename) == filename` (chống Path Traversal).
- **`sanitize_sql_input`**: Lọc bỏ dấu nháy (`'`, `"`), dấu chú thích (`--`, `#`), dấu chấm phẩy (`;`) và các từ khóa SQL (`SELECT`, `INSERT`, `UPDATE`, `DELETE`, `DROP`, `OR`, `AND`, `UNION`, `WHERE`).
- **`sanitize_html_input`**: Dùng `html.escape()` chuyển đổi ký tự đặc biệt sang HTML Entities (`&lt;`, `&gt;`, `&quot;`, `&amp;`) để vô hiệu hóa mã JavaScript độc hại.

### 3. Kết quả kiểm thử
- **Unit Test**: `python -m unittest discover tests` $\rightarrow$ **10/10 test cases PASS (OK)**.
- **Kiểm thử trên Giao diện Web (`http://127.0.0.1:5000`)**:
  - `Email`: `nhatminh@gmail.com` $\rightarrow$ **Email hợp lệ** (Xanh)
  - `URL`: `https://www.hutech.edu.vn` $\rightarrow$ **URL hợp lệ** (Xanh)
  - `Filename`: `../../etc/passwd` $\rightarrow$ **Tên file không hợp lệ** (Đỏ)
  - `SQL Input`: `' OR 1=1 --` $\rightarrow$ **Đã lọc: 1=1**
  - `HTML Input`: `<script>alert(1)</script>` $\rightarrow$ **Đã mã hóa: `&lt;script&gt;alert(1)&lt;/script&gt;`**

---

# ================================================================
# BÀI THỰC HÀNH 2 (LAB 2): 1.4 THỰC HÀNH GIT SECURITY HOOK
# ================================================================
*(Theo hướng dẫn giáo trình Trang 20 – 25)*

### 1. Mục tiêu
- Triển khai cơ chế **Git Pre-commit Hook** nhằm tự động quét mã nguồn trước khi commit.
- Ngăn chặn lộ lọt các bí mật mã nguồn: Passwords, API Keys, Tokens, AWS Access Keys.
- Kiểm tra quyền truy cập tệp nguy hiểm (`world-writable`).
- Tích hợp công cụ **Bandit** quét lỗ hổng mức độ nghiêm trọng (High Severity).

### 2. Triển khai kỹ thuật (`lab2/.githooks/pre-commit`)
- Script Python được đăng ký làm pre-commit hook:
  ```bash
  git config core.hooksPath LAB/lab2/.githooks
  ```
- Định nghĩa danh sách biểu thức chính quy nhận diện bí mật (`SENSITIVE_PATTERNS`):
  - `apikey`: `r"(apikey)\s*[:=]\s*['"][A-Za-z0-9_-]{16,}['"]"`
  - `secret`: `r"(secret)\s*[:=]\s*['"][A-Za-z0-9_\-]{8,}['"]"`
  - `password`: `r"(password)\s*[:=]\s*['"][^'"\s]{4,}['"]"`
  - `token`: `r"(token)\s*[:=]\s*['"][A-Za-z0-9_\-]{10,}['"]"`
  - `AWS Key`: `r"(AKIA|ASIA)[A-Z0-9]{16}"`
- Xử lý tương thích môi trường Windows: Bỏ qua kiểm tra cờ POSIX `S_IWOTH` khi chạy trên hệ điều hành Windows.

### 3. Kết quả thử nghiệm chặn Commit
1. Tạo file vi phạm chứa mật khẩu: `lab2/pre-commit-hook-test/bad.py`
   ```python
   password = "super_secret_password_12345"
   ```
2. Thực hiện lệnh: `git add . && git commit -m "test bad file"`
3. **Kết quả**: Git tự động chặn và thông báo:
   ```text
   COMMIT BLOCKED by GitSecure:
    - Sensitive info found in bad.py: pattern (password)...
   ```
   Thông tin vi phạm được ghi vào file nhật ký `gitsecure.log`.

---

# ================================================================
# BÀI THỰC HÀNH 3 (LAB 3): 1.6 THỰC HÀNH GHI NHẬT KÝ ƯU TIÊN BẢO MẬT
# ================================================================
*(Theo hướng dẫn giáo trình Trang 26 – 31)*

### 1. Mục tiêu
- Xây dựng hệ thống ghi nhật ký an toàn (`SecureLogger`) theo tiêu chuẩn lập trình bảo mật.
- Đáp ứng 5 yêu cầu bắt buộc tại Mục 1.6.1:
  1. Hỗ trợ đa cấp độ log (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
  2. Tự động phát hiện và che giấu thông tin định danh cá nhân (PII Data Masking).
  3. Quản lý luân phiên log (Log Rotation) kèm nén dữ liệu bằng GZip.
  4. Phát hiện thay đổi trái phép trên tập tin nhật ký (Tamper Detection qua chữ ký SHA-256).
  5. Ghi nhật ký theo cấu trúc JSON chống tấn công Log Injection / CRLF Injection.
- Tích hợp với thư viện `SecureValidator` từ Lab 1 để ghi lại toàn bộ nhật ký các lần kiểm tra validation.

### 2. Triển khai kỹ thuật (`lab3/securelogger/logger.py`)
- **`mask_pii(text)`**: Sử dụng Regex nhận diện Email và Password/Token, tự động thay thế bằng `<email_masked>`, `<token_masked>`.
- **`JSONFormatter`**: Chuyển đổi mọi bản ghi log thành chuỗi JSON một dòng duy nhất, lưu timestamp chuẩn ISO 8601 UTC.
- **`hash_line(line)` & `append_signature(line)`**: Tính mã băm SHA-256 cho từng dòng log và ghi vào file chữ ký `secure.log.sig`.
- **`GZipRotator` & `SecureRotatingFileHandler`**: Tự động luân phiên file khi dung lượng đạt 1MB và nén thành tệp `.gz`.

### 3. Tích hợp API Flask (`lab3/app.py`)
Endpoint `POST /validate` tiếp nhận payload JSON, chuyển qua module `securevalidator` xử lý, sau đó ghi log an toàn qua `secure_logger.info(...)`:
```python
@app.route("/validate", methods=["POST"])
def validate():
    data = request.get_json(force=True)
    results = {
        "email": validate_email(data.get("email", "")),
        "url": validate_url(data.get("url", "")),
        "filename": validate_filename(data.get("filename", "")),
        "sql": sanitize_sql_input(data.get("sql", "")),
        "html": sanitize_html_input(data.get("html", "")),
    }
    secure_logger.info("Validation check performed", extra={"data": data, "results": results})
    return jsonify(results)
```

### 4. Kết quả kiểm thử Lab 3
- **Unit Test tự động**:
  ```bash
  cd LAB/lab3
  python -m unittest discover tests
  ```
  👉 **Kết quả: 4/4 test cases PASS (OK)** (Kiểm tra Mask Email, Mask Password, Hash SHA-256 64 ký tự, và API Validation).
- **Kiểm thử API (Postman / PowerShell)**:
  - Gửi POST tới `http://127.0.0.1:5000/validate`:
    ```json
    {
      "email": "phuoc@example.com",
      "url": "https://secure.com",
      "filename": "report.pdf",
      "sql": "' OR 1=1 --",
      "html": "<script>alert(1)</script>"
    }
    ```
  - **Kết quả trả về (Response)**:
    ```json
    {
      "email": true,
      "filename": true,
      "html": "&lt;script&gt;alert(1)&lt;/script&gt;",
      "sql": "1=1",
      "url": true
    }
    ```
  - **Kiểm tra `secure.log`**: Thông tin email đã được che giấu thành `<email_masked>`.
  - **Kiểm tra `secure.log.sig`**: Đã tạo chữ ký mã băm SHA-256 đối soát.

---

## 🚀 HƯỚNG DẪN CHẠY TỪNG BÀI LAB

### Chạy Lab 1 (Secure Validator Web App):
```bash
cd LAB/lab1
pip install -r requirements.txt
python app.py
# Truy cập: http://127.0.0.1:5000
```

### Chạy Lab 2 (Kích hoạt Git Security Hook):
```bash
git config core.hooksPath LAB/lab2/.githooks
```

### Chạy Lab 3 (Secure Logger API):
```bash
cd LAB/lab3
pip install -r requirements.txt
python app.py
# Gửi POST request tới: http://127.0.0.1:5000/validate
```

---
*Hoàn thành trọn vẹn 3 bài thực hành trong LAB theo đúng giáo trình.*

