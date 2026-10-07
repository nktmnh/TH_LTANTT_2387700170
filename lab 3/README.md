Bài 3: Bảo Mật Mạng Máy Tính & Công Cụ Trinh Sát

Repository này chứa mã nguồn và tài liệu hướng dẫn thực hành cho Bài 3: Bảo mật mạng máy tính, bao gồm hai ứng dụng chính: SecureChat (Ứng dụng chat bảo mật sử dụng SSL/TLS và mã hóa AES) và NetRecon (Bộ công cụ trinh sát và quét mạng tích hợp giao diện web Flask và CLI).

📋 Mục Lục

Giới Thiệu Đề Tài

Cấu Trúc Thư Mục Dự Án

Phần 1: Ứng Dụng Chat Bảo Mật (SecureChat)

Yêu cầu hệ thống & Thư viện

Hướng dẫn cấu hình chứng chỉ (OpenSSL)

Cách chạy ứng dụng

Phần 2: Bộ Công Cụ Trinh Sát Mạng (NetRecon)

Yêu cầu hệ thống & Cài đặt

Cấu hình môi trường (.env)

Cách chạy CLI và Web App

Tác Giả

🎯 Giới Thiệu Đề Tài

SecureChat: Xây dựng hệ thống chat đa luồng hỗ trợ SSL/TLS hai chiều (Client Certificate Authentication), mã hóa đầu cuối bằng thuật toán AES-256-CBC, quản lý kết nối và hỗ trợ nhiều phòng chat khác nhau.

NetRecon: Phát triển bộ công cụ khám phá và kiểm tra mạng toàn diện bao gồm quét cổng bất đồng bộ (PortScanner), nhận dạng dịch vụ qua Nmap (ServiceDetector), lấy banner an toàn (BannerGrabber), ánh xạ mạng (NetworkMapper) và kiểm tra lỗ hổng cơ bản dựa trên CVE (VulnChecker), kết hợp thông báo kết quả qua Email.

🗂️ Cấu Trúc Thư Mục Dự Án

.
├── secure-chat/                  # Thư mục chứa ứng dụng SecureChat
│   ├── certs/                    # Chứa chứng chỉ CA, Server, Client
│   ├── client.py                 # Mã nguồn phía Client
│   ├── server.py                 # Mã nguồn phía Server
│   ├── connection_manager.py     # Quản lý kết nối client
│   ├── room_manager.py           # Quản lý các phòng chat
│   ├── message_encryption.py     # Xử lý mã hóa/giải mã AES
│   ├── openssl.cnf               # Cấu hình OpenSSL cho CA
│   └── make-certs.bat            # Script tự động tạo chứng chỉ (Windows)
│
└── netrecon/                     # Thư mục chứa bộ công cụ NetRecon
    ├── modules/                  # Các module chức năng (port_scanner, banner_grabber, v.v.)
    ├── static/                   # File CSS tĩnh
    ├── templates/                # Giao diện HTML (Flask & HTMX)
    ├── app.py                    # Ứng dụng Web Flask
    ├── cli.py                    # Giao diện dòng lệnh (CLI)
    ├── requirements.txt          # Danh sách các gói Python cần thiết
    └── .env                      # Cấu hình bảo mật (SMTP User & App Password)


🔒 Phần 1: Ứng Dụng Chat Bảo Mật (SecureChat)

Yêu cầu hệ thống

Python 3.8+

Thư viện cryptography

Cài đặt OpenSSL trên hệ điều hành và thêm vào biến môi trường PATH.

Hướng dẫn tạo chứng chỉ tự ký (Certificate Authority & Certificates)

Di chuyển vào thư mục secure-chat:

cd secure-chat


Chạy file script make-certs.bat để tự động khởi tạo thư mục certs/ chứa:

CA (Certificate Authority): ca.crt, ca.key

Server: server.crt, server.key, server.csr

Client: client.crt, client.key, client.csr

Cách chạy ứng dụng

Khởi động Server:

python server.py


(Server sẽ lắng nghe tại cổng 8443 và yêu cầu xác thực chứng chỉ client).

Khởi động Client (Mở terminal mới cho mỗi client):

python client.py


Nhập Username khi được yêu cầu.

Nhập tin nhắn cần gửi hoặc gõ exit để thoát.

🔍 Phần 2: Bộ Công Cụ Trinh Sát Mạng (NetRecon)

Yêu cầu hệ thống

Python 3.8+

Công cụ Nmap đã được cài đặt và cấu hình trong PATH.

Cài đặt thư viện

Di chuyển vào thư mục netrecon:

cd netrecon


Cài đặt các gói phụ thuộc:

pip install -r requirements.txt


Cấu hình môi trường (.env)

Tạo hoặc chỉnh sửa file .env trong thư mục netrecon/ để cấu hình gửi email thông báo kết quả qua Gmail:

SMTP_USER=your_email@gmail.com
SMTP_PASS=your_google_app_password


(Lấy mật khẩu ứng dụng Google tại: https://myaccount.google.com/apppasswords)

Cách chạy ứng dụng

Chạy bằng dòng lệnh (CLI):

python cli.py --target 127.0.0.1 --ports 22,80,443 --mode all


Chạy giao diện Web Flask:

python app.py


Truy cập trình duyệt tại địa chỉ: http://localhost:5000/

✍️ Tác Giả

Họ và tên: Võ Nhật Minh

Mã số sinh viên: 2387700170
