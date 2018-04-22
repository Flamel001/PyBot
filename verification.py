import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import bot


def pin_generator():
    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    passlen = 8
    p = "".join(random.sample(s, passlen))
    return p


def pin_sender(email, pin):
    fromaddr = "innolibbot@gmail.com"
    toaddr = str(email)
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "PIN-code verification for Innopolis's library system"

    body = str(pin)
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "401206176")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    print("Message has been sent with PIN:" + str(body))
    server.quit()


def mesage_sender(email, message):
    fromaddr = "innolibbot@gmail.com"
    toaddr = str(email)
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Notification about outstanding request"

    body = message
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "401206176")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    print("Message has been sent with PIN:" + str(body))
    server.quit()
