"""
This workflow action sends a credit limit approval form link in
an email to one or more users.

The form has a title, content, a credit limit float field,
a long form comments box, and Approve/Reject buttons::

    Title

    Content

    Credit Limit: _________________________
    Comments: _____________________________

    Approve | Reject

The action takes the following parameters:

- Parameter1: Email Notification Template - sent to users to notify that
  that a form is available.
- Parameter2: To list of Sage Users or Extender User Groups
- Parameter3: Form Title and Content Template - template to render for form
  title (message subject) and content (message body)
- Parameter4: Approve,Reject - steps to proceed to when approved or rejected,
  comma separated.
"""
from collections import OrderedDict

try:
    from accpac import *
    from form_client import (create_workflow_approval_form,
                             resolve_users,
                             render_title_and_content_for, )
except ImportError:
    pass

form_controls =  [
                    {
                      'name': 'RUNUSER',
                      'type': 'text',
                      'label': 'Sage User',
                      'required': True,
                    },
                    {
                      'name': 'APPRCRLIMT',
                      'type': 'float',
                      'label': 'Credit Limit',
                      'required': True,
                    },
                    {
                      'name': 'APPROVALCOMMENT',
                      'type': 'textarea',
                      'label': 'Comments',
                      'required': True,
                    }
                ]

def workflow(e):
    """Execute the workflow step.

    This function is invoked by the workflow engine.  It is called
    with ``accpac.WorkflowArgs`` and must return ``0`` on success and
    ``1`` on failed.

    :param e: the workflow arguments for this action.
    :type e: ``accpac.WorkflowArgs``
    :returns: 0/1
    :rtype: int
    """

    # Parse the actions from P4 into a { label: nextstep, } data structure
    actions = OrderedDict()
    try:
        steps = e.resolve(e.p4).split(',')
        for step in steps:
            label, next_step = step.split('=')
            actions[label] = next_step
    except (IndexError, ValueError) as s:
        showMessageBox("The actions (P4) must be a comma-separated list "
                       "of label=nextstep pairs, "
                       "eg. 'Approve=Approved+RTP,Reject=Rejected'" )
        return 1

    # Create the form, setting the initial value for the credit limit.
    try:
        title, content = render_title_and_content_for(e.resolve(e.p3), e)
        credit_limit = e.resolve("{TOVALUE}").replace(",", "")
        form = create_workflow_approval_form(
                            e.wi.viworkih.get("WIID"),
                            form_controls,
                            title,
                            content,
                            actions,
                            APPRCRLIMT=credit_limit)
    except Exception as e:
        showMessageBox("Failed to create approval form: {}".format(e))
        return 1

    # Get the url for the form.
    url = form.get('url')
    if not url:
        error("Unable to get approval form URL.")
        return 1

    # And set it in the workflow for troubleshooting and posterity
    e.wi.setValue("FORMURL", url)

    # Resolve all users, groups, and emails from P2
    users = resolve_users(e.resolve(e.p2))

    # For each user identified, send an email with a custom link that sets
    # RUNUSER.
    for (username, email_address) in users:
        email = Email()
        email.setTo(email_address)
        if not email.load(e.resolve(e.p1)):
            error("Unable to load message template '" + e.p1 + "'")
            return 1

        # Build a custom URL for the user that defaults the runuser field.
        user_url = "{}?RUNUSER={}&".format(url, username)

        # And interpolate it into the template
        email.replace("FORMURL", user_url)

        # Do all the remaining interpolation for Workflow, View, and Globals
        # to build the subject and body.
        email.replace("", e.wi.getView())
        email.setSubject(e.resolve(email.subject))
        if email.textBody != None:
            email.setText(e.resolve(email.textBody))
        if email.htmlBody != None:
            email.setHtml(e.resolve(email.htmlBody))

        # Send the email.
        email.send()

    # Success.
    return 0
