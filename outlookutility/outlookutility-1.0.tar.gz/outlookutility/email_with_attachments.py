from win32com.client import Dispatch


def email_with_attachments(
        message: str, subject: str, to_list: str, cc_list: str, *args
):
    """ Send email with 1-3 attachments to given list of recipients. HTML body can also include inline chart if chart is also sent as an attachment.\n
    See Examples/Email_Strings.py \n
    Example Call - email_with_attachments(emailbody,subjectstring,to_list,cc_list,attachment1=r'c:/users/mjensen/report.xlsx',attachment2=r'c:/users/mjensen/report.doc',attachment3=r'c:/users/mjensen/report.ppt')

    :param message: HTML String with Email message contained. See Examples/Email_Body.html.
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
    for count, Path in enumerate(args):
        print("{0}. {1}".format(count, Path))
        new_mail.Attachments.Add(Source=Path)
    index = new_mail.HTMLbody.find(">", new_mail.HTMLbody.find("<body"))
    new_mail.HTMLbody = (
            new_mail.HTMLbody[: index + 1] + message + new_mail.HTMLbody[index + 1:]
    )
    # noinspection PyStatementEffect
    new_mail.send
