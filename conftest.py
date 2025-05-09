from email.policy import default

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def pytest_addoption(parser):
    parser.addoption("--MobileEmulation", action="store", default="iPhone 12 Pro",
                     choices=("iPhone 12 Pro", False), help="Testing in MobileEmulation or not")
    parser.addoption("--browser", action='store', default="chrome",
                   choices=("chrome", "Chrome"), help="Choice the test platform")
    parser.addoption("--windows-size", action='store', default="390,844",
                   help="emulation size")
    parser.addoption("--headless", action='store', default=False,
                   choices=(True, False), help="Headless mode?")

@pytest.fixture(scope="session")
def driver_options_modifier(request) -> Options:
    """
    Take command line parameter by leverage pytest_addoption() to alter the driver options
    :param request: pytest build-in parameters passed by fixture. Do nothing with it
    :return: Options for drivers to modify browser behaviour
    """
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    mobile_emulation_test =  request.config.getoption("--MobileEmulation")
    window_size = request.config.getoption("--windows-size")
    headless = request.config.getoption("--headless")

    if mobile_emulation_test:
        options.add_experimental_option("mobileEmulation", {"deviceName": mobile_emulation_test})

    if window_size:
        options.add_argument(window_size)

    if headless:
        options.add_argument("headless=new")

    return options

@pytest.fixture(scope="function")
def driver(request, driver_options_modifier) -> webdriver:
    """
    yield the webdriver depends on command line options, default chrome driver.

    :param request: pytest build-in parameters passed by fixture. Do nothing with it
    :param driver_options_modifier: Take the desired options from, passed by fixture driver_options_modifier()
    :yield: webdriver
    """
    options = driver_options_modifier
    browser = request.config.getoption("--browser").lower()

    match browser:
        case "chrome":
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            driver.maximize_window()
            yield  driver
        case _:
            raise EnvironmentError("There are no proper WebDriver")
    driver.quit()


