import os
import time
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

load_dotenv()

# Configure a simple logger for this module
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LinkedInAuth:

    @staticmethod
    def is_logged_in(driver) -> bool:
        return "feed" in driver.current_url

    @staticmethod
    def login(driver):
        cookie = os.getenv("LINKEDIN_COOKIE")
        if cookie:
            logger.info("Attempting login with session cookie...")
            driver.get("https://www.linkedin.com")
            driver.add_cookie({"name": "li_at", "value": cookie})
            driver.get("https://www.linkedin.com/feed/")
            time.sleep(3)
            if LinkedInAuth.is_logged_in(driver):
                logger.info("Cookie login successful!")
                return
            else:
                logger.warning("Cookie login failed. Falling back to username/password.")

        email = os.getenv("LINKEDIN_EMAIL")
        password = os.getenv("LINKEDIN_PASSWORD")
        if not email or not password:
            raise ValueError("LinkedIn credentials (LINKEDIN_EMAIL, LINKEDIN_PASSWORD) not found in environment variables.")

        logger.info("Opening LinkedIn for username/password login...")
        driver.get("https://www.linkedin.com/login")
        
        wait = WebDriverWait(driver, 20)

        try:
            username_field = wait.until(EC.visibility_of_element_located((By.ID, "username")))
            username_field.send_keys(email)

            password_field = wait.until(EC.visibility_of_element_located((By.ID, "password")))
            password_field.send_keys(password + Keys.RETURN)
            
            time.sleep(5)

            if not LinkedInAuth.is_logged_in(driver):
                current_url = driver.current_url
                raise Exception(f"LinkedIn login failed. Expected 'feed' in URL, but was on: {current_url}")
            logger.info("Login successful")
        except Exception as e:
            logger.error(f"Login failed: {e}")
            raise e