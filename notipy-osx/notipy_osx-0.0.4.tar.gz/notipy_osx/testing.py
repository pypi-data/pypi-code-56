# This file is never used in the modules. It is only meant for testing parts of the package

# # pylint: disable=import-error
# from notification import notify
# from dialog import dialog_prompt

from notipy_osx import dialog_prompt, notify

# notify(title='New Notifiation', delay=3)

a = dialog_prompt('First', buttons=['Yes', 'No'])
print(a.button_returned)