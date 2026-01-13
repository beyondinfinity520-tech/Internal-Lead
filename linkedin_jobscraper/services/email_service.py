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
        self.sender_email = os.getenv("LINKEDIN_EMAIL")
        self.password = os.getenv("GMAIL_APP_PASSWORD") 
        self.recipient_email = os.getenv("RECIPIENT_EMAIL")

    def send_csv(self, file_path, lead_count):
        """
        Sends the scraped leads CSV via Gmail SMTP.
        """
        if not os.path.exists(file_path):
            print(f"DEBUG: File {file_path} not found. Skipping email.")
            return
        
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.recipient_email
        msg['Subject'] = f"LinkedIn Job Leads Report - {datetime.now().strftime('%Y-%m-%d')}"

  
        body = f"""
        Hello,

        The LinkedIn Job Scraper has completed for today.
        
        Summary:
        - Total Leads Collected: {lead_count}
        - Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

        Please find the attached CSV file for details.

        Regards,
        Automated Scraper
        """
        msg.attach(MIMEText(body, 'plain'))

        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition", 
                    f"attachment; filename={os.path.basename(file_path)}"
                )
                msg.attach(part)
        except Exception as e:
            print(f"Error attaching file: {e}")
            return

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.sender_email, self.password)
            server.send_message(msg)
            server.quit()

            print("\n" + "*"*60)
            print(f"SUCCESS: Email sent to {self.recipient_email}")
            print(f"Leads included: {lead_count}")
            print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
            print("*"*60 + "\n")
            
        except Exception as e:
            print("\n" + "!"*60)
            print(f"EMAIL FAILED: {e}")
            print("Check your GMAIL_APP_PASSWORD and Sender Email in .env")
            print("!"*60 + "\n")