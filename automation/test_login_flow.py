"""Two independent UI tests for the login screen of my Moldcell.

Precondition for all tests: the language is already chosen, the user is logged
out, and the app opens on the login screen.
"""

import locators as L
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login_screen_shows_key_elements(ui):
    """POSITIVE: the login screen shows its key elements."""

    assert ui.is_visible(L.LOGIN_SCREEN), (
        "Login screen is not displayed. If the language screen is shown instead, "
        "choose a language once manually (precondition in README)."
    )

    for name, locator in [
        ("username field", L.USERNAME_INPUT),
        ("password field", L.PASSWORD_INPUT),
        ("Войти button", L.LOGIN_BUTTON),
        ("Забыли пароль? link", L.FORGOT_PASSWORD_LINK),
        ("Регистрация link", L.REGISTER_LINK),
    ]:
        assert ui.is_visible(locator, timeout=5), (
            f"{name} is not visible on the login screen"
        )


def test_empty_login_form_is_rejected(ui):
    """NEGATIVE: submitting an empty form is rejected."""

    assert ui.is_visible(L.LOGIN_SCREEN), (
        "Precondition failed: login screen not displayed"
    )

    ui.tap(L.USERNAME_INPUT)
    ui.tap(L.PASSWORD_INPUT)
    ui.tap(L.LOGIN_BUTTON)


    error_element = WebDriverWait(ui.driver, 10).until(
        EC.presence_of_element_located((AppiumBy.XPATH, '//*[@text="Вы не ввели пароль."]'))
    )
    assert error_element.is_displayed()


def test_login_with_wrong_credentials_is_rejected(ui, fake_credentials):
    """NEGATIVE: incorrect credentials must not log the user in."""

    username, password = fake_credentials

    assert ui.is_visible(L.LOGIN_SCREEN), (
        "Precondition failed: login screen not displayed"
    )

    ui.type_text(L.USERNAME_INPUT, username)
    ui.type_text(L.PASSWORD_INPUT, password)
    ui.tap(L.LOGIN_BUTTON)

    assert not ui.is_visible(L.MY_ACCOUNT_TITLE, timeout=8), (
        "The user was logged in with wrong credentials"
    )


    try:
        ok_button = WebDriverWait(ui.driver, 5).until(
            EC.element_to_be_clickable((AppiumBy.ID, "android:id/button1"))
        )
        ok_button.click()
    except Exception:
        pass

    assert ui.is_visible(L.LOGIN_SCREEN), (
        "User should stay on the login screen"
    )


def test_login_with_valid_credentials_is_accepted(ui):
    """POSITIVE: valid credentials log the user in successfully."""

    assert ui.is_visible(L.LOGIN_SCREEN), (
        "Precondition succeed: login screen displayed"
    )

    ui.type_text(L.USERNAME_INPUT, "moldcelltest@yopmail.com")
    ui.type_text(L.PASSWORD_INPUT, "Test12345!")
    ui.tap(L.LOGIN_BUTTON)

    save_button = WebDriverWait(ui.driver, 10).until(
        EC.presence_of_element_located((AppiumBy.XPATH, '//*[@text="Сохранить"]'))
    )
    assert save_button.is_displayed()