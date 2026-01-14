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
        cookie = os.getenv("LINKEDIN_COOKIE")
        if cookie:
            logger.info("Attempting login with session cookie...")
            driver.get("https://www.linkedin.com")
            driver.add_cookie({"name": "li_at", "value": cookie})
            driver.get("https://www.linkedin.com/feed/")
            try:
                # Wait for a stable element on the feed page to ensure it's fully loaded
                WebDriverWait(driver, 15).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "input.search-global-typeahead__input"))
                )
                if LinkedInAuth.is_logged_in(driver):
                    logger.info("Cookie login successful! Feed page is ready.")
                    return
                else:
                    logger.warning("Cookie login failed after page load. Falling back to username/password.")
            except Exception:
                logger.warning("Cookie login failed: Could not verify feed page. Falling back to username/password.")
 
        email = os.getenv("LINKEDIN_EMAIL")
        password = os.getenv("LINKEDIN_PASSWORD")
        if not email or not password:
            raise ValueError("LinkedIn credentials (LINKEDIN_EMAIL, LINKEDIN_PASSWORD) not found in environment variables.")

        logger.info("Opening LinkedIn for username/password login...")
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
                current_url = driver.current_url
                error_msg = f"LinkedIn login failed. Expected 'feed' in URL, but was on: {current_url}."
                if "checkpoint" in current_url or "challenge" in current_url:
                    error_msg += " This may be a security check (CAPTCHA)."
                elif "login" in current_url:
                    error_msg += " Page did not redirect, check credentials."
                raise Exception(error_msg)
        except Exception as e:
            logger.error(f"Login failed: {e}")
            raise e
