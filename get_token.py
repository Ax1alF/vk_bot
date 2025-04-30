from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re

chrome_options = Options()

# 🔥 Укажи путь к своему рабочему профилю Chrome
chrome_options.add_argument("--user-data-dir=/home/ubuntu/snap/chromium/common/chromium")
chrome_options.add_argument("--profile-directory=Default")

# ⛔️ НЕ headless! Нужно визуальное окно
# chrome_options.add_argument("--headless")  # Отключи это

driver = webdriver.Chrome(options=chrome_options)

# Проверим авторизован ли пользователь
driver.get("https://oauth.vk.com")
time.sleep(2)

if "login.vk.com" in driver.current_url:
    print("❌ Сессия не активна. Требуется повторная авторизация.")
    driver.quit()
    exit()

# Переходим по OAuth-ссылке
driver.get("https://oauth.vk.com/authorize?client_id=6287487&scope=1073803263&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1")
time.sleep(3)

# Жмем "Разрешить", если нужно
try:
    allow_btn = driver.find_element("css selector", 'button[type="submit"], .FlatButton--primary')
    allow_btn.click()
    time.sleep(2)
except:
    print("🚫 Кнопка 'Разрешить' не найдена или уже нажата")

# Получаем токен
url = driver.current_url
match = re.search(r'access_token=([^&]+)', url)
if match:
    print("✅ Access Token:", match.group(1))
else:
    print("❌ Токен не найден")

# driver.quit()
