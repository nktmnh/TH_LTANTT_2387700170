# TH_LTANTT Lab 2: Mật mã & PKI

Đây là kết quả bài thực hành Lab 2: Mật mã học hiện đại và Hạ tầng khóa công khai (PKI).
Bài làm bao gồm 2 phần chính: `crypto-toolkit` và `mini-ca`.

## Phần 1: Thư viện `crypto-toolkit`

Cài đặt các thư viện cần thiết và chạy unit test cho các module AES, Argon2 và RSA.

![Unit Test](images/image1.png)

Kết quả mã hóa file `data.txt` bằng công cụ dòng lệnh (CLI):

![Mã hóa CLI](images/image2.png)

Kết quả giải mã file `data.txt.enc` qua CLI:

![Giải mã CLI](images/image3.png)

Sử dụng ứng dụng giao diện (GUI) để mã hóa/giải mã:

![Giao diện GUI](images/image4.png)

Chạy Flask API và kiểm thử qua Postman:

![Postman API](images/image5.png)

## Phần 2: Hệ thống `mini-ca`

Khởi chạy kịch bản (demo) tạo Root CA, Intermediate CA, phát hành và thu hồi chứng chỉ.

![Kết quả kịch bản Mini CA](images/image6.png)

Giao diện quản lý vòng đời chứng chỉ số:

![Giao diện Mini CA](images/image7.png)
