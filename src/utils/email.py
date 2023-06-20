from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def send_message(payload: str, to: str):
    msg = MIMEMultipart()
    msg['From'] = 'pratayeu@yandex.ru'
    msg['To'] = to
    msg['Subject'] = 'FastApi'

    msg.attach(MIMEText(payload))

    server = smtplib.SMTP('smtp.yandex.ru', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('pratayeu@yandex.ru', 'oyyaehwnlvdwlexy')
    server.sendmail(
        'pratayeu@yandex.ru',
        to,
        msg.as_string()
    )
    server.quit()
