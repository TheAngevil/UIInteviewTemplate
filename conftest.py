import pytest
import logging
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as chrome_options
from webdriver_manager.chrome import ChromeDriverManager


def pytest_addoption(parser):
    """
    adaptor of the command line variables
    :param parser:
    :return:
    """
    parser.addoption("--MobileEmulation", action="store", default="iPhone 14 Pro Max",
                     choices=("iPhone 14 Pro Max", False), help="Testing in MobileEmulation or not. Options: True/False")
    parser.addoption("--browser", action='store', default="chrome",
                   choices=("chrome", "Chrome"), help="Choice the test platform, Options: Chrome")
    parser.addoption("--windows-size", action='store', default="344,746",
                   help="emulation size, Option: 'Width: x pixel, Length: y pixel', e.g.: '430,932'")
    parser.addoption("--headless", action='store', default=False,
                   choices=(True, False), help="Headless mode?")
    parser.addoption("--env", action='store', default = 'Staging',
                   choices=("staging", "Staging", "UAT", "uat", "dev", "Dev"), help="Testing Env, e.g.: Staging, UAT")
    parser.addoption("--max-screen", action='store', default=True,
                   choices=(True, False), help="Max Screen? Options: True/False")

@pytest.fixture(scope="session")
def driver_options_modifier(request):
    """
    Take the command line parameter by leverage pytest_addoption() to alter the driver options
    :param request: pytest build-in parameters passed by fixture. Do nothing with it
    :return: Options for drivers to modify browser behaviour
    """
    arg ={
        'browser': request.config.getoption("--browser").lower(),
        'windows_size' : request.config.getoption("--windows-size").replace(" ", "").split(",", 1),
        'headless' : request.config.getoption("--headless"),
        'mobile_emulation_test': request.config.getoption("--MobileEmulation")

    }

    match arg['browser']:
        case "chrome" | _:
            options = chrome_options()
            options.add_argument("--no-sandbox")
            options.add_experimental_option("useAutomationExtension", False)
            options.add_experimental_option("excludeSwitches", ["enable-automation"])

            if arg['mobile_emulation_test']:
                # reference for Device information: https://github.com/alxwndr/list-of-custom-emulated-devices-in-chrome
                mobile_emulation = {
                    "deviceMetrics": {"width": int(arg['windows_size'][0]), "height": int(arg['windows_size'][1]), "pixelRatio": 3},
                    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19",
                    "clientHints": {"platform": "iOS", "mobile": True}}
                options.add_experimental_option("mobileEmulation",  mobile_emulation)
            elif arg['windows_size']:
                options.add_argument(f"--windows-size={arg['windows_size'][0]},{arg['windows_size'][1]}")

            if arg['headless']:
                options.add_argument("headless=new")

            return options

@pytest.fixture(scope="function")
def driver(request, driver_options_modifier) -> webdriver:
    """
    yield the webdriver depends on command line options, default chrome driver.

    :param request: pytest build-in parameters passed by fixture.
    :param driver_options_modifier: Take the desired options from, passed by fixture driver_options_modifier()
    :yield: webdriver
    """
    options = driver_options_modifier
    browser = request.config.getoption("--browser").lower()
    max_screen = request.config.getoption("--max-screen")

    match browser:
        case "chrome":
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            if max_screen:
                driver.maximize_window()
            yield  driver
        case _:
            raise EnvironmentError("There are no proper WebDriver")
    driver.quit()

@pytest.fixture(scope="function")
def case_name(request):
    """
    yield case name for tracking purpose
    """
    yield request.node.name

def pytest_configure():
    project_path = Path.cwd()
    logs_dir = project_path / "logs"
    logs_dir.mkdir(exist_ok=True)

    now = datetime.now()
    timestamp = now.strftime("%H:%M:%S %m-%d")
    log_file = logs_dir / f"{timestamp}.log"

    logging.getLogger(__name__)

    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_file, mode='w'),
            logging.StreamHandler()  # optional if you want both file and console
        ]
    )
