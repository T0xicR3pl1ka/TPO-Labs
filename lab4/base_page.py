"""
BasePage: общие методы для всех страниц (открытие, поиск, ожидания, клики, ввод).
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    TIMEOUT = 10

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.TIMEOUT)

    def open(self, url: str):
        """Открывает URL."""
        self.driver.get(url)
        return self

    def find(self, locator: tuple):
        """Возвращает элемент (с ожиданием присутствия в DOM)."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_visible(self, locator: tuple):
        """Возвращает видимый элемент."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator: tuple):
        """Клик по кликабельному элементу."""
        self.wait.until(EC.element_to_be_clickable(locator)).click()
        return self

    def type(self, locator: tuple, text: str):
        """Очищает поле и вводит текст."""
        element = self.find_visible(locator)
        element.clear()
        element.send_keys(text)
        return self

    def get_text(self, locator: tuple) -> str:
        """Возвращает текст элемента."""
        return self.find_visible(locator).text

    def is_visible(self, locator: tuple) -> bool:
        """Проверяет видимость элемента (без исключения)."""
        try:
            return self.find_visible(locator).is_displayed()
        except Exception:
            return False

    def wait_until_visible(self, locator: tuple):
        """Ждет появления элемента и возвращает его."""
        return self.wait.until(EC.visibility_of_element_located(locator))