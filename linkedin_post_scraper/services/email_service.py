import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

class EmailService:
    def __init__(self):
        self.sender_email = os.getenv("LINKEDIN_EMAIL")
        self.password = os.getenv("GMAIL_APP_PASSWORD") 
        self.recipient_email = os.getenv("RECIPIENT_EMAIL")

    def send_csv(self, file_path, lead_count):
        if not os.path.exists(file_path):
            print(f"File {file_path} not found. Skipping email.")
            return

        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.recipient_email
        msg['Subject'] = f"LinkedIn Leads Report - {datetime.now().strftime('%Y-%m-%d')}"

        body = f"The daily scrape is complete.\nTotal leads collected: {lead_count}\nAttached is the CSV file."
        msg.attach(MIMEText(body, 'plain'))

        with open(file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(file_path)}")
            msg.attach(part)

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.sender_email, self.password)
            server.send_message(msg)
            server.quit()
            print(f"Email sent to {self.recipient_email}")
        except Exception as e:
            print(f" Email failed: {e}")