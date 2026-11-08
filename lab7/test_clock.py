import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Точные данные, которые мы получили через adb
APP_PACKAGE = "com.google.android.deskclock"
APP_ACTIVITY = ".DeskClock"
TIMEOUT = 15

@pytest.fixture()
def driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.platform_version = "11"
    options.device_name = "emulator-5554" 
    options.app_package = APP_PACKAGE
    options.app_activity = APP_ACTIVITY
    options.automation_name = "UiAutomator2"
    options.no_reset = True

    # Подключаемся к локальному Appium серверу
    drv = webdriver.Remote("http://127.0.0.1:4723", options=options)
    drv.wait = WebDriverWait(drv, TIMEOUT)
    yield drv
    drv.quit()

def test_clock_app_launches(driver):
    """Проверяем, что приложение Часы открылось (ищем текстовые элементы на экране)"""
    time_element = driver.wait.until(
        EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.TextView"))
    )
    assert time_element.is_displayed()
    print("Приложение Часы успешно запущено!")