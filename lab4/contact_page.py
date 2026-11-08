"""
ContactPage: Page Object для contact.html.
Содержит локаторы и бизнес-методы формы.
"""
from selenium.webdriver.common.by import By

from base_page import BasePage


class ContactPage(BasePage):
    # ---------- Локаторы ----------
    FORM = (By.ID, "contact-form")
    NAME_INPUT = (By.ID, "name")
    EMAIL_INPUT = (By.ID, "email")
    SUBJECT_SELECT = (By.ID, "subject")
    MESSAGE_TEXTAREA = (By.ID, "message")
    AGREE_CHECKBOX = (By.ID, "agree")
    SUBMIT_BUTTON = (By.ID, "submit-btn")

    SUCCESS_MESSAGE = (By.ID, "success-message")

    NAME_ERROR = (By.ID, "name-error")
    EMAIL_ERROR = (By.ID, "email-error")
    SUBJECT_ERROR = (By.ID, "subject-error")
    MESSAGE_ERROR = (By.ID, "message-error")
    AGREE_ERROR = (By.ID, "agree-error")

    # ---------- Действия ----------
    def fill_name(self, name: str):
        self.type(self.NAME_INPUT, name)
        return self

    def fill_email(self, email: str):
        self.type(self.EMAIL_INPUT, email)
        return self

    def select_subject(self, subject_value: str):
        """subject_value: 'order' | 'support' | 'other'."""
        from selenium.webdriver.support.ui import Select
        Select(self.find_visible(self.SUBJECT_SELECT)).select_by_value(subject_value)
        return self

    def fill_message(self, message: str):
        self.type(self.MESSAGE_TEXTAREA, message)
        return self

    def check_agree(self):
        checkbox = self.find_visible(self.AGREE_CHECKBOX)
        if not checkbox.is_selected():
            checkbox.click()
        return self

    def submit(self):
        self.click(self.SUBMIT_BUTTON)
        return self

    def fill_form(self, name: str, email: str, subject: str, message: str, agree: bool = True):
        """Заполняет всю форму за один вызов."""
        self.fill_name(name)
        self.fill_email(email)
        self.select_subject(subject)
        self.fill_message(message)
        if agree:
            self.check_agree()
        return self

    # ---------- Проверки ----------
    def get_success_text(self) -> str:
        return self.get_text(self.SUCCESS_MESSAGE)

    def is_success_visible(self) -> bool:
        return self.is_visible(self.SUCCESS_MESSAGE)

    def is_form_visible(self) -> bool:
        return self.is_visible(self.FORM)

    def get_name_error(self) -> str:
        return self.get_text(self.NAME_ERROR)

    def get_email_error(self) -> str:
        return self.get_text(self.EMAIL_ERROR)

    def get_subject_error(self) -> str:
        return self.get_text(self.SUBJECT_ERROR)

    def get_message_error(self) -> str:
        return self.get_text(self.MESSAGE_ERROR)

    def get_agree_error(self) -> str:
        return self.get_text(self.AGREE_ERROR)