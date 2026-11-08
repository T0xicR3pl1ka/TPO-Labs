"""
Автотесты контактной формы (contact.html).
Запуск: pytest test_contact_form.py -v
"""
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from contact_page import ContactPage


VALID_DATA = {
    "name": "Иван Петров",
    "email": "ivan.petrov@example.com",
    "subject": "support",
    "message": "Здравствуйте! У меня вопрос по заказу №12345.",
}


# ---------- Фикстуры ----------
@pytest.fixture()
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1280,900")
    # options.add_argument("--headless=new")
    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    yield drv
    drv.quit()


@pytest.fixture()
def contact_page(driver):
    url = Path(__file__).with_name("contact.html").resolve().as_uri()
    return ContactPage(driver).open(url)


# ---------- Позитивный сценарий ----------
def test_successful_submit(contact_page):
    """Все поля заполнены валидно -> успешное сообщение, форма скрыта."""
    contact_page.fill_form(**VALID_DATA).submit()

    assert contact_page.is_success_visible(), "Сообщение об успехе не появилось"
    assert "успешно отправлено" in contact_page.get_success_text().lower()
    assert not contact_page.is_form_visible(), "Форма должна быть скрыта после отправки"


# ---------- Негативные сценарии ----------
def test_empty_required_field_name(contact_page):
    """Пустое обязательное поле «Имя» -> ошибка, успех не показан."""
    data = dict(VALID_DATA, name="")
    contact_page.fill_form(**data).submit()

    assert contact_page.get_name_error() == "Введите имя"
    assert not contact_page.is_success_visible()
    assert contact_page.is_form_visible()


def test_all_fields_empty(contact_page):
    """Пустая форма -> ошибки во всех обязательных полях."""
    contact_page.submit()

    assert contact_page.get_name_error() == "Введите имя"
    assert contact_page.get_email_error() == "Введите email"
    assert contact_page.get_subject_error() == "Выберите тему"
    assert contact_page.get_message_error() == "Введите сообщение"
    assert contact_page.get_agree_error() == "Необходимо согласие с обработкой данных"
    assert not contact_page.is_success_visible()


def test_invalid_email(contact_page):
    """Некорректный email -> ошибка «Некорректный email»."""
    data = dict(VALID_DATA, email="ivan.petrov@")
    contact_page.fill_form(**data).submit()

    assert contact_page.get_email_error() == "Некорректный email"
    assert not contact_page.is_success_visible()


def test_short_message(contact_page):
    """Слишком короткое сообщение (<10 символов) -> ошибка."""
    data = dict(VALID_DATA, message="Привет")
    contact_page.fill_form(**data).submit()

    assert "минимум 10 символов" in contact_page.get_message_error()
    assert not contact_page.is_success_visible()


def test_no_agreement_checkbox(contact_page):
    """Не установлен чекбокс согласия -> ошибка."""
    contact_page.fill_form(**VALID_DATA, agree=False).submit()

    assert contact_page.get_agree_error() == "Необходимо согласие с обработкой данных"
    assert not contact_page.is_success_visible()