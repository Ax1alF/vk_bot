from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle
import time
import re

# Параметры браузера для запуска
chrome_options = Options()
chrome_options.add_argument("--headless")  # Если нужно в headless-режиме
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Инициализируем новый экземпляр браузера
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://oauth.vk.com")
time.sleep(2)

# Загружаем cookies из сохранённого файла
cookies_file = 'vk_cookies.pkl'
with open(cookies_file, 'rb') as f:
    cookies = pickle.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)

# Переходим на нужную страницу
driver.get('https://oauth.vk.com/authorize?client_id=6287487&scope=1073803263&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1')

# Нажимаем кнопку "Разрешить" (если она есть)
try:
    allow_btn = driver.find_element_by_css_selector('button[type="submit"], .FlatButton--primary')
    allow_btn.click()
    time.sleep(2)
except Exception:
    print("Кнопка 'Разрешить' не найдена — возможно, уже было подтверждено ранее.")

# Ждём редиректа с токеном
url = driver.current_url
print("🌐 Redirect URL:", url)

# Извлекаем токен
match = re.search(r'access_token=([^&]+)', url)
if match:
    token = match.group(1)
    print("✅ Access Token:", token)
else:
    print("❌ Access Token не найден")

driver.quit()
