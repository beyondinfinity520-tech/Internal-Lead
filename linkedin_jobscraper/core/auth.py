import os
import time
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from ..utils.cookies import save_cookies, load_cookies
from ..utils.logger import logger

load_dotenv()

EMAIL = os.getenv("LINKEDIN_EMAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")
USE_COOKIES = os.getenv("USE_COOKIES", "true").lower() == "true"

class LinkedInAuth:

    @staticmethod
    def is_logged_in(driver) -> bool:
        return "feed" in driver.current_url

    @staticmethod
    def login(driver):
        logger.info("Opening LinkedIn...")
        driver.get("https://www.linkedin.com/")
        time.sleep(3)

        if USE_COOKIES and load_cookies(driver):
            driver.refresh()
            time.sleep(3)
            if LinkedInAuth.is_logged_in(driver):
                logger.info("Logged in using cookies")
                return
            logger.warning("Cookies invalid, doing fresh login...")

        driver.get("https://www.linkedin.com/login")
        time.sleep(2)

        driver.find_element(By.NAME, "session_key").send_keys(EMAIL)
        driver.find_element(By.NAME, "session_password").send_keys(PASSWORD + Keys.RETURN)
        time.sleep(5)

        if LinkedInAuth.is_logged_in(driver):
            logger.info("Login successful Saving cookies...")
            save_cookies(driver)
        else:
            raise Exception("LinkedIn login failed")
