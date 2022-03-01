import smtplib, ssl

from config import logger

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "eustacemwai263@gmail.com"  # Enter your address
receiver_email = "emwai@onfonmedia.com"  # Enter receiver address
password = "Eustacemw@263"
message = """\
Subject: Hi there

This message is sent from Python."""




def send_mail():
    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP(smtp_server, port, context)
        server.ehlo()  # Can be omitted
        server.starttls(context)
        server.ehlo()  # Can be
        print("before login")
        server.login(sender_email, password)
        print("login success")
        server.sendmail(sender_email, receiver_email, message)
        print("mail success")

    except Exception as e:
        logger.error("send_davis_email error {}".format(e))
        logger.error(e, exc_info=True)
        raise

if __name__ == "__main__":
    try:
        send_mail()

    except Exception as e:
        logger.error('Main error: {}'.format(str(e)))
        logger.error(e, exc_info=True)