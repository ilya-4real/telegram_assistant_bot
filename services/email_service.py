import aiosmtplib

import random
import re
from email.message import EmailMessage

from .exceptions import InvalidEmail
from config import EMAIL_SENDER, EMAIL_PASSWORD, SMTP_HOST, SMTP_PORT


def check_email(email: str) -> str | None:
    found_email = re.search(r"^.+@.+\..+$", email)
    if not found_email:
        raise InvalidEmail("Something wrong with your email. Try again")
    return found_email.string


def generate_verification_code():
    code = ''
    for _ in range(6):
        code += str(random.randint(0, 9))
    return code


def get_email_template(username: str, user_email: str, code: str):
    print(type(user_email))
    print(str(user_email))
    message = EmailMessage()
    message['Subject'] = "Telegram assistant verification"
    message['From'] = EMAIL_SENDER
    message['To'] = str(user_email)
    message.set_content(
        '<div>'
        f"<h1> Hello {username}!</h1>" 
        "<h1> Your verification code: </h1>"
        f"<h2> {code} <h2>"
        '</div>',
        subtype='html'
    )
    return message


async def send_email(username: str, user_email: str):
    email = check_email(user_email)
    code = generate_verification_code()
    message = get_email_template(username, email, code)
    await aiosmtplib.send(
        message,
        hostname=SMTP_HOST,
        username=EMAIL_SENDER,
        password=EMAIL_PASSWORD,
        port=SMTP_PORT,
        use_tls=True
        )
    return code
