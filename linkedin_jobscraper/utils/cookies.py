import pickle
import os

COOKIE_FILE = "linkedin_cookies.pkl"

def save_cookies(driver):
    with open(COOKIE_FILE, "wb") as f:
        pickle.dump(driver.get_cookies(), f)

def load_cookies(driver):
    if not os.path.exists(COOKIE_FILE):
        return False

    with open(COOKIE_FILE, "rb") as f:
        cookies = pickle.load(f)

    for cookie in cookies:
        cookie.pop("sameSite", None)
        driver.add_cookie(cookie)

    return True
