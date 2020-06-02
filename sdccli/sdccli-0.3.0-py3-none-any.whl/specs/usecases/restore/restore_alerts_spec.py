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


with description("Backup restore alerts") as self:
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

        self.cleanup_alerts()

        self.alert_name = "[sdc-cli-test] random-alert-{}".format(_rand_text())
        ok, res = self.create_test_alert(self.alert_name)
        expect(ok).to(be_true)
        DumpAlertsUseCase(self.monitor, self.repository).execute()

        self.cleanup_alerts()

    with after.each:
        self.cleanup_alerts()


    def create_test_alert(self, alert_name):
        return self.monitor.create_alert(name=alert_name,
                                         description="Alert Description",
                                         severity=4,
                                         for_atleast_s=60,
                                         condition="avg(avg(cpu.used.percent)) > 50")


    def cleanup_alerts(self):
        ok, res = self.monitor.get_alerts()
        expect(ok).to(be_true)

        for alert in res['alerts']:
            if alert['name'].startswith('[sdc-cli-test]'):
                ok, res = self.monitor.delete_alert(alert)
                expect(ok).to(be_true)


    with context('when an alert in the backup does not exist in the product'):
        with it('restores the alert'):
            _, alerts_before = self.monitor.get_alerts()
            ok_restore, res_restore = RestoreAlertsUseCase(self.monitor, self.repository).execute()
            _, alerts_after = self.monitor.get_alerts()

            expect(ok_restore).to(be_true)
            expect(len(alerts_before['alerts']) + 1).to(equal(len(alerts_after['alerts'])))
            expect(alerts_before['alerts']).to_not(contain(have_keys({'name': self.alert_name})))
            expect(alerts_after['alerts']).to(contain(have_keys({'name': self.alert_name})))

        with it('ignores the already restored alert'):
            RestoreAlertsUseCase(self.monitor, self.repository).execute()

            _, alerts_before = self.monitor.get_alerts()
            ok_restore, res_restore = RestoreAlertsUseCase(self.monitor, self.repository).execute()
            _, alerts_after = self.monitor.get_alerts()

            expect(ok_restore).to(be_true)
            expect(len(alerts_before['alerts'])).to(equal(len(alerts_after['alerts'])))
            expect(alerts_before['alerts']).to(contain(have_keys({'name': self.alert_name})))
            expect(alerts_after['alerts']).to(contain(have_keys({'name': self.alert_name})))

    with context('when someone creates an alert and removes one that is in the backup'):
        with before.each:
            self.create_test_alert(f"[sdc-cli-test] random-unwanted-alert-{_rand_text()}")

        with it('creates again the removed alert without removing the unwanted'):
            _, alerts_before = self.monitor.get_alerts()
            ok_restore, res_restore = RestoreAlertsUseCase(self.monitor, self.repository).execute()
            _, alerts_after = self.monitor.get_alerts()

            expect(ok_restore).to(be_true)
            expect(len(alerts_before['alerts']) + 1).to(equal(len(alerts_after['alerts'])))
            expect(alerts_before['alerts']).to(
                contain(have_keys({'name': start_with("[sdc-cli-test] random-unwanted-alert-")})))
            expect(alerts_before['alerts']).to_not(contain(have_keys({'name': self.alert_name})))
            expect(alerts_after['alerts']).to(
                contain(have_keys({'name': start_with("[sdc-cli-test] random-unwanted-alert-")})))
            expect(alerts_after['alerts']).to(contain(have_keys({'name': self.alert_name})))

        with it('removes the unwanted dashboard and creates the backed up one'):
            _, alerts_before = self.monitor.get_alerts()
            ok_restore, res_restore = RemoveAndRestoreAlertsUseCase(self.monitor, self.repository).execute()
            _, alerts_after = self.monitor.get_alerts()

            expect(ok_restore).to(be_true)
            expect(len(alerts_before['alerts'])).to(equal(len(alerts_after['alerts'])))
            expect(alerts_before['alerts']).to(
                contain(have_keys({'name': start_with("[sdc-cli-test] random-unwanted-alert-")})))
            expect(alerts_before['alerts']).to_not(contain(have_keys({'name': self.alert_name})))
            expect(alerts_after['alerts']).to_not(
                contain(have_keys({'name': start_with("[sdc-cli-test] random-unwanted-alert-")})))
            expect(alerts_after['alerts']).to(contain(have_keys({'name': self.alert_name})))
