from dataclasses import dataclass

@dataclass
class ScraperConfig:
    COOKIE_FILE: str = "linkedin_cookies.pkl"
    HEADLESS: bool = False  
    CARD_CSS: str = ".feed-shared-update-v2"
    MORE_BTN_CSS: str = "button.feed-shared-inline-show-more-text__see-more-less-toggle"
    AUTHOR_CSS: str = ".update-components-actor__title span[aria-hidden='true']"
    HEADLINE_CSS: str = ".update-components-actor__description span[aria-hidden='true']"
    TEXT_CSS: str = ".update-components-text span[dir='ltr']"