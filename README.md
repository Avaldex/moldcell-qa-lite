# My Moldcell: QA test assignment

Manual testing, defect report and two automated UI tests for the **my moldcell**
Android app (`md.moldcell.selfservice`), unauthenticated part only.

## Structure
```
README.md
manual/        checklist.md, bugs.md, summary.md, evidence/ (screenshots)
automation/
  locators.py          ALL locators in one place
  helpers.py           small UI helper (explicit waits)
  conftest.py          settings from .env, new session + app restart per test,
                       screenshot + page source on failure
  test_login_flow.py   positive test + negative test
```

## Environment used
- Android Studio emulator Pixel 6a, Android 13 (API 33), app installed from Google Play
- Appium 2.x started with the `appium` command (UiAutomator2 driver), `http://127.0.0.1:4723`
- Python 3.12, Android SDK platform-tools (`adb` in PATH), `ANDROID_HOME` and `JAVA_HOME` set

## Precondition for the tests
Open the app once by hand and choose a language, so that it starts on the login screen
("добро пожаловать в my moldcell!"). Stay logged out. The tests restart the app but keep
its data, so the language stays selected.

## Setup
```
py -3.12 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env      (then set UDID from `adb devices`)
```
`.env` is git-ignored; no real phone numbers, passwords or secrets are stored.

## Run
1. Start the emulator; `adb devices` must show it with status `device`.
2. Start Appium in another terminal: `appium`. Close any Appium Inspector session.
3. From the repository root, one command:
```
pytest
```
On failure a screenshot and the page source are saved to `reports/`.

## What the tests do
- **Positive:** the login screen shows the username and password fields, "Войти",
  "Забыли пароль?" and "Регистрация".
  **Positive** the login is succeed with correct email and passwordr
- **Negative:** with an empty form, touching the fields and tapping "Войти" shows
  "Пожалуйста, введите имя пользователя." and the user stays on the login screen.
  No credentials are entered and nothing is submitted.
- **Negative (server):** a login attempt with a non-existent account (`FAKE_USERNAME` /
  `FAKE_PASSWORD` from `.env`) must not log the user in; the login screen stays.

## Optional: authorized test (outside the assignment scope)
`automation/test_profile_authorized.py` logs in with a disposable test account and renames the
profile. It is excluded from the default run and needs `LOGIN_USERNAME` / `LOGIN_PASSWORD` in `.env`:
```
pytest -m authorized
```
It changes only the display name (no balance, tariff or payment). The app stays logged in afterwards,
so log out manually before running the default tests again.

## Design decisions
- Tests are independent: each one starts a new session and restarts the app.
- Locators are centralized in `automation/locators.py`.
- Explicit waits only (`WebDriverWait`); no fixed sleeps.
- No test data or credentials in code; settings come from `.env`.
- Every assertion has a message; screenshot and page source are saved on failure.

## Limitations
- The tests rely on the precondition above (language already chosen) and on the Russian UI texts.
- Compose elements have few resource-ids, so text-based locators are used and depend on
  the app language and version.
- A failure in the `driver` fixture (no Appium connection, device offline, app does not
  start) is an environment problem. An assertion failure with the app on screen points
  to application behaviour.
- During manual testing one disposable-email test account was created while exploring the
  registration flow. Phone-number registration, "С новым номером", payments and tariff changes
  were not tested. The authorized part is covered only by the optional test above.
