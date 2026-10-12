"""All UI locators in ONE place. If the UI changes, fix it here, not in the tests.

The login screen is built with Jetpack Compose and exposes few resource-ids, so most
elements are located by visible text (Russian UI). `login_screen` is a resource-id seen
in Appium Inspector. VERIFY the text/instance locators in Appium Inspector and adjust
them if a test cannot find an element.
"""
from appium.webdriver.common.appiumby import AppiumBy


def by_text(text: str):
    return (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")')


def edit_text(index: int):
    """N-th text input on the screen (0 = first). Replace with a resource-id if one exists."""
    return (
        AppiumBy.ANDROID_UIAUTOMATOR,
        f'new UiSelector().className("android.widget.EditText").instance({index})',
    )



LOGIN_SCREEN = (AppiumBy.XPATH, '//View[@id="login_screen"]')
USERNAME_INPUT = edit_text(0)
PASSWORD_INPUT = edit_text(1)
LOGIN_BUTTON = by_text("Войти")
FORGOT_PASSWORD_LINK = by_text("Забыли пароль?")
REGISTER_LINK = by_text("Регистрация")
ALERT_MESSAGE = (AppiumBy.XPATH, '//*[contains(@text, "имя")]')

USERNAME_REQUIRED_ERROR = by_text("Неверное имя пользователя или пароль.")


SETUP_BIOMETRICS_LATER = by_text("Настроить позже")
MY_ACCOUNT_TITLE = by_text("Мой счет")
EDIT_PROFILE_BUTTON = by_text("Редактировать")
EDIT_PROFILE_TITLE = by_text("Редактирование профиля")

CHANGE_NAME_BUTTON = (
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().text("Изменить").instance(0)',
)
NAME_DIALOG_TITLE = by_text("Введите имя")
NAME_INPUT = edit_text(0)
SAVE_BUTTON = by_text("Сохранить")
