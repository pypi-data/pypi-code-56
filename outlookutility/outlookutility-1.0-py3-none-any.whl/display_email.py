from win32com.client import Dispatch


def display_email(message: str, subject: str, to_list: str, cc_list: str):
    """Display draft of email.

        :param message: HTML String with Email message contained. See Examples/Email_Strings.py
        :param subject: Subject String
        :param to_list: Semicolon separated list of email addresses. (ex - a@abc.com; b@abc.com; c@abc.com;)
        :param cc_list: Semicolon separated list of email addresses. (ex - a@abc.com; b@abc.com; c@abc.com;)
        """
    ol_mail_item = 0x0
    obj = Dispatch("Outlook.Application")
    new_mail = obj.CreateItem(ol_mail_item)
    new_mail.Subject = subject
    new_mail.GetInspector()
    new_mail.To = to_list
    new_mail.CC = cc_list
    index = new_mail.HTMLbody.find(">", new_mail.HTMLbody.find("<body"))
    new_mail.HTMLbody = (
            new_mail.HTMLbody[: index + 1] + message + new_mail.HTMLbody[index + 1:]
    )
    # noinspection PyStatementEffect
    new_mail.display
