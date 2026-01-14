import os
import time
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..utils.logger import logger

load_dotenv()

class LinkedInAuth:

    @staticmethod
    def is_logged_in(driver) -> bool:
        return "feed" in driver.current_url

    @staticmethod
    def login(driver):
        email = os.getenv("LINKEDIN_EMAIL")
        password = os.getenv("LINKEDIN_PASSWORD")
        if not email or not password:
            raise ValueError("LinkedIn credentials (LINKEDIN_EMAIL, LINKEDIN_PASSWORD) not found in environment variables.")

        logger.info("Opening LinkedIn...")
        driver.get("https://www.linkedin.com/login")
        
        wait = WebDriverWait(driver, 20)

        try:
            # Wait for username field to be visible
            username_field = wait.until(EC.visibility_of_element_located((By.ID, "username")))
            username_field.clear()
            username_field.send_keys(email)

            # Wait for password field to be visible
            password_field = wait.until(EC.visibility_of_element_located((By.ID, "password")))
            password_field.clear()
            password_field.send_keys(password + Keys.RETURN)
            
            time.sleep(5)

            if LinkedInAuth.is_logged_in(driver):
                logger.info("Login successful")
            else:
                raise Exception("LinkedIn login failed")
        except Exception as e:
            logger.error(f"Login failed: {e}")
            raise e
