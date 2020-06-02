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


with description("Backup restore alerts and notification channels") as self:
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
        self.channel_name = "[sdc-cli-test] random-chan-{}".format(_rand_text())
        self.alert_name = "[sdc-cli-test] random-alert-{}".format(_rand_text())

        self.cleanup_alerts()
        self.cleanup_notification_channels()

        ok, _ = self.create_test_alert_with_notification_channel(self.alert_name, self.channel_name)
        expect(ok).to(be_true)

        DumpNotificationChannelsUseCase(self.monitor, self.repository).execute()
        DumpAlertsUseCase(self.monitor, self.repository).execute()

        self.cleanup_alerts()
        self.cleanup_notification_channels()

    with after.each:
        self.cleanup_alerts()
        self.cleanup_notification_channels()

    with context('when someone removes and restores notification channels'):
        with it('restores correctly the alert'):
            ok_nc, _ = RemoveAndRestoreNotificationChannelsUseCase(self.monitor, self.repository).execute()
            ok_al, res = RemoveAndRestoreAlertsUseCase(self.monitor, self.repository).execute()

            _, alerts = self.monitor.get_alerts()
            _, ncs = self.monitor.list_notification_channels()
            restored_alert = [alert for alert in alerts['alerts'] if alert['name'] == self.alert_name][0]
            restored_nc = [nc for nc in ncs['notificationChannels'] if nc['name'] == self.channel_name][0]

            expect(ok_nc).to(be_true)
            expect(ok_al).to(be_true)
            expect(restored_alert['notificationChannelIds']).to(contain_exactly(restored_nc['id']))

    with context('when someone removes the notification channel and does not restore it'):
        with it('restores correctly the alert'):
            ok, res = RemoveAndRestoreAlertsUseCase(self.monitor, self.repository).execute()

            _, alerts = self.monitor.get_alerts()
            _, ncs = self.monitor.list_notification_channels()
            restored_alert = [alert for alert in alerts['alerts'] if alert['name'] == self.alert_name][0]

            expect(ok).to(be_true)
            expect(restored_alert).to_not(have_key('notificationChannelIds'))


    def cleanup_alerts(self):
        ok, res = self.monitor.get_alerts()
        expect(ok).to(be_true)

        for alert in res['alerts']:
            if alert['name'].startswith('[sdc-cli-test]'):
                ok, res = self.monitor.delete_alert(alert)
                expect(ok).to(be_true)


    def cleanup_notification_channels(self):
        ok, res = self.monitor.list_notification_channels()
        expect(ok).to(be_true)

        for nc in res['notificationChannels']:
            if nc['name'].startswith('[sdc-cli-test]'):
                ok, res = self.monitor.delete_notification_channel(nc)
                expect(ok).to(be_true)


    def create_test_alert_with_notification_channel(self, alert_name, channel_name):
        ok, channel = self.monitor.create_email_notification_channel(channel_name,
                                                                     ["random-email-{}@localhost".format(_rand_text())])
        if not ok:
            return False, channel

        return self.monitor.create_alert(name=alert_name,
                                         description="Alert Description",
                                         severity=4,
                                         for_atleast_s=60,
                                         notify=[channel["notificationChannel"]["id"]],
                                         condition="avg(avg(cpu.used.percent)) > 50")
