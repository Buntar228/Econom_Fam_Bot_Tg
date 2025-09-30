import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

def get_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')  # если хочешь видеть браузер, закомментируй
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--log-level=3")

    if os.path.exists("/usr/bin/chromium"):
        chrome_options.binary_location = "/usr/bin/chromium"
        driver_path = "/usr/bin/chromedriver"
    else:
        from webdriver_manager.chrome import ChromeDriverManager
        chrome_options.binary_location = "/usr/bin/google-chrome"
        driver_path = ChromeDriverManager().install()

    return webdriver.Chrome(service=Service(driver_path), options=chrome_options)

async def create_screenshots():
    driver = get_chrome_driver()
    try:
        # Загружаем сайт
        driver.get("https://cacs.ws")

        # Путь для скриншотов
        path1 = "/tmp/1.png"
        path2 = "/tmp/2.png"

        # Скрин 1
        success1 = driver.save_screenshot(path1)
        print("Screenshot 1 saved:", success1, os.path.exists(path1))

        # Скрин 2
        success2 = driver.save_screenshot(path2)
        print("Screenshot 2 saved:", success2, os.path.exists(path2))

    finally:
        driver.quit()

if __name__ == "__main__":
    asyncio.run(create_screenshots())
