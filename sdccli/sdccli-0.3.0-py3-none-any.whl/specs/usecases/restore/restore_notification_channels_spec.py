import os
import random
import string

from expects import *
from mamba import *

from sdccli.usecases.backup.dump import *
from sdccli.usecases.backup.restore import *


class _InMemoryRepository(object):
    def __init__(self):
        self.data = ""

    def write(self, data):
        self.data += data

    def read(self):
        return self.data


def _rand_text():
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=10))


with description("Backup restore notification channels") as self:
    with before.each:
        self.repository = _InMemoryRepository()
        self.monitor = SdMonitorClient(
            token=os.environ["SDC_MONITOR_TOKEN"],
            sdc_url="https://app.sysdigcloud.com",
            ssl_verify=True,
        )
        self.secure = SdSecureClient(
            token=os.environ["SDC_SECURE_TOKEN"],
            sdc_url="https://secure.sysdig.com",
            ssl_verify=True,
        )

        self.cleanup_notification_channels()

        self.channel_name = "[sdc-cli-test] random-chan-{}".format(_rand_text())
        _, channel = self.monitor.create_email_notification_channel(
            self.channel_name, ["random-email-{}@localhost".format(_rand_text())])

        DumpNotificationChannelsUseCase(self.monitor, self.repository).execute()

        self.cleanup_notification_channels()

    with after.each:
        self.cleanup_notification_channels()


    def cleanup_notification_channels(self):
        ok, res = self.monitor.list_notification_channels()
        expect(ok).to(be_true)

        for nc in res['notificationChannels']:
            if nc['name'].startswith('[sdc-cli-test]'):
                ok, res = self.monitor.delete_notification_channel(nc)
                expect(ok).to(be_true)


    with context('when there is a missing notification channel'):
        with it("restores notification channels"):
            _, nc_before = self.monitor.list_notification_channels()
            ok_restore, res_restore = RestoreNotificationChannelsUseCase(self.monitor,
                                                                         self.repository).execute()
            _, nc_after = self.monitor.list_notification_channels()

            expect(ok_restore).to(be_true)
            expect(len(nc_before['notificationChannels']) + 1).to(equal(len(nc_after['notificationChannels'])))

        with it("ignores the already created notification channel"):
            ok_restore, res_restore = RestoreNotificationChannelsUseCase(self.monitor,
                                                                         self.repository).execute()
            _, nc_after = self.monitor.list_notification_channels()
            _, nc_before = self.monitor.list_notification_channels()
            ok_restore, res_restore = RestoreNotificationChannelsUseCase(self.monitor,
                                                                         self.repository).execute()
            _, nc_after = self.monitor.list_notification_channels()

            expect(ok_restore).to(be_true)
            expect(len(nc_before['notificationChannels'])).to(equal(len(nc_after['notificationChannels'])))

    with context('when someone creates an unwanted notification channel and there is a missing one'):
        with before.each:
            self.monitor.create_email_notification_channel(
                "[sdc-cli-test] random-unwanted-chan-{}".format(_rand_text()),
                ["random-email-{}@localhost".format(_rand_text())])

        with it('restores the removed notification channel without removing the ones not in the backup'):
            _, nc_before = self.monitor.list_notification_channels()

            ok_restore, res_restore = RestoreNotificationChannelsUseCase(self.monitor,
                                                                         self.repository).execute()
            _, nc_after = self.monitor.list_notification_channels()

            expect(ok_restore).to(be_true)
            expect(len(nc_before['notificationChannels']) + 1).to(equal(len(nc_after['notificationChannels'])))

        with it("restores the removed one and removes the notification channels not existing in the backup"):
            _, nc_before = self.monitor.list_notification_channels()

            ok_restore, res_restore = RemoveAndRestoreNotificationChannelsUseCase(self.monitor,
                                                                                  self.repository).execute()
            _, nc_after = self.monitor.list_notification_channels()

            expect(ok_restore).to(be_true)
            expect(len(nc_before['notificationChannels'])).to(equal(len(nc_after['notificationChannels'])))
