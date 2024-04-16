from dotenv import load_dotenv
from os import getenv
from smtplib import SMTP_SSL
from ssl import create_default_context
from email.message import EmailMessage
import imghdr
from time import strftime


load_dotenv()
SENDER = getenv("sender")
PASSWORD = getenv("password")
RECEIVER = getenv("receiver")
HOST = "smtp.gmail.com"
TIME = strftime("%d/%m/%Y - %H:%M")

def send_email():
    """
    Sends an email through a gmail account, with an image attached and default 
    content (body).
    """
    message = EmailMessage()
    message["Subject"] = "Object detected"
    message.set_content(f"An object has been detected ({TIME})")
    
    with open("image.png", "rb") as file:
        image = file.read()
    message.add_attachment(image, maintype="image", subtype=imghdr.what(None, image))
    
    with SMTP_SSL(HOST, context=create_default_context()) as server:
        server.login(SENDER, PASSWORD)
        server.send_message(message, SENDER, RECEIVER)


if __name__ == "__main__":
    send_email()