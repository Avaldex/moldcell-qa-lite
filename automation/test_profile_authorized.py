"""OPTIONAL test for the authorized part (outside the assignment scope).

Excluded from the default `pytest` run. Run it explicitly:  pytest -m authorized
It logs in with a DISPOSABLE test account whose credentials come from .env, and renames
the profile. It changes only the display name; it touches no balance, tariff or payment.

Side effect: the app stays logged in afterwards. Log out manually (or clear the app data
and choose a language again) before running the default tests, which expect the login screen.
"""
import os

import pytest

import locators as L

pytestmark = pytest.mark.authorized

NAME_A = "Test Moldcel"
NAME_B = "Moldcell Test"


@pytest.fixture
def credentials():
    username = os.getenv("LOGIN_USERNAME")
    password = os.getenv("LOGIN_PASSWORD")
    if not username or not password:
        pytest.fail(
            "LOGIN_USERNAME and LOGIN_PASSWORD are not set. Put the test account in .env "
            "(never commit it).",
            pytrace=False,
        )
    return username, password


def test_login_and_change_profile_name(ui, credentials):
    """POSITIVE (authorized): log in and change the profile name.

    Preconditions: app opens on the login screen (language chosen, logged out);
                   a disposable test account exists; credentials are in .env.
    Steps:         1. Enter the username and password, tap "Войти".
                   2. If the biometrics offer appears, tap "Настроить позже".
                   3. Open "Редактировать" and tap "Изменить" next to the name.
                   4. Enter the new name and tap "Сохранить".
    Expected:      the "Мой счет" screen opens after login, and the profile screen
                   shows the new name. The target name alternates between
                   "Moldcell Test" and "Test Moldcel", so the test can be re-run.
    """
    username, password = credentials

    assert ui.is_visible(L.LOGIN_SCREEN), "Precondition failed: login screen not displayed"
    ui.type_text(L.USERNAME_INPUT, username)
    ui.type_text(L.PASSWORD_INPUT, password)
    ui.tap(L.LOGIN_BUTTON)

    if ui.is_visible(L.SETUP_BIOMETRICS_LATER, timeout=10):
        ui.tap(L.SETUP_BIOMETRICS_LATER)

    assert ui.is_visible(L.MY_ACCOUNT_TITLE), "Login failed: 'Мой счет' screen is not shown"

    ui.tap(L.EDIT_PROFILE_BUTTON)
    assert ui.is_visible(L.EDIT_PROFILE_TITLE), "Profile editing screen did not open"

    new_name = NAME_A if ui.is_visible(L.by_text(NAME_B), timeout=3) else NAME_B

    ui.tap(L.CHANGE_NAME_BUTTON)
    assert ui.is_visible(L.NAME_DIALOG_TITLE), "Name dialog did not open"
    ui.type_text(L.NAME_INPUT, new_name)
    ui.tap(L.SAVE_BUTTON)

    assert ui.is_visible(L.by_text(new_name)), f"Profile does not show the new name '{new_name}'"
