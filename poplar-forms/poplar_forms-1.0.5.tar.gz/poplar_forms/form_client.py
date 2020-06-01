""" Fleeting Forms Client Library for Extender

The Fleeting Form Client performs API calls to the
fleetingforms.io service.

This library also contains helper methods that are used
across multiple workflow actions.

Structure of the file is:

- Workflow Action Helper Functions
- Client Helper Function
- FormClient Class

"""
import re
import requests

try:
    from accpac import *
except ImportError:
    pass

# Workflow helper methods

def get_user(a4wuser, userid):
    """Get a user's email from the a4wuser view.

    :param a4wuser: An open AS0003 view
    :type a4wuser: accpac.View
    :param userid: The Sage User ID.
    :type userid: str
    :returns: username and email if found, otherwise None.
    :rtype: (str, str)
    """
    user = None
    a4wuser.put("USERID", userid)
    if a4wuser.read() == 0:
        email = a4wuser.get("EMAIL1").strip()
        user = (userid, email)
    return user

def get_users_for_group(a4wuser, vigroupd, groupid):
    """Get the users and their emails for a vi group.

    :param a4wuser: An open AS0003 view
    :type a4wuser: accpac.View
    :param vigroupd: An open VI0024 view
    :type a4wuser: accpac.View
    :param groupid: The Extender Group ID.
    :returns: list of usernames and email tuples found.
    :rtype: [(str, str)]
    """
    users = []
    vigroupd.order(0) # GROUP/USERID
    vigroupd.recordClear()
    vigroupd.browse('GROUP="{}"'.format(groupid))
    while vigroupd.fetch() == 0:
        user = get_user(a4wuser, vigroupd.get("USERID"))
        if user:
            users.append(user)
    return users

def resolve_users(emails):
    """Resolve a ; separated list to a list of (username, email) tuples.

    Given a ; separated list, resolve to Sage Usernames and User Emails.
    If an email is provided directly, return the email as the username.

    Consider a configuration in which:

    - There is a group MYGRP composed of three users:

      - ANNE (anne@a.com), BOB (bobby@a.com), CHRIS (cbinckly@a.com)

    - Other users are defined in Sage but are not members of the group.

      - DARREN (darren@a.com), ESTHER (esther@a.com), FRANK (frank@a.com)

    - And some clients are not in the Sage database at all:

      - user1@client.com, user2@client.com

    .. code-block:: python

        >>> resolve_users("MYGRP;DARREN;user1@client.com")
        [(ANNE, anne@a.com), (BOB, bobby@a.com), (CHRIS, cbinckly@a.com),
         (DARREN, darren@a.com), (user1@client.com, user1@client.com)]

    :param emails: ';' separated list
    :type emails: str
    :returns: list of (username, email) tuples
    :rtype: [(str, str)]
    """
    users = []
    emails = [e.strip() for e in emails.split(";") if e]

    a4wuser = openView("AS0003")
    vigroupd = openView("VI0024")

    for email in emails:
        if re.search(r'[^@]+@.+\.\w+', email):
            users.append((email, email, ))
        elif email:
            user = get_user(a4wuser, email)
            if user:
                users.append(user)
            else:
                users += get_users_for_group(
                                a4wuser, vigroupd, email)

    a4wuser.close()
    vigroupd.close()

    return users

def render_title_and_content_for(template_name, workflow):
    """Hijack the Email templates for workflow form content.

    Renders an email template, resolving the content in the context
    of the provided workflow object and its associated view.

    :param template_name: VIMSG template name to render
    :type template_name: str
    :param workflow: workflow object to use for resolution
    :type worflow: accpac.Workflow
    :returns: (title, content)
    :rtype: (str, str)
    """
    email_renderer = Email()
    email_renderer.load(template_name)
    email_renderer.replace("", workflow.wi.getView())
    title = workflow.resolve(email_renderer.subject)
    content = workflow.resolve(email_renderer.textBody)
    return title, content

def create_workflow_approval_form(wiid, form_controls, title, content,
                                  actions, **initials):
    """Create a workflow approval form.

    Any arguments passed in the keyword arguments (``initials``) will
    be treated as initial values for fields of that name.

    For example, if a form contained a field name ``APPROVALCOMMENT``,
    it can be defaulted to "Comments are required" by using the following
    call to create_form::

        create_form(wiid, title, content,
                    APPROVALCOMMENT="Comments are required.")

    :param wiid: workflow instance ID
    :type wiid: int
    :param form_controls: list of control definitions for the form.
    :type form_controls: dict
    :param title: the title to display above the form
    :type title: str
    :param content: the instructions to display above the form.
    :type content: str
    :param actions: a map of button labels to next steps.
    :type actions: { label: stepname, label2: stepname2, ...}
    :param initials: key value pairs of initial field values.
    :type initials: ``str=object``
    :returns: form dictionary
    :rtype: dict
    :raises Exception: on API create failure.
    """

    app =   {
                'wiid': wiid,
                'steps': actions,
                'type': 'workflow_approval',
                'org': org,
            }

    template = {
        'title': title,
        'content': content,
        'actions':  [{'label': a} for a in actions.keys()],
        'form_controls': form_controls,
    }

    for field in template['form_controls']:
        if field['name'] in initials:
            field['initial'] = initials[field['name']]

    return FormClient().create(template=template, app=app)

class FormClient():
    """The form client class is used to interact with the fleetingforms.io api.

    :param namespace_token: the unique token for the user namespace
    :type token: str (uuid4 format)

    The client supports standard ReSTful actions against the API.  To walk
    through the lifecycle of a form as seen from the api:

    .. code-block:: python

        # Instantiate a new client
        client = FormClient()

        # And define a minimalist form with two buttons.
        form_template = {
            'title': 'Approval Request for More Eggs',
            'content': 'Can we buy more eggs?',
            'form_controls': [],
            'actions': [{'label': 'Yes!'}, {'label': 'No.'}],
        }

        # Create the form using a POST request to the API.
        form = client.create(form_template)

        _id = form['id']
        # print an integer ID unique to the form
        print(form['id'])

        # print the unique URL for the form
        print(form['url'])

        # Retrieve the form to see if the form has been opened
        form = client.get(_id)

        # Check to see if the opened_on field has a datetime
        if form['opened_on']:
            print("The form was opened on {}".format(form['opened_on']))

        # Get a list of all the forms defined in the namespace:
        forms = client.list()
        for form in forms:
            print("Form {} at URL {}".format(form['_id'], form['url']))

        # Delete a form
        deleted = client.delete(_id)
    """

    API_ROOT = "http://fleetingforms.test"
    FORMS_ROOT = "forms"
    TRAILING_SLASH = True

    def __init__(self, namespace_token=None):
        self.namespace_token = namespace_token or self.token

    @property
    def headers(self):
        """Headers for authentication to a namespace.

        Make it easy to get namespace authentication headers for this client.

        :returns: authentication headers for use with requests.
        :rtype: dict
        """
        return { 'X-FLEETING-TOKEN': self.namespace_token }

    @property
    def token(self):
        """Get the token from the license options."""
        return "75fd76f2-ecc0-490b-ba50-6f41ac1e8b84"

    def url_for(self, action='create', _id=None):
        """Get the URL for an action type.

        Supported actions are ``create``, ``retrieve``, ``list``, ``delete``.

        :param action: the action the url is required form.
        :type action: str
        :param _id: the id of the form to retrieve or delete.
        :type _id: int
        :returns: url for the action and _id.
        :rtype: str
        :raises Exception: Unsupported action if action not supported.
        """
        if action in ['create', 'list']:
            url = "/".join([self.API_ROOT, self.FORMS_ROOT])
        elif action in ['get', 'delete']:
            url ="/".join([self.API_ROOT, self.FORMS_ROOT, str(_id)])
        else:
            raise Exception("Unsupported URL action: {}".format(action))

        if self.TRAILING_SLASH:
            url += "/"

        return url

    def create(self, template={}, auth={}, app={}):
        """Create a new form.

        :param template: the form template.
        :type template: dict
        :param auth: the form authentication parameters.
        :type auth: dict
        :param app: the form appentication parameters.
        :type app: dict
        :returns: form dictionary
        :rtype: dict
        :raises Exception: API failure.
        """

        payload = {
                'template': template,
                'auth': auth,
                'app': app,
            }

        try:
            resp = requests.post(self.url_for('create'),
                                 json=payload,
                                 headers=self.headers)
            if resp.status_code == 201:
                rj = resp.json()
            else:
                raise Exception("Failed to create. {}/{}".format(resp.status_code, resp.text))
        except Exception as e:
            raise Exception("Failed to create: {}".format(e))

        return rj

    def get(self, _id):
        """Retrieve a specific form from the service.

        :param _id: the ``id`` of the form to retrieve
        :type _id: int
        :returns: form dictionary
        :rtype: dict
        :raises Exception: API failure.
        """
        try:
            resp = requests.get(self.url_for('get', _id), headers=self.headers)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            pass

        return None

    def list(self):
        """List all the forms in this namespace.

        :returns: a list of form dictionaries
        :rtype: [{'id': 1, }, ...]
        :raises Exception: API failure.
        """
        try:
            resp = requests.get(self.url_for('list'), headers=self.headers)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            raise

        return []

    def delete(self, _id):
        """Delete a form from the service.

        :param _id: the ``id`` of the form to delete
        :type _id: int
        :returns: True if deleted, else False
        :rtype: bool
        :raises Exception: API failure.
        """
        try:
            resp = requests.delete(self.url_for('delete', _id),
                                   headers=self.headers)
            if resp.status_code == 204:
                return True
            else:
                raise Exception("Failed to delete: {}".format(resp.text))
        except Exception as e:
            raise Exception("Failed to delete: {}".format(e))

        return False
