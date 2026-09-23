# LAB 2: THỰC HÀNH GIT SECURITY HOOK
*(Theo hướng dẫn giáo trình Trang 20 – 25)*

## 1. Mục tiêu
- Triển khai cơ chế **Git Pre-commit Hook** nhằm tự động quét mã nguồn trước khi commit.
- Ngăn chặn lộ lọt các bí mật mã nguồn: Passwords, API Keys, Tokens, AWS Access Keys.
- Kiểm tra quyền truy cập tệp nguy hiểm (`world-writable`).
- Tích hợp công cụ **Bandit** quét lỗ hổng mức độ nghiêm trọng (High Severity).

## 2. Triển khai kỹ thuật (`.githooks/pre-commit`)
- Định nghĩa danh sách biểu thức chính quy nhận diện bí mật (`SENSITIVE_PATTERNS`) như apikey, secret, password, token, AWS Key.
- Xử lý tương thích môi trường Windows: Bỏ qua kiểm tra cờ POSIX `S_IWOTH` khi chạy trên hệ điều hành Windows.
- Tự động gọi Bandit quét mã nguồn Python trước khi cho phép commit.

## 3. Cấu trúc thư mục
- `.githooks/pre-commit`: Script hook kiểm tra mã nguồn, secrets & permissions.
- `pre-commit-hook-test/bad.py`: File mẫu kiểm thử vi phạm lộ password.
- `requirements.txt`: Chứa thư viện bandit.

## 4. Hướng dẫn chạy và kiểm thử
### Kích hoạt Git Security Hook
Đăng ký thư mục chứa hook với git:
`ash
git config core.hooksPath LAB/lab2/.githooks
`

### Kiểm thử chặn Commit
1. Đảm bảo có file vi phạm chứa mật khẩu: `pre-commit-hook-test/bad.py`
2. Thực hiện lệnh:
   `ash
   git add .
   git commit -m "test bad file"
   `
3. Kết quả mong đợi: Git tự động chặn và thông báo lỗi phát hiện "password", đồng thời ghi vào file `gitsecure.log`.
