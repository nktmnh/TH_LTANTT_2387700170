# TH_LTANTT - Bài 3: Bảo mật Mạng Máy tính

Repository này chứa mã nguồn cho **Bài 3: Bảo mật Mạng Máy tính**, bao gồm hai ứng dụng chính: **SecureChat** và **NetRecon**.

## 1. SecureChat
Ứng dụng trò chuyện bảo mật với mã hóa đầu cuối (End-to-End Encryption) và kết nối an toàn qua SSL/TLS.

### Tính năng chính:
- Tự động tạo và quản lý chứng chỉ CA, Server, và Client (`make-certs.bat`).
- Mã hóa toàn bộ tin nhắn bằng chuẩn AES-256 (`message_encryption.py`).
- Xác thực hai chiều giữa Server và Client sử dụng SSL/TLS.
- Hỗ trợ đa luồng cho phép nhiều client kết nối và trò chuyện trong các phòng chat.

### Cách sử dụng:
1. Chạy file `make-certs.bat` để tạo bộ chứng chỉ (nếu chưa có).
2. Mở một terminal và chạy server: `cd secure-chat` -> `python server.py`
3. Mở các terminal khác để chạy client: `cd secure-chat` -> `python client.py`

## 2. NetRecon
Công cụ trinh sát mạng tự động với giao diện Web (Flask) và công cụ dòng lệnh (CLI).

### Tính năng chính:
- **Port Scanner:** Quét cổng bất đồng bộ sử dụng `asyncio`.
- **Service Detector:** Tích hợp Nmap để phát hiện phiên bản dịch vụ đang chạy.
- **Banner Grabber:** Thu thập thông tin banner từ các dịch vụ mạng.
- **Network Mapper:** Lập bản đồ mạng cục bộ thông qua ARP.
- **Vulnerability Checker:** Quét và đối chiếu các lỗ hổng (CVE) cơ bản trên các cổng mở.
- **Báo cáo:** Gửi email kết quả tự động sau khi quét xong.

### Cách sử dụng:
1. Cài đặt các thư viện yêu cầu: `pip install -r netrecon/requirements.txt`
2. Đổi thông tin email trong file `netrecon/.env` (SMTP_USER, SMTP_PASS).
3. Sử dụng qua giao diện Web: `cd netrecon` -> `python app.py` (truy cập `http://localhost:5000/`)
4. Sử dụng qua CLI: `cd netrecon` -> `python cli.py --target <IP> --ports 22,80,443 --mode all`
