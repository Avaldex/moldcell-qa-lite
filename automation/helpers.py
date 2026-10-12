"""Tiny UI helper: explicit waits only, no fixed sleeps."""
import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Ui:
    def __init__(self, driver, timeout: int = 20):
        self.driver = driver
        self.timeout = timeout

    @staticmethod
    def _check_filled(locator):

        if "TODO" in locator[1]:
            pytest.fail(
                f"Locator {locator} is a placeholder. Fill it in automation/locators.py "
                f"using Appium Inspector.",
                pytrace=False,
            )

    def wait_visible(self, locator, timeout=None):
        self._check_filled(locator)
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def is_visible(self, locator, timeout=None) -> bool:
        try:
            self.wait_visible(locator, timeout)
            return True
        except TimeoutException:
            return False

    def tap(self, locator):
        self._check_filled(locator)
        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        ).click()

    def type_text(self, locator, text: str):
        element = self.wait_visible(locator)
        element.clear()
        element.send_keys(text)
