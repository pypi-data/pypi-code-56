"""
The poller component of the PPFORMS module connects to fleetingforms.io using
a Sage instance's unique token and downloads any forms that have been
completed or are in error.

On every execution, the poller takes the following steps::

    for each form in the polling results:
        if the form is completed and workflow related:
            progress the workflow based on the user action
        if the form is in error:
            log the error

    delete all processed forms
    log a summary of the actions taken

The poller can be executed from the Scripts panel or run using
:ref:`Process Scheduler <running-the-poller-with-process-scheduler>`.

The poller logs to
``Sage300/SharedData/Company/<ComanyName>/ppforms.poll.log``
"""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

try:
    from accpac import *
    from form_client import FormClient
except ImportError:
    pass


# Forms in these statuses need to be handled.
FORM_COMPLETED_STATUSES = { 'completed', 'error', }

# Execution contexts: run through the scripts panel (VI) or scheduler (PS)
VI = 0
PS = 1

# Error counter for PS
pserr = 0

# The logger must be setup in the main method, config here fails.
logger = None

def execution_context():
    """Enable running from PS or Scrips panel.

    If run through PS this will return PS, otherwise VI.
    """
    if program.startswith("AS1"):
        return PS
    return VI

def _alert(message):
    """Show an alert to the user.

    When running in VI, the alert is shown in a message box.
    """
    if execution_context() == VI:
        showMessageBox("Remote Approvals\n\n{}".format(message))
    logger.info(message)

def _error(message):
    """Register an error in the process.

    When running in VI, the error is shown in a message box.
    """
    if execution_context() == VI:
        showMessageBox("Remote Approvals - Error\n\n{}".format(message))
    logger.exception(message)

def main(*args, **kwargs):
    """Entry point for execution - perform a poll."""

    # Configure a logger to write to the log file.
    global logger
    log_path = Path(getOrgPath(), "ppforms.poll.log")
    logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S',
            handlers=[RotatingFileHandler(
                filename=str(log_path),
                backupCount=5,
                maxBytes=10*1024*1024), ],
        )
    logger = logging.getLogger('PPFORMS.poll')
    logger.debug("main: org {}, user {}, program {}".format(
            org, user, program))

    # Create a new poller for this organization and poll.
    try:
        poller = FleetingFormPoller(org)
        successes, errors = poller.poll()
        summary = """
        Polling complete.

        {} approvals applied successfully
        {} errors encountered.

        See the details in the PS Log.
        """.format(len(successes), len(errors))
        _alert(summary)
    except PollerError as e:
        _error("Error in poller: {}".format(e))
    except Exception as e:
        _error("General failure in poller: {}".format(e))

    if execution_context() == PS:
        # When running through PS, log a completion message.
        log_message = "{}|{}|{}".format(
                "ERR" if errors else "OK",
                len(errors),
                log_path)
        log(log_message)

    if execution_context() == VI:
        # When running through the scripts panel, close the empty UI.
        UI().closeUI()

# Poller class and errors
class PollerError(Exception):
    """Base Exception class for all errors raised by the poller."""
    pass

class PollerStartupError(PollerError):
    """Poller failed to start."""
    pass

class PollerAPIError(PollerError):
    """Poller had an API communication failure."""
    pass

class PollerValidationError(PollerError):
    """Poller failed to validate a completed form."""
    pass

class PollerDeleteError(PollerAPIError):
    """Poller failed to delete a form over the API."""
    pass

class PollerWorkflowSaveError(PollerError):
    """Poller failed to save a workflow."""
    pass

class PollerFormInError(PollerError):
    """Poller encountered a form in an error state."""
    pass

class FormHandler(object):
    """Abstract parent for all form handlers.

    To handle a new type of form, define a new handler and register
    it in the FleetingFormPoller.FORM_HANDLERS dict.

    Form handlers are automatically dispatched based on the form.app.type
    value.
    """
    type = None

    def __init__(self, form):
        if not self.type:
            raise NotImplementedError("Handlers must have a type.")
        self.form = form

    def validate(self):
        raise NotImplementedError(
                "Validate must be implemented in a subclass.")

    def apply(self):
        raise NotImplementedError(
                "Apply must be implemented in a subclass.")

class WorkflowApprovalFormHandler(FormHandler):
    """Handle a workflow approval form.

    This handler validates that a workflow approval form has
    all the required fields and progresses to the next step based
    on the user action.

    :param form: the form to handle.
    :type form: dict
    """

    type = 'workflow_approval'

    def __init__(self, form):
        super(WorkflowApprovalFormHandler, self).__init__(form)
        self.wiid = None
        self.stepname = None
        self._validated = False

    def validate(self):
        """Validate a completed workflow approval self.form.

        Sets:
          - self.stepname: next workflow step
          - self.wiid: workflow instance id
          - self.app: app parameters for this form

        :returns: validated form
        :rtype: dict
        :raises: PollerValidationError
        """

        self.app = self.form.get('app', {})
        self.wiid = self.app.get('wiid')

        # forms must have a valid workflow instance id
        if not self.wiid:
            raise PollerValidationError(
                    "self.form {} has no workflow ID set.".self.format(
                        self.form.get('code', 'unset')))

        # and a mapping of form actions to steps.
        self.steps = self.app.get('steps', {})
        if not self.steps:
            raise PollerValidationError(
                    "self.form {} has no steps set.".self.format(
                        self.form.get('code', 'unset')))

        # an action must have been performed and recorded (i.e. Approve)
        self.result_action = self.form.get('result', {}).pop('action', None)
        if not self.result_action:
            raise PollerValidationError(
                    "No action for self.form {}".self.format(
                        self.form.get('code', 'unset')))

        # there must be a step to progress to for that action.
        self.stepname = self.steps.get(self.result_action)
        if not self.stepname:
            raise PollerValidationError(
                    "self.form {} has no stepname for {}.".self.format(
                            self.form.get('code', 'unset'),
                            self.result_action))

        # all is well.
        self._validated = True
        return self.form

    def apply(self):
        """Apply a workflow validation form.

        Applies a workflow validation form by setting the result
        values in the workflow instance values and progressing the
        workflow to the next step.

        :returns: None
        :raises: PollerError
        """
        if not self._validated:
            raise PollerValidationError(".validate() must be called on the "
                                        "form before .apply().")
        # Validate sets self.app, self.wiid, self.stepname
        wi = WorkflowInstance()
        _r = wi.loadInstance(self.wiid)

        # Copy all keys from the result into the workflow values.
        result = self.form.get('result', {})
        for (key, value) in result.items():
            wi.setValue(key, value)

        # If the RUNUSER result key is set, use it to change the
        # user executing the action.
        runuser = result.get("RUNUSER", user)
        wi.viworkih.put("RUNUSER", runuser)
        wi.viworkih.update()

        # Progress the workflow to the next step.
        logger.info('[{}] - progressing {} to {} as {}.'.format(
                self.form['code'], self.wiid, self.stepname, runuser))
        r = wi.progressTo(self.stepname)
        if wi.save() != 0:
            raise PollerWorkflowSaveError(
                    "Failed to progress {} to {} for form {}".format(
                             self.wiid, self.stepname,
                             self.form.get('code', 'unset')))


class FleetingFormPoller():
    """The fleeting form poller retrieves completed forms and applies them.

    :param org_: the sage company to poll for.
    :type org_: str
    :param clean: delete forms after applying their actions?
    :type clean: bool
    """

    FORM_HANDLERS = [
                WorkflowApprovalFormHandler,
            ]

    def __init__(self, org_, clean=True):
        self.errors = []
        self.successes = []
        self.org = org_
        self.clean = clean
        self.__form_list = []
        self._handlers = {}

        for handler_class in self.FORM_HANDLERS:
            self._handlers[handler_class.type] = handler_class

        try:
            self.client = FormClient()
        except Exception as e:
            raise PollerStartupError("Failed to start client: {}".format(e))

        logger.info("poller started for org {} with clean {}".format(
                org_, clean))

    def _flush_error_stack_to_log(self):
        """Flush the error stack to the log to debug errors in Sage."""
        errors = ErrorStack()
        logger.debug("flushing {} messages from error stack.".format(errors.count()))
        for i in range(0, errors.count()):
            func = logger.debug
            priority = errors.getPriority(i)
            if priority == PRI_MESSAGE:
                func = logger.info
            elif priority == PRI_WARNING:
                func = logger.warn
            elif priority == PRI_MESSAGE:
                func = logger.error
            func(errors.getText(i))
        errors.clear()

    @property
    def form_list(self):
        """A list of all forms in this namespace from cache or API."""
        if not self.__form_list:
            try:
                self.__form_list = self.client.list()
            except Exception as e:
                raise PollerAPIError("Failed to list forms: {}".format(e))
        return self.__form_list

    def form_list_filtered_by(self, form_filter={}, app_filter={}):
        """Yields forms from form_list matching form and app attrs.

        :param form_filter: the form attributes to filter for.
        :type form_filter: dict
        :param app_filer: the app attributes to filter for.
        :type app_filter: dict
        :yields: dict()
        """
        for form in self.form_list:
            if form_filter.items() <= form.items():
                if app_filter.items() <= form.get('app', {}).items():
                    yield(form)

    def poll(self):
        """Poll fleetingforms and process completed actions.

        :returns: a list of forms successfully processed and a list of forms
                  that encountered errors.
        :rtype: (list, list)
        """
        app_filter = {'org': self.org}

        # Filter our complete forms for this org.
        for form in self.form_list_filtered_by({'status': 'completed'},
                                               app_filter):
            try:
                # Get a handler for this form type.
                handler_class = self._handlers[form['app']['type']]

                # Create a new instance, validate and apply the action
                handler = handler_class(form)
                handler.validate()
                handler.apply()

                # Track stats and log/notify
                self.successes.append((form, True, ))
                _alert("[{}] - successfully applied.".format(form['code']))
            except Exception as e:
                # Log the error and track the form in errors.
                self.errors.append((form, e, ))
                _error("[{}] - error while applying: {}".format(
                        form['code'], e))
                # Flush Sage errors to the log for debugging
                self._flush_error_stack_to_log()

        # Find all forms in error for this org and log.
        # Deletion of the form deferred until cleanup.
        for form in self.form_list_filtered_by({'status': 'error'},
                                               app_filter):
            if app_filter.items() <= form['app'].items():
                raise PollerFormInError(
                        "Form {} is in an error state.".format(
                            form.get('code', 'unset')))

        # After processing completed forms and those in error,
        # clean up all processed forms from the service.
        if self.clean:
            self.cleanup()

        return (self.successes, self.errors)

    def cleanup(self):
        """Delete all successfully processed forms from the service.

        :returns: None
        """
        processed = self.successes + self.errors
        logger.debug('cleaning up {} forms.'.format(len(processed)))
        for (form, status) in processed:
            try:
                self.client.delete(form['id'])
                logger.info("[{}] - deleted form {}.".format(
                        form['code'], form['id']))
            except Exception as e:
                self.errors.append((form,
                        PollerDeleteError(
                        "Failed to delete the entry {}: {}".format(
                                form.get('code', 'unset'), e)),
                        ))

        # Clear the cache of forms for this org.
        self.__form_list.clear()
