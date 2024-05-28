
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, to_email):
    sender_email = "your-email@example.com"
    sender_password = "your-email-password"
    
    
    # Create the email head (sender, receiver, and subject)
    email = MIMEMultipart()
    email["From"] = sender_email
    email["To"] = to_email
    email["Subject"] = subject

    # Add body and attachments to email
    email.attach(MIMEText(body, 'plain'))

    # Create SMTP session for sending the mail
    try:
        server = smtplib.SMTP('smtp.example.com', 587)  # Use your SMTP server details
        server.starttls()  # Enable security
        server.login(sender_email, sender_password)  # Login with mail_id and password
        text = email.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Example usage:
# send_email("Test Subject", "Hello, this is a test email.", "receiver-email@example.com")

