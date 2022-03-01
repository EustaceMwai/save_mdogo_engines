import smtplib, ssl

from config import logger

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "eustacemwai263@gmail.com"  # Enter your address
receiver_email = "emwai@onfonmedia.com"  # Enter receiver address
password = "Eustacemw@263"
message = """\
Subject: Hi there

This message is sent from Python by Eustace."""


def send_davis_email():
    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(smtp_server, port, context)
        print("hits before login")
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()

    except Exception as e:
        logger.error("send_davis_email error {}".format(e))
        logger.error(e, exc_info=True)
        raise


if __name__ == "__main__":
    try:
        send_davis_email()

    except Exception as e:
        logger.error('Main error: {}'.format(str(e)))
        logger.error(e, exc_info=True)