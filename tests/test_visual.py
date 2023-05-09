import os
import pytest

from applitools.playwright import *
from playwright.sync_api import Page
from testlib.inputs import User


@pytest.fixture(scope='session')
def api_key():
  return os.getenv('APPLITOOLS_API_KEY')


@pytest.fixture(scope='session')
def runner():
  run = VisualGridRunner(RunnerOptions().test_concurrency(5))
  yield run
  print(run.get_all_test_results())


@pytest.fixture(scope='session')
def batch_info():
  return BatchInfo("Bulldoggy: The Reminders App")


@pytest.fixture(scope='session')
def configuration(api_key: str, batch_info: BatchInfo):
  config = Configuration()
  config.set_batch(batch_info)
  config.set_api_key(api_key)

  config.add_browser(800, 600, BrowserType.CHROME)
  config.add_browser(1600, 1200, BrowserType.FIREFOX)
  config.add_browser(1024, 768, BrowserType.SAFARI)
  config.add_device_emulation(DeviceName.Pixel_2, ScreenOrientation.PORTRAIT)
  config.add_device_emulation(DeviceName.Nexus_10, ScreenOrientation.LANDSCAPE)

  return config


@pytest.fixture(scope='function')
def eyes(
  runner: VisualGridRunner,
  configuration: Configuration,
  page: Page,
  request: pytest.FixtureRequest):

  eyes = Eyes(runner)
  eyes.set_configuration(configuration)

  eyes.open(
    driver=page,
    app_name='ACME Bank Web App',
    test_name=request.node.name,
    viewport_size=RectangleSize(1024, 768))
  
  yield eyes
  eyes.close_async()


def test_login_visually(page: Page, eyes: Eyes, user: User):

  # Load the login page
  page.goto('/login')

  # Check the login page
  eyes.check(Target.window().fully().with_name("Login page"))

  # Perform login
  page.locator('[name="username"]').fill(user.username)
  page.locator('[name="password"]').fill(user.password)
  page.get_by_text('Login').click()

  # Check the reminders page
  eyes.check(Target.window().fully().with_name("Reminders page"))
