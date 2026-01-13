import os, pickle, time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LinkedInAuth:
    @staticmethod
    def login(driver, email, password, cookie_path):
        driver.get("https://www.linkedin.com")
        
        if os.path.exists(cookie_path):
            with open(cookie_path, "rb") as f:
                cookies = pickle.load(f)
                for c in cookies:
                    if 'expiry' in c: c['expiry'] = int(c['expiry'])
                    driver.add_cookie(c)
            driver.refresh()
            time.sleep(3)
        
        if "feed" not in driver.current_url:
            driver.get("https://www.linkedin.com/login")
            driver.find_element(By.NAME, "session_key").send_keys(email)
            driver.find_element(By.NAME, "session_password").send_keys(password + Keys.RETURN)
            WebDriverWait(driver, 120).until(EC.url_contains("feed"))
            pickle.dump(driver.get_cookies(), open(cookie_path, "wb"))
        return True