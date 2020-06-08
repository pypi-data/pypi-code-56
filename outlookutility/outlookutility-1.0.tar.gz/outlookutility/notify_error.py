from win32com.client import Dispatch
from datetime import datetime


def notify_error(report_name, error_log, to_list: str):
    """Auto-notify for automated scripts crashing.

    :param to_list: List of emails to receive notification.
    :param report_name: Name of automated report.
    :param error_log: Raised exception or other error to report.
    """
    ol_mail_item = 0x0
    obj = Dispatch("Outlook.Application")
    new_mail = obj.CreateItem(ol_mail_item)
    new_mail.Subject = f"Automated Report Error Notification - {report_name}"
    new_mail.GetInspector()
    message = f"""
                                 <HTML>
                                 <BODY>
                                 {report_name} failed on execution at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
                                 <br>
                                 Error Log:
                                 <br>
                                 {error_log}
                                 <br>
                                 </BODY>
                                 </HTML>"""
    new_mail.To = to_list
    index = new_mail.HTMLbody.find(">", new_mail.HTMLbody.find("<body"))
    new_mail.HTMLbody = (
            new_mail.HTMLbody[: index + 1] + message + new_mail.HTMLbody[index + 1:]
    )
    # noinspection PyStatementEffect
    new_mail.send
