"""Models for integrating BigBLueButton API with Django.

These models are intended for persisting data that is needed for setting up
access to any BigBlueButton servers, and for (re-)creating meetings on these
servers. Normally, all other data, i.e. that represents live state, is fetched
from the API directly and not persisted.
"""

import uuid

from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..api.bigbluebutton import BigBlueButton as _BigBlueButton
from ..api.bigbluebutton import BigBlueButtonGroup as _BigBlueButtonGroup
from ..api.meeting import Meeting as _Meeting
from . import settings


class BigBlueButton(models.Model):
    """Configuration for one BigBlueButton server.

    See the documentation of the :class:`~bigbluebutton.api.bigbluebutton.BigBlueButton`
    in the main API module for most details.
    """

    name = models.CharField(verbose_name=_("Server name"), max_length=60)
    url = models.URLField(verbose_name=_("API base URL"))
    salt = models.CharField(verbose_name=_("API shared secret"), max_length=60)

    group = models.ForeignKey("BigBlueButtonGroup", on_delete=models.CASCADE, related_name="apis")

    _api = None

    def __str__(self) -> str:
        return self.name

    @property
    def api(self) -> _BigBlueButton:
        """The real :class:`~bigbluebutton.api.bigbluebutton.BigBlueButton` API object.

        Use this object to operate on any live data. It is created on the first request and
        then cached.
        """
        if self._api is None:
            self._api = _BigBlueButton(self.group.api_group, self.name, self.url, self.salt)

        return self._api


class BigBlueButtonGroup(models.Model):
    """Configuration for a group of BigBlueButton servers.

    See the documentation of the :class:`~bigbluebutton.api.bigbluebutton.BigBlueButtonGroup`
    in the main API module for most details.
    """

    name = models.CharField(verbose_name=_("Group name"), max_length=60)

    site = models.ForeignKey(Site, on_delete=models.CASCADE, default=Site.objects.get_current)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    _api_group = None

    def __str__(self) -> str:
        return self.name

    @property
    def api_group(self) -> _BigBlueButtonGroup:
        """The real :class:`~bigbluebutton.api.bigbluebutton.BigBlueButtonGroup` API object.

        Use this object to operate on any live data. It is created on the first request and
        then cached.
        """
        if self._api_group is None:
            self._api_group = _BigBlueButtonGroup(
                self.name, origin=self.site.name, origin_server_name=self.site.domain
            )

            for api in self.apis.all():
                api.api

        return self._api_group


class Meeting(models.Model):
    """Configuation for a BigBlueButton meeting.

    See the documentation of the :class:`~bigbluebutton.api.meeting.Meeting`
    in the main API module for most details.
    """

    name = models.CharField(verbose_name=_("Meeting name"), max_length=60)

    welcome_message = models.TextField(verbose_name=_("Welcome message"), blank=True)
    moderator_message = models.TextField(
        verbose_name=_("Welcome message for moderators"), blank=True
    )

    max_participants = models.PositiveSmallIntegerField(
        verbose_name=_("Maximum number of participants"), default=0
    )

    api = models.ForeignKey("BigBlueButton", on_delete=models.CASCADE, related_name="meetings")

    guid = models.UUIDField(default=uuid.uuid1, editable=False)

    _meeting = None

    def __str__(self) -> str:
        return self.name

    @classmethod
    def from_api(cls, api: _BigBlueButton, meeting: _Meeting) -> "Meeting":
        """Create a persistent meeting object from the live API.

        This can be used to retroactively persist a
        :class:`~bigbluebutton.api.meeting.Meeting` object object that was not created
        by the Django application.
        """
        obj, created = cls.update_or_create(
            name=meeting.meeting_name,
            api=api,
            defaults={
                "welcome_message": meeting.welcome,
                "moderator_message": meeting.moderator_only_message,
                "max_participants": meeting.max_participants,
            },
        )
        obj.save()

        obj._meeting = meeting

        return obj

    @property
    def meeting(self) -> _Meeting:
        """The real :class:`~bigbluebutton.api.meeting.Meeting` API object.

        Use this object to operate on any live data. It is created on the first request and
        then cached.
        """
        if self._meeting is None:
            self._meeting = self.api.api.create_meeting(
                do_create=False,
                meeting_id=self.meeting_id,
                meeting_name=self.name,
                welcome=self.welcome_message,
                moderator_only_message=self.moderator_message,
                max_participants=self.max_participants,
            )
        return self._meeting

    @property
    def meeting_id(self) -> str:
        """Internal meeting ID as used by BigBlueButton.

        If a :class:`~bigbluebutton.api.meeting.Meeting` object is already linked and
        has an ID, it is returned. If not, a new ID is generated and stored in the
        linked Meeting object, if any. This means that the ID is stable once it was
        transported to the API.
        """
        if self._meeting and self._meeting.meeting_id:
            return self._meeting.meeting_id
        else:
            meeting_id = settings.MEETING_ID_CALLBACK(self)
            if self._meeting:
                self._meeting.meeting_id = meeting_id
            return meeting_id

    def join(self, user: "User", do_join: bool = False) -> str:
        """Join a Django user to this meeting.

        Generate an :class:`~bigbluebutton.api.attendee.Attendee` object from a Django
        user and asks the API to join it to the meeting. To generate the Attendee object,
        the function defined in the `BBB_ATTENDEE_CALLBACK` setting is called, defaulting to
         :func:`~bigbluebutton.django.util.get_attendee`.

        :param user: The Django user object of the user to join as attendee
        :param do_join: Handle the join request server-side. Defaults to False, so the
                        client browser can request the actual join

        :return: The result of the :meth:`~bigbluebutton.api.attendee.Attendee.join` method
                 from the main API
        """
        attendee = user.bbb_get_attendee(self)
        return attendee.join(do_join=do_join)


class APIToken(models.Model):
    """An API token when using the proxy capabilities of bigbluebutton2.

    This is used to authenticate and authorise requests in the
    :class:`~bigbluebutton.django.views.APIView` that can be used to handle
    HTTP requests to the Django application that resemble the original BigBlueButton API,
    e.g. when creating a proxy or load balancer, and when these requests shall be linked
    to permissions in Django.

    :param name: Human-readable display name for the token
    :param salt: The API salt/secret key for this token; see
                 :meth:`~bigbluebutton.api.bigbluebutton.BigBlueButton.request_checksum`
                 for details
    :param server_group: The server group to forward requests to after successful authorisation
    :param user: The Django user linked to this token, if the user scope is used
    :param scope: The scope of this token, used to determine what data is returned in requests
                  that handle existing meeting data
    """

    SCOPE_CHOICES = (
        ("token", _("Data associated to this token")),
        ("user", _("Data associated to the owning user")),
        ("global", _("All data")),
    )

    name = models.CharField(verbose_name=_("Descriptive name"), max_length=60, unique=True)
    salt = models.CharField(verbose_name=_("API salt"), max_length=60, unique=True)

    server_group = models.ForeignKey(BigBlueButtonGroup, on_delete=models.CASCADE)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User owning this token"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    scope = models.CharField(
        verbose_name=_("Privilege scope"), choices=SCOPE_CHOICES, max_length=15, default="token"
    )

    guid = models.UUIDField(default=uuid.uuid1, editable=False)

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        """Ensure a user is linked when the user scope is selected."""
        if self.scope == "user" and not self.user:
            raise ValidationError(_("A user must be selected to use the user scope."))
