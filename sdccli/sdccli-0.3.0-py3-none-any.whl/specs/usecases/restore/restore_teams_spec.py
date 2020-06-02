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


with description("Backup restore monitor teams") as self:
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

        self.cleanup_monitor_teams()

        self.monitor_team_name = "[sdc-cli-test] random-team-{}".format(_rand_text())
        ok, created_dashboard = self.monitor.create_team(self.monitor_team_name)

        expect(ok).to(be_true)
        DumpTeamsMonitorUseCase(self.monitor, self.repository).execute()

        self.cleanup_monitor_teams()

    with after.each:
        self.cleanup_monitor_teams()


    def cleanup_monitor_teams(self):
        ok, res = self.monitor.get_teams()
        expect(ok).to(be_true)

        for team in res:
            if team['name'].startswith('[sdc-cli-test]'):
                ok, res = self.monitor.delete_team(team['name'])
                expect(ok).to(be_true)


    with context('when a monitor team in the backup does not exist in the product'):
        with it('restores the monitor team'):
            _, teams_before = self.monitor.get_teams()
            ok_restore, res_restore = RestoreTeamsMonitorUseCase(self.monitor, self.repository).execute()
            _, teams_after = self.monitor.get_teams()

            expect(ok_restore).to(be_true)
            expect(len(teams_before) + 1).to(equal(len(teams_after)))

        with it('ignores the already restored team'):
            RestoreTeamsMonitorUseCase(self.monitor, self.repository).execute()

            _, teams_before = self.monitor.get_teams()
            ok_restore, res_restore = RestoreTeamsMonitorUseCase(self.monitor, self.repository).execute()
            _, teams_after = self.monitor.get_teams()

            expect(ok_restore).to(be_true)
            expect(len(teams_before)).to(equal(len(teams_after)))

    with context('when someone creates a team and removes one that is in the backup'):
        with before.each:
            self.monitor.create_team(f"[sdc-cli-test] random-unwanted-team-{_rand_text()}")

        # with before.each:
        #     _, dashboard = get_dashboard_by_name(self.monitor, self.dashboard_name)
        #     self.monitor.delete_dashboard(dashboard)

        with it('creates again the removed team without removing the unwanted'):
            _, teams_before = self.monitor.get_teams()
            ok_restore, res_restore = RestoreTeamsMonitorUseCase(self.monitor,
                                                                 self.repository).execute()
            _, teams_after = self.monitor.get_teams()

            expect(ok_restore).to(be_true)
            expect(len(teams_before) + 1).to(equal(len(teams_after)))
            expect(teams_before).to_not(contain(have_keys({'name': self.monitor_team_name})))
            expect(teams_before).to(contain(have_keys({'name': start_with("[sdc-cli-test] random-unwanted-team-")})))
            expect(teams_after).to(contain(have_keys({'name': self.monitor_team_name})))
            expect(teams_after).to(contain(have_keys({'name': start_with("[sdc-cli-test] random-unwanted-team-")})))

        with it('removes the unwanted team and creates the backed up one'):
            _, teams_before = self.monitor.get_teams()
            ok_restore, res_restore = RemoveAndRestoreTeamsMonitorUseCase(self.monitor,
                                                                          self.repository).execute()
            _, teams_after = self.monitor.get_teams()

            expect(ok_restore).to(be_true)
            expect(len(teams_before)).to(equal(len(teams_after)))
            expect(teams_before).to_not(contain(have_keys({'name': self.monitor_team_name})))
            expect(teams_before).to(contain(have_keys({'name': start_with("[sdc-cli-test] random-unwanted-team-")})))
            expect(teams_after).to(contain(have_keys({'name': self.monitor_team_name})))
            expect(teams_after).to_not(contain(have_keys({'name': start_with("[sdc-cli-test] random-unwanted-team-")})))
