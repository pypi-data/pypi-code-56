import smtplib
from email.message import EmailMessage


def email_without_attachment(
    message: str, subject: str, to_list: str, cc_list: str, login: str, password: str
):
    """Send email to given list of recipients. Uses Office 365 Port 587.

    :param message: HTML String with Email message contained. See Examples/Email_Strings.py
    :param subject: Subject String
    :param to_list: Semicolon separated list of email addresses. (ex - a@abc.com; b@abc.com; c@abc.com;)
    :param cc_list: Semicolon separated list of email addresses. (ex - a@abc.com; b@abc.com; c@abc.com;)
    :param login: Office 365 login email. This is also used for the from field.
    :param password: Office 365 password.
    """
    mailserver = smtplib.SMTP("smtp.office365.com", 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.login(login, password)
    msg = EmailMessage()
    msg.add_header("Content-Type", "text/html")
    msg.set_payload(message)
    msg["Subject"] = subject
    msg["From"] = login
    msg["To"] = to_list
    msg["CC"] = cc_list
    mailserver.send_message(msg)
    mailserver.quit()
