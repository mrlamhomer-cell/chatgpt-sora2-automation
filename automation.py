#!/usr/bin/env python3
"""
ChatGPT + Sora 2 Automation Script
Đọc từ Google Sheets, tự động login vào ChatGPT và Sora 2, tạo video
"""

import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import gspread
from google.oauth2.service_account import Credentials

# Load config
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# Google Sheets setup
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPE)
client = gspread.authorize(creds)
sheet = client.open_by_key(config['google_sheets_id']).sheet1

def setup_driver():
    """Thiết lập Chrome driver"""
    options = webdriver.ChromeOptions()
    if config.get('chrome_profile_path'):
        options.add_argument(f"user-data-dir={config['chrome_profile_path']}")
    
    # Tắt automation flags
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=options)
    return driver

def login_chatgpt(driver):
    """Login vào ChatGPT"""
    print("[ChatGPT] Đang login...")
    driver.get("https://chat.openai.com")
    
    try:
        # Chờ user login thủ công nếu cần
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[placeholder*='Message']"))
        )
        print("[ChatGPT] Login thành công")
        return True
    except TimeoutException:
        print("[ChatGPT] Login timeout")
        return False

def generate_prompt(driver, description):
    """Gửi mô tả cho ChatGPT để tạo prompt video"""
    print(f"[ChatGPT] Tạo prompt từ mô tả: {description}")
    
    try:
        # Tìm textarea
        textarea = driver.find_element(By.CSS_SELECTOR, "textarea[placeholder*='Message']")
        
        # Gửi prompt engineering
        prompt_request = f"""Tạo một prompt chi tiết cho Sora AI để tạo video từ mô tả sau:
{description}

Prompt cần:
- Mô tả chi tiết cảnh quay, góc máy, ánh sáng
- Thời lượng 5-10 giây
- Chất lượng điện ảnh
- Chuyển động mượt mà

Chỉ trả về prompt, không giải thích thêm."""
        
        textarea.send_keys(prompt_request)
        textarea.submit()
        
        # Chờ response
        time.sleep(10)
        
        # Lấy response cuối cùng
        messages = driver.find_elements(By.CSS_SELECTOR, "div[data-message-author-role='assistant']")
        if messages:
            prompt = messages[-1].text
            print(f"[ChatGPT] Prompt nhận được: {prompt[:100]}...")
            return prompt
        
    except Exception as e:
        print(f"[ChatGPT] Lỗi: {e}")
        return None

def login_sora(driver):
    """Login vào Sora 2"""
    print("[Sora] Đang login...")
    driver.get("https://sora.com")  # Thay URL thật
    
    try:
        # Chờ login thủ công hoặc tự động
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label*='Create']"))
        )
        print("[Sora] Login thành công")
        return True
    except TimeoutException:
        print("[Sora] Login timeout")
        return False

def create_video(driver, prompt, image_url=None):
    """Tạo video trên Sora 2"""
    print(f"[Sora] Tạo video với prompt...")
    
    try:
        # Click nút Create
        create_btn = driver.find_element(By.CSS_SELECTOR, "button[aria-label*='Create']")
        create_btn.click()
        time.sleep(2)
        
        # Upload ảnh nếu có
        if image_url:
            print(f"[Sora] Upload ảnh: {image_url}")
            # Logic upload ảnh
            pass
        
        # Nhập prompt
        prompt_input = driver.find_element(By.CSS_SELECTOR, "textarea[placeholder*='prompt']")  
        prompt_input.send_keys(prompt)
        
        # Click generate
        generate_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        generate_btn.click()
        
        print("[Sora] Đang render video...")
        
        # Chờ video hoàn thành (tối đa 5 phút)
        WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "video"))
        )
        
        # Lấy URL video
        video_element = driver.find_element(By.CSS_SELECTOR, "video")
        video_url = video_element.get_attribute("src")
        
        print(f"[Sora] Video hoàn thành: {video_url}")
        return video_url
        
    except Exception as e:
        print(f"[Sora] Lỗi: {e}")
        return None

def download_video(driver, video_url, filename):
    """Download video về máy"""
    print(f"[Download] Đang tải {filename}...")
    
    download_folder = config.get('download_folder', './videos')
    os.makedirs(download_folder, exist_ok=True)
    
    # Logic download
    # Có thể dùng requests hoặc browser automation
    
    return os.path.join(download_folder, filename)

def update_sheet(row_index, video_url, status):
    """Cập nhật Google Sheet"""
    print(f"[Sheet] Cập nhật dòng {row_index}: {status}")
    
    # Cột D: video_url, Cột E: status
    sheet.update_cell(row_index, 4, video_url or "")
    sheet.update_cell(row_index, 5, status)

def main():
    """Hàm chính"""
    print("=== Bắt đầu automation ===")
    
    # Lấy tất cả dòng từ sheet
    all_rows = sheet.get_all_records()
    
    # Setup driver
    driver = setup_driver()
    
    try:
        # Login ChatGPT
        if not login_chatgpt(driver):
            print("Không thể login ChatGPT")
            return
        
        # Login Sora  
        if not login_sora(driver):
            print("Không thể login Sora")
            return
        
        # Xử lý từng dòng pending
        for i, row in enumerate(all_rows, start=2):  # Start từ 2 vì dòng 1 là header
            if row.get('status', '').lower() != 'pending':
                continue
                
            description = row.get('description', '')
            image_url = row.get('image_url', '')
            
            print(f"\n[Row {i}] Xử lý: {description}")
            
            # Update status = processing
            update_sheet(i, None, "processing")
            
            # 1. Tạo prompt từ ChatGPT
            prompt = generate_prompt(driver, description)
            if not prompt:
                update_sheet(i, None, "failed_prompt")
                continue
            
            # 2. Tạo video trên Sora
            video_url = create_video(driver, prompt, image_url)
            if not video_url:
                update_sheet(i, None, "failed_video")
                continue
            
            # 3. Download (optional)
            # local_path = download_video(driver, video_url, f"video_{i}.mp4")
            
            # 4. Update sheet
            update_sheet(i, video_url, "completed")
            
            print(f"[Row {i}] Hoàn thành!")
            
            # Nghỉ giữa các lần tạo
            time.sleep(5)
            
    finally:
        print("\n=== Kết thúc automation ===")
        input("Nhấn Enter để đóng browser...")
        driver.quit()

if __name__ == "__main__":
    main()
