import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os

def get_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')  # закомментируй, чтобы видеть браузер
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


async def test_step_by_step(name: str):
    driver = get_chrome_driver()
    try:
        # 1️⃣ Открываем сайт
        driver.get("https://cacs.ws")
        driver.save_screenshot("/tmp/step_1_open.png")
        print("Step 1: page opened ->", os.path.exists("/tmp/step_1_open.png"))

        # 2️⃣ Находим поле поиска и вводим имя
        try:
            input_element = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Поиск на Каксе"]')
            input_element.send_keys(name)
            driver.save_screenshot("/tmp/step_2_input.png")
            print("Step 2: input sent ->", os.path.exists("/tmp/step_2_input.png"))
        except Exception as e:
            print("Step 2: input failed ->", e)

        # 3️⃣ Клик по найденному элементу
        try:
            wait = WebDriverWait(driver, 10)
            element = wait.until(
                  EC.element_to_be_clickable(
                  (By.XPATH, f'//a[contains(text(), "{name}")]')
    )
)
            element.click()
            driver.save_screenshot("/tmp/step_3_click.png")
            print("Step 3: element clicked ->", os.path.exists("/tmp/step_3_click.png"))
        except Exception as e:
            print("Step 3: click failed ->", e)

        # 4️⃣ Клик по последней кнопке, если есть
        try:
            buttons = driver.find_elements(By.CLASS_NAME, 'Button_button__PjVhE')
            if buttons:
                buttons[-1].click()
                driver.save_screenshot("/tmp/step_4_button.png")
                print("Step 4: button clicked ->", os.path.exists("/tmp/step_4_button.png"))
            else:
                print("Step 4: no buttons found")
        except Exception as e:
            print("Step 4: button click failed ->", e)

        # 5️⃣ Финальный скриншот
        driver.save_screenshot("/tmp/step_5_final.png")
        print("Step 5: final screenshot ->", os.path.exists("/tmp/step_5_final.png"))

    finally:
        driver.quit()


if __name__ == "__main__":
    import sys
    name = sys.argv[1] if len(sys.argv) > 1 else "Иванов"
    asyncio.run(test_step_by_step(name))
