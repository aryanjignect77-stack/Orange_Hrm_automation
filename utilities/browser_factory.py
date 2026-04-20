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

            if headless:
                options.add_argument("--headless=new")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")  # ← Critical fix: menu invisible without this
                options.add_argument("--remote-debugging-port=9222")
            else:
                options.add_argument("--start-maximized")

            try:
                service = ChromeService(ChromeDriverManager().install())
            except Exception:
                service = ChromeService()

            driver = webdriver.Chrome(service=service, options=options)

        elif browser == "edge":
            options = EdgeOptions()
            options.add_argument("--disable-notifications")

            if headless:
                options.add_argument("--headless=new")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")  # ← Same fix for edge
            else:
                options.add_argument("--start-maximized")

            service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service, options=options)

        elif browser == "firefox":
            options = FirefoxOptions()
            options.add_argument("--start-maximized")

            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)

        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        return driver


def get_driver(browser_name: str, headless: bool = False):
    return BrowserFactory.get_driver(browser_name, headless)