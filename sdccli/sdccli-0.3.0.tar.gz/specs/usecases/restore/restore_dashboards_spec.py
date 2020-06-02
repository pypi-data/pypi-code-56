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


with description("Backup restore dashboards") as self:
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

        self.cleanup_dashboards()

        self.dashboard_name = "[sdc-cli-test] random-dashboard-{}".format(_rand_text())
        ok, created_dashboard = self.monitor.create_dashboard(self.dashboard_name)
        DumpDashboardsUseCase(self.monitor, self.repository).execute()

        self.cleanup_dashboards()

    with after.each:
        self.cleanup_dashboards()


    def cleanup_dashboards(self):
        ok, res = self.monitor.get_dashboards()
        expect(ok).to(be_true)

        for dashboard in res['dashboards']:
            if dashboard['name'].startswith('[sdc-cli-test]'):
                ok, res = self.monitor.delete_dashboard(dashboard)
                expect(ok).to(be_true)


    with context('when a dashboard in the backup does not exist in the product'):
        with it('restores the dashboard'):
            _, db_before = self.monitor.get_dashboards()
            ok_restore, res_restore = RestoreOwnedDashboardsUseCase(self.monitor,
                                                                    self.repository).execute()
            _, db_after = self.monitor.get_dashboards()

            expect(ok_restore).to(be_true)
            expect(len(db_before['dashboards']) + 1).to(equal(len(db_after['dashboards'])))

        with it('ignores the already restored dashboard'):
            ok_restore, res_restore = RestoreOwnedDashboardsUseCase(self.monitor,
                                                                    self.repository).execute()
            _, db_before = self.monitor.get_dashboards()
            ok_restore, res_restore = RestoreOwnedDashboardsUseCase(self.monitor,
                                                                    self.repository).execute()
            _, db_after = self.monitor.get_dashboards()

            expect(ok_restore).to(be_true)
            expect(len(db_before['dashboards'])).to(equal(len(db_after['dashboards'])))

    with context('when someone creates a dashboard and removes one that is in the backup'):
        with before.each:
            self.monitor.create_dashboard("[sdc-cli-test] random-unwanted-dashboard-{}".format(_rand_text()))

        # with before.each:
        #     _, dashboard = get_dashboard_by_name(self.monitor, self.dashboard_name)
        #     self.monitor.delete_dashboard(dashboard)

        with it('creates again the removed dashboard without removing the unwanted'):
            _, db_before = self.monitor.get_dashboards()
            ok_restore, res_restore = RestoreOwnedDashboardsUseCase(self.monitor,
                                                                    self.repository).execute()
            _, db_after = self.monitor.get_dashboards()

            expect(ok_restore).to(be_true)
            expect(len(db_before['dashboards']) + 1).to(equal(len(db_after['dashboards'])))

        with it('removes the unwanted dashboard and creates the backed up one'):
            _, db_before = self.monitor.get_dashboards()
            ok_restore, res_restore = RemoveOwnedAndRestoreOwnedDashboardsUseCase(self.monitor,
                                                                                  self.repository).execute()
            _, db_after = self.monitor.get_dashboards()

            expect(ok_restore).to(be_true)
            expect(len(db_before['dashboards'])).to(equal(len(db_after['dashboards'])))
