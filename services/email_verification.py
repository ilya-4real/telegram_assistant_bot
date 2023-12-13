import aiosmtplib

import random
import re
from email.message import EmailMessage

from config import EMAIL_SENDER, EMAIL_PASSWORD, SMTP_HOST, SMTP_PORT


def check_email(email: str) -> str | None:
    found_email = re.search(r"( .*@\w+\.\w+)", email)
    ready_email = found_email.group().strip()
    return ready_email


def generate_verification_code():
    code = ''
    for _ in range(6):
        code += str(random.randint(0, 9))
    return code

def get_email_template(username: str, user_email: str, code: str):
    email = EmailMessage()
    email['Subject'] = "Telegram assistant verification"
    # email['From'] = EMAIL_SENDER
    # email['To'] = user_email
    email.set_content(
        'hello'
    )


async def send_email(username: str, user_email: str):
    code = generate_verification_code()
    message = get_email_template(username, user_email, code)
    await aiosmtplib.send(
        message,
        recipients=[user_email],
        sender=EMAIL_SENDER,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        password=EMAIL_PASSWORD,
        use_tls=True
        )
