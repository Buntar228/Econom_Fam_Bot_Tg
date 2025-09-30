import os
import asyncio
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Константы
TIMEOUT = 1
WAIT_ELEMENT = 10  # время ожидания элемента

def get_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--log-level=3")

    if os.path.exists("/usr/bin/chromium"):
        chrome_options.binary_location = "/usr/bin/chromium"
        driver_path = "/usr/bin/chromedriver"
    else:
        chrome_options.binary_location = "/usr/bin/google-chrome"
        driver_path = ChromeDriverManager().install()

    return webdriver.Chrome(
        service=Service(driver_path),
        options=chrome_options
    )

async def get_schedule(name: str):
    driver = get_chrome_driver()
    driver.set_window_size(2048, 1080)
    loop = asyncio.get_event_loop()

    try:
        # Открываем сайт
        await loop.run_in_executor(None, driver.get, 'https://cacs.ws')

        # Находим поле поиска и вводим имя
        input_element = await loop.run_in_executor(
            None,
            lambda: driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Поиск на Каксе"]')
        )
        input_element.send_keys(name)

        # Ждём появления нужного результата поиска
        wait = WebDriverWait(driver, WAIT_ELEMENT)
        try:
            element = await loop.run_in_executor(
                None,
                lambda: wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, f'//a[contains(@class, "Searchbar_searchbaroptionVOoIz") and contains(., "{name}")]')
                    )
                )
            )
        except TimeoutException:
            print(f"Элемент с именем {name} не найден")
            return None

        element.click()

        # Скриншот первой страницы
        screenshot_path_1 = os.path.join(os.getcwd(), '1.png')
        await make_screenshot(driver, loop, screenshot_path_1)

        # Нажимаем последнюю кнопку на странице
        buttons = await loop.run_in_executor(None, lambda: driver.find_elements(By.CLASS_NAME, 'Button_button__PjVhE'))
        if buttons:
            buttons[-1].click()
            await asyncio.sleep(TIMEOUT)

        # Скриншот второй страницы
        screenshot_path_2 = os.path.join(os.getcwd(), '2.png')
        await make_screenshot(driver, loop, screenshot_path_2)

        return screenshot_path_1, screenshot_path_2

    finally:
        driver.quit()

async def make_screenshot(driver, loop, path):
    wait = WebDriverWait(driver, WAIT_ELEMENT)
    try:
        # Ждём, пока нужный элемент прогрузится
        await loop.run_in_executor(
            None,
            lambda: wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "main div.wrapper.Timetable_timetable___l88y"))
            )
        )
    except TimeoutException:
        print("Элемент для скриншота не найден, делаем полный скриншот страницы")

    # Получаем размеры страницы
    page_width = await loop.run_in_executor(None, driver.execute_script, "return document.body.scrollWidth")
    page_height = await loop.run_in_executor(None, driver.execute_script, "return document.body.scrollHeight")
    driver.set_window_size(width=page_width, height=page_height)

    # Сохраняем скриншот
    await loop.run_in_executor(None, driver.save_screenshot, path)
