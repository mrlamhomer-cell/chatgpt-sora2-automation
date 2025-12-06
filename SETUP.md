# Hướng dẫn cài đặt ChatGPT + Sora 2 Automation

## Yêu cầu hệ thống
- Python 3.8+
- Chrome Browser
- ChromeDriver (phiên bản tương thích với Chrome)
- Tài khoản ChatGPT (OpenAI)
- Tài khoản Sora 2 (OpenAI)
- Google Account (để dùng Google Sheets)

## Bước 1: Clone Repository
```bash
git clone https://github.com/mrlamhomer-cell/chatgpt-sora2-automation.git
cd chatgpt-sora2-automation
```

## Bước 2: Cài đặt Python Dependencies
```bash
pip install -r requirements.txt
```

## Bước 3: Cài đặt ChromeDriver
1. Kiểm tra phiên bản Chrome: chrome://version
2. Download ChromeDriver tương ứng: https://chromedriver.chromium.org/
3. Đưa ChromeDriver vào PATH hoặc cùng thư mục với script

## Bước 4: Setup Google Sheets API
1. Vào https://console.cloud.google.com/
2. Tạo project mới
3. Enable Google Sheets API
4. Tạo Service Account
5. Download credentials.json
6. Đặt file credentials.json vào thư mục gốc

## Bước 5: Tạo Google Sheet
Tạo Google Sheet với cấu trúc:

| A: description | B: image_url | C: prompt | D: video_url | E: status |
|---------------|-------------|----------|-------------|----------|
| Mô tả video | URL ảnh (optional) | | | pending |

**Share Sheet với email service account!**

## Bước 6: Cấu hình
```bash
cp config.json.example config.json
```

Edit config.json:
```json
{
  "chatgpt_email": "your@email.com",
  "chatgpt_password": "your_password",
  "openai_email": "your@email.com",
  "openai_password": "your_password",
  "google_sheets_id": "ID_CUA_GOOGLE_SHEET",
  "download_folder": "./videos",
  "chrome_profile_path": null
}
```

**Lấy Google Sheet ID**: Copy từ URL
`https://docs.google.com/spreadsheets/d/[SHEET_ID_O_DAY]/edit`

## Bước 7: Chạy Automation
```bash
python automation.py
```

## Cách hoạt động
1. Script đọc Google Sheet, tìm dòng có status="pending"
2. Mở Chrome, login ChatGPT
3. Gửi mô tả để ChatGPT tạo prompt
4. Login Sora 2
5. Upload ảnh (nếu có) và tạo video
6. Chờ video render xong
7. Download video và cập nhật Google Sheet

## Troubleshooting

### Lỗi: ChromeDriver không tương thích
- Cài đúng phiên bản ChromeDriver với Chrome

### Lỗi: Cannot login ChatGPT
- Kiểm tra email/password
- Có thể cần xác thực 2FA thủ công lần đầu

### Lỗi: Google Sheets API
- Kiểm tra credentials.json
- Đảm bảo đã share Sheet với service account email

### Lỗi: Sora 2 không khả dụng
- Tài khoản cần có access Sora 2 API
- Kiểm tra URL Sora 2 trong code

## Lưu ý
- Script sẽ mở browser thật, bạn sẽ thấy automation chạy
- Lần đầu có thể cần xác thực 2FA thủ công
- Video sẽ được lưu trong folder ./videos/
- Không đóng browser khi đang chạy
