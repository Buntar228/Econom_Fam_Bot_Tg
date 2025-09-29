import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

TIMEOUT = 1
WAIT_ELEMENT = 15  # увеличиваем ожидание для полной загрузки


def get_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--log-level=3")

    # Автоматически выбираем бинарь: в контейнере chromium, локально google-chrome
    if os.path.exists("/usr/bin/chromium"):
        print("⚡ Используется Chromium из контейнера")
        chrome_options.binary_location = "/usr/bin/chromium"
        driver_path = "/usr/bin/chromedriver"
    else:
        print("⚡ Используется Google Chrome локально")
        chrome_options.binary_location = "/usr/bin/google-chrome"
        driver_path = ChromeDriverManager().install()

    return webdriver.Chrome(
        service=Service(driver_path),
        options=chrome_options
    )


def get_schedule(name: str):
    driver = get_chrome_driver()
    driver.set_window_size(2048, 1080)

    try:
        driver.get('https://cacs.ws')

        # Вводим имя
        input_element = WebDriverWait(driver, WAIT_ELEMENT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Поиск на Каксе"]'))
        )
        input_element.send_keys(name)

        element = WebDriverWait(driver, WAIT_ELEMENT).until(
            EC.element_to_be_clickable(
                (By.XPATH, f'//a[contains(@class, "Searchbar_searchbaroptionVOoIz") and contains(., "{name}")]')
            )
        )
        element.click()

        # Скриншот 1
        screenshot_path_1 = os.path.join(os.getcwd(), '1.png')
        make_screenshot_sync(driver, screenshot_path_1)

        # Жмём последнюю кнопку (если есть)
        buttons = driver.find_elements(By.CLASS_NAME, 'Button_button__PjVhE')
        if buttons:
            buttons[-1].click()

        screenshot_path_2 = os.path.join(os.getcwd(), '2.png')
        make_screenshot_sync(driver, screenshot_path_2)

        return screenshot_path_1, screenshot_path_2

    finally:
        driver.quit()


def make_screenshot_sync(driver, path):
    try:
        WebDriverWait(driver, WAIT_ELEMENT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "main div.wrapper.Timetable_timetable___l88y"))
        )
    except TimeoutException:
        print("⚠ Элемент для скриншота не найден, делаем полный скриншот страницы")

    # Размеры страницы
    page_width = driver.execute_script("return document.body.scrollWidth")
    page_height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(width=page_width, height=page_height)

    driver.save_screenshot(path)
