import logging
import sys
from typing import Optional


class ScraperLogger:
    """Custom logger for scraper operations."""
    
    def __init__(self, name: str = "LinkedInScraper", level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Avoid duplicate handlers
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(level)
            
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def info(self, message: str) -> None:
        """Log info message."""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log warning message."""
        self.logger.warning(message)
    
    def error(self, message: str, exc_info: bool = False) -> None:
        """Log error message."""
        self.logger.error(message, exc_info=exc_info)
    
    def debug(self, message: str) -> None:
        """Log debug message."""
        self.logger.debug(message)
    
    def success(self, message: str) -> None:
        """Log success message with custom formatting."""
        self.logger.info(f"[✓] {message}")
    
    def failure(self, message: str) -> None:
        """Log failure message with custom formatting."""
        self.logger.error(f"[✗] {message}")


# Global logger instance
logger = ScraperLogger()
