from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

VALID_USER = "testuser"
VALID_PASS = "testpass123"
TIMEOUT = 10


# ---------- Фикстуры ----------
@pytest.fixture()
def driver():
    """Фикстура: создает браузер до теста и закрывает после."""
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1280,800")
    options.add_argument("--headless=new")          # Включаем невидимый режим для GitHub
    options.add_argument("--no-sandbox")            # Обязательно для серверов Linux
    options.add_argument("--disable-dev-shm-usage") # Обязательно для серверов Linux
    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    yield drv
    drv.quit()


@pytest.fixture()
def login_page(driver):
    """Открывает страницу логина и возвращает driver."""
    url = Path(__file__).with_name("login.html").resolve().as_uri()
    driver.get(url)
    return driver


def login(driver, username: str, password: str) -> None:
    """Хелпер: заполняет форму и нажимает «Войти»."""
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-btn").click()


# ---------- Тесты ----------
def test_successful_login(login_page):
    """Позитивный: валидные credentials -> появляется кнопка Logout."""
    driver = login_page

    login(driver, VALID_USER, VALID_PASS)

    logout_btn = WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "logout-btn"))
    )

    assert logout_btn.is_displayed(), "Кнопка Logout не отображается после входа"
    assert logout_btn.text == "Logout"
    assert driver.find_element(By.ID, "welcome").is_displayed()
    # Форма логина скрыта
    assert not driver.find_element(By.ID, "login-container").is_displayed()


def test_logout_returns_to_login(login_page):
    """После Logout снова отображается форма логина."""
    driver = login_page

    login(driver, VALID_USER, VALID_PASS)
    WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "logout-btn"))
    ).click()

    assert WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "login-container"))
    ).is_displayed()
    assert not driver.find_element(By.ID, "logout-btn").is_displayed()


def test_login_invalid_password(login_page):
    """Негативный: неверный пароль -> сообщение об ошибке, Logout не появляется."""
    driver = login_page

    login(driver, VALID_USER, "wrong_password")

    error = WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "error-message"))
    )
    assert "Неверный логин или пароль" in error.text
    assert not driver.find_element(By.ID, "logout-btn").is_displayed()


def test_login_empty_fields(login_page):
    """Негативный: пустые поля -> валидационное сообщение."""
    driver = login_page

    driver.find_element(By.ID, "login-btn").click()

    error = WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "error-message"))
    )
    assert "Заполните все поля" in error.text
