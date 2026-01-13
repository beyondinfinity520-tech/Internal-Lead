import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def send_unified_report(file_paths):
    sender = os.getenv("RECIPIENT_EMAIL")
    password = os.getenv("GMAIL_APP_PASSWORD")
    recipient = os.getenv("RECIPIENT_EMAIL")

    if not sender or not password or not recipient:
        print("Error: Email credentials missing in .env")
        return

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = f"Unified Daily Leads Report - {datetime.now().strftime('%Y-%m-%d')}"

    body = "Hello,\n\nThe daily scraping cycle is complete. Please find attached the reports for LinkedIn Jobs, LinkedIn Posts, and Naukri.\n\nRegards,\nAutomated Scraper"
    msg.attach(MIMEText(body, 'plain'))

    for file_path in file_paths:
        if os.path.exists(file_path):
            try:
                with open(file_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(file_path)}")
                    msg.attach(part)
            except Exception as e:
                print(f"Error attaching {file_path}: {e}")

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        print(f"SUCCESS: Combined email sent to {recipient}")
    except Exception as e:
        print(f"SMTP FAILED: {e}")