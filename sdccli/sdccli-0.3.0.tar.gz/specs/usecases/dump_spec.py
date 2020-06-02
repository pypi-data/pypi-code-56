from expects import *
from mamba import *
from sdcclient import SdMonitorClient, SdSecureClient
import os

from sdccli.usecases.backup.dump import *


class _InMemoryRepository(object):
    def __init__(self):
        self.data = ""

    def write(self, data):
        self.data += data

    def read(self):
        return self.data


with description(sdccli.usecases.backup.dump) as self:
    with before.all:
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

    with context("with an in-memory repository"):
        with before.each:
            self.repository = _InMemoryRepository()

        with it("dumps users to the repository"):
            ok, res = DumpUsersUseCase(self.monitor, self.repository).execute()
            data = self.repository.read()

            expect(ok).to(be_true)
            expect(data).to_not(be_empty)

        with it("dumps dashboards to the repository"):
            ok, res = DumpDashboardsUseCase(self.monitor, self.repository).execute()
            data = self.repository.read()

            expect(ok).to(be_true)
            expect(data).to_not(be_empty)

        with it("dumps alerts to the repository"):
            ok, res = DumpAlertsUseCase(self.monitor, self.repository).execute()
            data = self.repository.read()

            expect(ok).to(be_true)
            expect(data).to_not(be_empty)

        with it("dumps monitor teams to the repository"):
            ok, res = DumpTeamsMonitorUseCase(self.monitor, self.repository).execute()
            data = self.repository.read()

            expect(ok).to(be_true)
            expect(data).to_not(be_empty)

        with it("dumps notification channels to the repository"):
            ok, res = DumpNotificationChannelsUseCase(self.monitor, self.repository).execute()
            data = self.repository.read()

            expect(ok).to(be_true)
            expect(data).to_not(be_empty)

        with it("dumps secure teams to the repository"):
            ok, res = DumpTeamsSecureUseCase(self.secure, self.repository).execute()
            data = self.repository.read()

            expect(ok).to(be_true)
            expect(data).to_not(be_empty)

        with it("dumps policies to the repository"):
            ok, res = DumpPoliciesUseCase(self.secure, self.repository).execute()
            data = self.repository.read()

            expect(ok).to(be_true)
            expect(data).to_not(be_empty)

        with it("dumps rules to the repository"):
            ok, res = DumpUserCreatedRulesUseCase(self.secure, self.repository).execute()
            data = self.repository.read()

            expect(ok).to(be_true)
            expect(data).to_not(be_empty)

        with it("dumps falco macros to the repository"):
            ok, res = DumpUserCreatedFalcoMacrosUseCase(self.secure, self.repository).execute()
            data = self.repository.read()

            expect(ok).to(be_true)
            expect(data).to_not(be_empty)

        with it("dumps falco lists to the repository"):
            ok, res = DumpUserCreatedFalcoListsUseCase(self.secure, self.repository).execute()
            data = self.repository.read()
            expect(ok).to(be_true)
            expect(data).to_not(be_empty)

        with it("dumps everything to the repository"):
            ok, res_err = DumpEverythingUseCase(self.monitor, self.secure, self.repository).execute()
            data = self.repository.read()

            expect(ok).to(be_true)
            expect(data).to_not(be_empty)
