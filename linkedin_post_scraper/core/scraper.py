import time
from selenium.webdriver.common.by import By
from config.settings import ScraperConfig
from models.post import PostLead, PostCollection

class PostScraper:
    def __init__(self, driver, limit):
        self.driver = driver
        self.limit = limit
        self.config = ScraperConfig()

    def scrape(self, keyword):
        query = keyword.replace(" ", "%20")
        url = (
            "https://www.linkedin.com/search/results/content/"
            f"?keywords={query}&datePosted=%22past-24h%22"
        )

        self.driver.get(url)
        time.sleep(5)

        collection = PostCollection()
        scraped_urls = set()
   
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        stagnant_scrolls = 0

        while len(collection.leads) < self.limit:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)

            try:
                btns = self.driver.find_elements(By.CSS_SELECTOR, self.config.MORE_BTN_CSS)
                for btn in btns:
                    if btn.is_displayed():
                        self.driver.execute_script("arguments[0].click();", btn)
                        time.sleep(2)
            except:
                pass

            cards = self.driver.find_elements(By.CSS_SELECTOR, self.config.CARD_CSS)
            pre_scrape_count = len(collection.leads)

            for card in cards:
                if len(collection.leads) >= self.limit:
                    break
                try:
                    urn = card.get_attribute("data-urn") or \
                          card.find_element(By.XPATH, "./..").get_attribute("data-id")

                    post_url = f"https://www.linkedin.com/feed/update/{urn}/"

                    if post_url not in scraped_urls:
                        lead = PostLead(
                            author=card.find_element(By.CSS_SELECTOR, self.config.AUTHOR_CSS).text.strip(),
                            profile_url=card.find_element(
                                By.CSS_SELECTOR,
                                ".update-components-actor__meta-link"
                            ).get_attribute("href").split('?')[0],
                            headline=card.find_element(By.CSS_SELECTOR, self.config.HEADLINE_CSS).text.strip(),
                            post_url=post_url,
                            text=card.find_element(By.CSS_SELECTOR, self.config.TEXT_CSS).text.strip()
                        )
                        collection.add_lead(lead)
                        scraped_urls.add(post_url)
                except:
                    continue

            new_height = self.driver.execute_script("return document.body.scrollHeight")
 
            if len(collection.leads) == pre_scrape_count and new_height == last_height:
                stagnant_scrolls += 1
            else:
                stagnant_scrolls = 0 

            if stagnant_scrolls >= 3:
                print("End of search results reached.")
                break

            last_height = new_height

        return collection