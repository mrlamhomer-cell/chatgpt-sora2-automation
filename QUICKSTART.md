# Quick Start Guide - ChatGPT Sora 2 Automation

## Giới thiệu
Hướng dẫn nhanh để chạy automation tạo video Sora 2 từ Google Sheets trong 15 phút.

---

## Bước 1: Copy Google Sheets Template

1. Mở template: **[ChatGPT Sora 2 Automation Template](https://docs.google.com/spreadsheets/d/1Oq6MMf_uSq2f3vEFoj8V_rhlkvZ6Q6jCL5DTxCDRwNg/edit)**
2. Click **File → Make a copy** để tạo bản sao của bạn
3. Đổi tên sheet theo ý muốn

### Cấu trúc Google Sheet:

| Column | Description | Example |
|--------|-------------|----------|
| `description` | Mô tả video bằng ngôn ngữ tự nhiên | "Cinematic shot of a sunset over ocean waves" |
| `image_url` | (Optional) Link ảnh tham khảo | `https://example.com/image.jpg` |
| `prompt` | Prompt sẽ được ChatGPT tạo tự động | (để trống, script sẽ fill) |
| `video_url` | Link video sau khi Sora 2 tạo xong | (để trống, script sẽ fill) |
| `status` | Trạng thái: `pending`, `processing`, `completed`, `failed` | `pending` |

**Lưu ý**: Hàng nào có `status = pending` sẽ được script xử lý.

---

## Bước 2: Setup Google Sheets API

### 2.1. Tạo Google Cloud Project

1. Truy cập: https://console.cloud.google.com/
2. Tạo project mới (hoặc chọn project có sẵn)
3. Vào **APIs & Services → Library**
4. Search "Google Sheets API" → Click **Enable**

### 2.2. Tạo Service Account

1. Vào **APIs & Services → Credentials**
2. Click **Create Credentials → Service Account**
3. Đặt tên service account → Click **Create and Continue**
4. Role: Chọn **Editor** → Click **Done**

### 2.3. Download Credentials

1. Click vào service account vừa tạo
2. Tab **Keys** → **Add Key → Create new key**
3. Chọn format **JSON** → Click **Create**
4. File `credentials.json` sẽ được tải về máy

### 2.4. Share Google Sheet

1. Mở file `credentials.json`, tìm dòng:
```json
"client_email": "your-service-account@project.iam.gserviceaccount.com"
```
2. Copy email này
3. Mở Google Sheet của bạn → Click **Share**
4. Paste email service account → Chọn quyền **Editor** → **Send**

---

## Bước 3: Clone Repository

```bash
git clone https://github.com/mrlamhomer-cell/chatgpt-sora2-automation.git
cd chatgpt-sora2-automation
```

---

## Bước 4: Cài đặt Dependencies

### 4.1. Cài Python packages

```bash
pip install -r requirements.txt
```

### 4.2. Cài ChromeDriver

1. Kiểm tra version Chrome: `chrome://version`
2. Download ChromeDriver tương ứng: https://chromedriver.chromium.org/
3. Đưa file `chromedriver` vào PATH hoặc để cùng thư mục với `automation.py`

**Hoặc sử dụng webdriver-manager (tự động):**
```bash
pip install webdriver-manager
```

---

## Bước 5: Tạo File Config

### 5.1. Copy file mẫu

```bash
cp config.json.example config.json
```

### 5.2. Sửa config.json

Mở `config.json` và điền thông tin:

```json
{
  "chatgpt_email": "your-chatgpt@email.com",
  "chatgpt_password": "your_password",
  "openai_email": "your-openai@email.com",
  "openai_password": "your_password",
  "google_sheets_id": "YOUR_GOOGLE_SHEET_ID",
  "download_folder": "./videos",
  "chrome_profile_path": null
}
```

**Lấy Google Sheet ID:**
Từ URL: `https://docs.google.com/spreadsheets/d/[SHEET_ID_O_DAY]/edit`

### 5.3. Đặt file credentials.json

Copy file `credentials.json` (từ Bước 2.3) vào thư mục gốc của project.

---

## Bước 6: Chạy Automation

```bash
python automation.py
```

### Điều gì sẽ xảy ra:

1. Browser Chrome sẽ mở tự động
2. Script sẽ login vào ChatGPT (lần đầu có thể cần xác thực 2FA thủ công)
3. Với mỗi dòng có `status = pending` trong Google Sheet:
   - Gửi `description` cho ChatGPT để tạo prompt chi tiết
   - Login Sora 2 và tạo video
   - Chờ video render xong
   - Cập nhật `video_url` và `status = completed` vào Google Sheet

### Lưu ý quan trọng:

- ⏱️ **Không đóng browser** khi script đang chạy
- 🔐 **Lần đầu chạy**: Có thể cần login thủ công nếu có 2FA
- 🎬 **Thời gian**: Mỗi video mất ~2-5 phút để render
- 📁 **Video**: Được lưu trong folder `./videos/` (nếu bật download)

---

## Troubleshooting

### Lỗi: ChromeDriver không tương thích

**Giải pháp**: Cài đúng version ChromeDriver với Chrome của bạn

```bash
pip install webdriver-manager
```

Sau đó update code trong `automation.py`:

```python
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
```

### Lỗi: Google Sheets API Permission Denied

**Nguyên nhân**: Chưa share sheet với service account email

**Giải pháp**: Xem lại Bước 2.4

### Lỗi: Cannot login ChatGPT

**Nguyên nhân**: 2FA hoặc sai email/password

**Giải pháp**: 
- Kiểm tra lại `config.json`
- Lần đầu chạy, login thủ công trong browser automation

### Lỗi: Sora 2 không khả dụng

**Nguyên nhân**: Tài khoản chưa có quyền truy cập Sora 2 hoặc URL sai

**Giải pháp**: 
- Đảm bảo tài khoản có access Sora 2
- Update URL Sora 2 thật trong code (hiện tại dùng placeholder)

---

## Next Steps

✅ Automation đã chạy thành công?

### Tích hợp vào workflow:

1. **Schedule định kỳ**: Dùng cron job (Linux/Mac) hoặc Task Scheduler (Windows)
   ```bash
   # Chạy mỗi giờ
   0 * * * * cd /path/to/project && python automation.py
   ```

2. **Kết hợp n8n/Make.com**:
   - Trigger: Webhook khi có dòng mới trong Google Sheet
   - Action: Gọi script automation này

3. **Deploy lên server**: Cloud VM (AWS, GCP, Azure) để chạy 24/7

---

## Hỗ trợ

- **Issues**: https://github.com/mrlamhomer-cell/chatgpt-sora2-automation/issues
- **Docs chi tiết**: Xem `SETUP.md`
- **Questions**: Mở issue mới trên GitHub

---

**Chúc bạn automation thành công! 🚀**
