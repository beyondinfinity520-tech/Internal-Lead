import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    def __init__(self):
 
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.password = os.getenv("GMAIL_APP_PASSWORD")
        self.recipient_email = os.getenv("RECIPIENT_EMAIL")


        if not self.sender_email:
            print(" ERROR: 'SENDER_EMAIL' not found in .env file!")
        else:
            print(f"Email credentials loaded: {self.sender_email}")
        
        if not self.password:
            print("ERROR: 'GMAIL_APP_PASSWORD' not found in .env file!")

    def send_csv(self, file_path, lead_count):
        if not self.sender_email or not self.password:
            print("Email settings are incomplete. Cannot send email.")
            return

        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.recipient_email
        msg['Subject'] = f"Naukri Jobs Report - {datetime.now().strftime('%Y-%m-%d')}"

        body = f"The automated Naukri job scrape is complete.\n\nTotal Unique Leads: {lead_count}\nDate: {datetime.now().strftime('%Y-%m-%d')}\n\nPlease find the attached CSV file."
        msg.attach(MIMEText(body, 'plain'))

        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(file_path)}")
                msg.attach(part)

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.sender_email, self.password)
            server.send_message(msg)
            server.quit()
            print(f"SUCCESS: Email sent successfully to {self.recipient_email}!")
            
        except Exception as e:
            print(f" SMTP ERROR: {e}")