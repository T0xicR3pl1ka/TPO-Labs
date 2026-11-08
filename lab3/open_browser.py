"""
Скрипт 1: инициализация браузера Chrome с помощью WebDriver,
открытие страницы логина и закрытие браузера.
"""
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def build_driver() -> webdriver.Chrome:
    """Создает и возвращает экземпляр Chrome WebDriver."""
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")  # раскомментировать для запуска без окна
    options.add_argument("--window-size=1280,800")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def get_login_url() -> str:
    """Возвращает file:// URL страницы login.html рядом со скриптом."""
    return Path(__file__).with_name("login.html").resolve().as_uri()


if __name__ == "__main__":
    driver = build_driver()
    try:
        driver.get(get_login_url())
        print("Открыта страница:", driver.title)
        time.sleep(30)
    finally:
        driver.quit()
        print("Браузер закрыт.")