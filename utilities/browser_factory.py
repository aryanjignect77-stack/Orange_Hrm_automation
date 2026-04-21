from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class BrowserFactory:

    @staticmethod
    def get_driver(browser_name: str, headless: bool = False):
        browser = browser_name.lower()

        if browser == "chrome":
            options = ChromeOptions()
            options.add_argument("--incognito")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-extensions")

            if headless:
                options.add_argument("--headless=new")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")   # avoids /dev/shm OOM in Docker/CI
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")   # menus invisible without an explicit size
                options.add_argument("--remote-debugging-port=9222")
                options.add_argument("--ignore-certificate-errors")
            else:
                options.add_argument("--start-maximized")

            try:
                # webdriver_manager downloads the matching chromedriver automatically.
                # Falls back to the system chromedriver if the download fails (e.g. network restrictions in CI).
                service = ChromeService(ChromeDriverManager().install())
            except Exception:
                service = ChromeService()  # relies on chromedriver being on PATH

            driver = webdriver.Chrome(service=service, options=options)

        elif browser == "edge":
            options = EdgeOptions()
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-extensions")

            if headless:
                options.add_argument("--headless=new")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--ignore-certificate-errors")
            else:
                options.add_argument("--start-maximized")

            try:
                service = EdgeService(EdgeChromiumDriverManager().install())
            except Exception:
                service = EdgeService()

            driver = webdriver.Edge(service=service, options=options)

        elif browser == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
                options.add_argument("--width=1920")
                options.add_argument("--height=1080")
            else:
                options.add_argument("--start-maximized")

            try:
                service = FirefoxService(GeckoDriverManager().install())
            except Exception:
                service = FirefoxService()

            driver = webdriver.Firefox(service=service, options=options)

        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        return driver


def get_driver(browser_name: str, headless: bool = False):
    return BrowserFactory.get_driver(browser_name, headless)