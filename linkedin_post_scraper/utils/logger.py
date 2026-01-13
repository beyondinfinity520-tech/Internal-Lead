import logging
import sys

def setup_logger():
    logger = logging.getLogger("LinkedInScraper")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        
        console_handler = logging.StreamHandler(sys.stdout)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(formatter)

       
        logger.addHandler(console_handler)

    return logger

logger = setup_logger()