import smtplib
from email.message import EmailMessage
from datetime import datetime


def notify_error(report_name, error_log, to_list: str, login: str, password: str):
    """Auto-notify for automated scripts crashing.

    :param report_name: Name of automated report.
    :param error_log: Raised exception or other error to report.
    :param to_list: Semicolon separated list of email addresses. (ex - a@abc.com; b@abc.com; c@abc.com;)
    :param login: Office 365 login email. This is also used for the from field.
    :param password: Office 365 password.
    """
    mailserver = smtplib.SMTP("smtp.office365.com", 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.login(login, password)
    msg = EmailMessage()
    msg.add_header("Content-Type", "text/html")
    message = f"""
                                    <HTML>
                                    <BODY>
                                    {report_name} failed on execution at {datetime.now().strftime("%m/%d/%Y %H:%M:%S")}
                                    <br>
                                    Error Log:
                                    <br>
                                    {error_log}
                                    <br>
                                    </BODY>
                                    </HTML>"""
    msg.set_payload(message)
    msg["Subject"] = f"Automated Report Error Notification - {report_name}"
    msg["From"] = login
    msg["To"] = to_list
    mailserver.send_message(msg)
    mailserver.quit()
