import os
import pytest

from applitools.selenium import *
from selenium.webdriver import Chrome, ChromeOptions, Remote
from selenium.webdriver.common.by import By
from testlib.inputs import User


# --------------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------------

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
def webdriver():
  options = ChromeOptions()
  options.set_capability('applitools:tunnel', 'true')

  driver = Remote(
    command_executor=Eyes.get_execution_cloud_url(),
    options=options)

  yield driver
  driver.quit()


@pytest.fixture(scope='function')
def eyes(
  runner: VisualGridRunner,
  configuration: Configuration,
  webdriver: Remote,
  request: pytest.FixtureRequest):

  eyes = Eyes(runner)
  eyes.set_configuration(configuration)

  eyes.open(
    driver=webdriver,
    app_name='Bulldoggy: The Reminders App',
    test_name=request.node.name,
    viewport_size=RectangleSize(1024, 768))
  
  yield eyes
  eyes.close_async()


@pytest.fixture(scope='function')
def non_eyes_driver(
  batch_info: BatchInfo,
  webdriver: Remote,
  request: pytest.FixtureRequest):

  webdriver.execute_script(
    "applitools:startTest",
    {
      "testName": request.node.name,
      "appName": "Bulldoggy: The Reminders App",
      "batch": {"id": batch_info.id}
    }
  )
  
  yield webdriver

  status = 'Failed' if request.node.test_result.failed else 'Passed'
  webdriver.execute_script("applitools:endTest", {"status": status})


# --------------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------------

def test_login_visually(webdriver: Remote, eyes: Eyes):

  # Load the login page
  webdriver.get("http://127.0.0.1:8000/login")

  # Check the login page
  eyes.check(Target.window().fully().with_name("Login page"))

  # Perform login
  webdriver.find_element(By.NAME, "username").send_keys('pythonista')
  webdriver.find_element(By.NAME, "password").send_keys("I<3testing")
  webdriver.find_element(By.XPATH, "//button[.='Login']").click()

  # Check the reminders page
  eyes.check(Target.window().fully().with_name("Reminders page"))


def test_login_functionally(non_eyes_driver: Remote):

  # Load the login page
  non_eyes_driver.get("http://127.0.0.1:8000/login")

  # Perform login
  non_eyes_driver.find_element(By.NAME, "username").send_keys('pythonista')
  non_eyes_driver.find_element(By.NAME, "password").send_keys("I<3testing")
  non_eyes_driver.find_element(By.XPATH, "//button[.='Login']").click()

  # Check the reminders page
  assert non_eyes_driver.find_element(By.ID, 'bulldoggy-logo')
  assert non_eyes_driver.find_element(By.ID, 'bulldoggy-title').text == 'Bulldoggy'
  assert non_eyes_driver.find_element(By.XPATH, "//button[.='Logout']")
  assert non_eyes_driver.title == 'Reminders | Bulldoggy reminders app'
