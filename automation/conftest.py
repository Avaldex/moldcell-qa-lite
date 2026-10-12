"""Fixtures. Every test starts a new Appium session and restarts the app, so tests are
independent of each other. Settings come from environment/.env."""
import datetime
import os
import pathlib

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv

from helpers import Ui

load_dotenv()

REPORTS_DIR = pathlib.Path(__file__).resolve().parent.parent / "reports"


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Remember each phase's result so the driver fixture can detect a failed test."""
    outcome = yield
    setattr(item, f"rep_{outcome.get_result().when}", outcome.get_result())


@pytest.fixture
def driver(request):
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "Android Emulator"
    options.app_package = os.getenv("APP_PACKAGE", "md.moldcell.selfservice")
    options.no_reset = True
    options.set_capability("appium:forceAppLaunch", True)
    options.set_capability("appium:shouldTerminateApp", True)
    options.auto_grant_permissions = True
    options.new_command_timeout = 120
    if os.getenv("UDID"):
        options.udid = os.getenv("UDID")
    if os.getenv("APP_ACTIVITY"):
        options.app_activity = os.getenv("APP_ACTIVITY")

    drv = webdriver.Remote(
        os.getenv("APPIUM_URL", "http://127.0.0.1:4723"), options=options
    )
    yield drv

    report = getattr(request.node, "rep_call", None)
    if report is not None and report.failed:
        REPORTS_DIR.mkdir(exist_ok=True)
        stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        base = REPORTS_DIR / f"{request.node.name}_{stamp}"
        drv.get_screenshot_as_file(f"{base}.png")
        pathlib.Path(f"{base}_page_source.xml").write_text(
            drv.page_source, encoding="utf-8"
        )
    drv.quit()


@pytest.fixture
def ui(driver) -> Ui:
    return Ui(driver)


@pytest.fixture
def fake_credentials():
    """Non-existent account for the negative login test (never a real subscriber)."""
    username = os.getenv("FAKE_USERNAME")
    password = os.getenv("FAKE_PASSWORD")
    if not username or not password:
        pytest.fail(
            "FAKE_USERNAME and FAKE_PASSWORD are not set. Copy them from .env.example to .env.",
            pytrace=False,
        )
    return username, password
