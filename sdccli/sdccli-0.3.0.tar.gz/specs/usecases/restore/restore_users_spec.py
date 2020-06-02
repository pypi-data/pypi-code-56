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


with _description("Backup restore users") as self:
    with before.all:
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

    with context("with a backup created"):
        with before.all:
            user_email = "random-email-{}@localhost".format(_rand_text())
            _, created_user = self.monitor.create_user_invite(
                user_email=user_email,
                first_name="random-name-{}".format(_rand_text()),
                last_name=""
            )
            self.created_user = created_user["user"]

            DumpUsersUseCase(self.monitor, self.repository).execute()

        with after.all:
            ok, res = self.monitor.delete_user(self.created_user["username"])
            if not ok:
                print("unable to delete the user: {}".format(res))

        with context('with a missing user in the product'):
            with before.all:
                # Delete the created user
                self.monitor.delete_user(self.created_user["username"])

            with it("restores the user"):
                # Try to restore the user
                _, users_before = self.monitor.get_users()
                ok_restore, res_restore = RestoreUsersUseCase(self.monitor, self.repository).execute()
                _, users_after = self.monitor.get_users()

                expect(ok_restore).to(be_true)
                expect(len(users_before) + 1).to(equal(len(users_after)))

            with it("ignores the already created user"):
                _, users_before = self.monitor.get_users()
                ok_restore, res_restore = RestoreUsersUseCase(self.monitor, self.repository).execute()
                _, users_after = self.monitor.get_users()

                expect(ok_restore).to(be_true)
                expect(len(users_before)).to(equal(len(users_after)))
