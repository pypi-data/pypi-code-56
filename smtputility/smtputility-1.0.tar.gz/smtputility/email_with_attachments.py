import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def email_with_attachments(
    message: str,
    subject: str,
    to_list: str,
    cc_list: str,
    login: str,
    password: str,
    *args
):
    """ Send email with 1-3 attachments to given list of recipients. HTML body can also include inline chart if chart is also sent as an attachment.\n
        See Examples/Email_Strings.py \n
        Example Call - email_with_attachments(emailbody,subjectstring,to_list,cc_list,attachment1=r'c:/users/mjensen/report.xlsx',attachment2=r'c:/users/mjensen/report.doc',attachment3=r'c:/users/mjensen/report.ppt')
        :param login:
        :param password:
        :param message: HTML String with Email message contained. See Examples/Email_Body.html.
        :param subject: Subject String
        :param to_list: Semicolon separated list of email addresses. (ex - a@abc.com; b@abc.com; c@abc.com;)
        :param cc_list: Semicolon separated list of email addresses. (ex - a@abc.com; b@abc.com; c@abc.com;)
        """

    msg = MIMEMultipart("alternative")
    body = MIMEText(message, "html")
    msg.attach(body)
    msg["Subject"] = subject
    msg["From"] = login
    msg["To"] = to_list
    msg["CC"] = cc_list
    for count, Path in enumerate(args):
        filename = os.path.basename(Path)
        attachment = open(Path, "rb")
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename= %s" % filename)
        msg.attach(part)
    mailserver = smtplib.SMTP("smtp.office365.com", 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.login(login, password)
    mailserver.sendmail(from_addr=login, to_addrs=to_list, msg=msg.as_string())
    mailserver.quit()
