import os
import random
import string

from expects import *
from mamba import *

from sdccli.usecases.backup import DumpPoliciesUseCase
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


with description("Backup restore policies") as self:
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

        self.cleanup_policies()

        self.policy_test_name = f"[sdc-cli-test] random-policy-{_rand_text()}"
        ok, _ = self.secure.add_policy(self.policy_test_name, "Description")
        expect(ok).to(be_true)
        DumpPoliciesUseCase(self.secure, self.repository).execute()

        self.cleanup_policies()

    with after.each:
        self.cleanup_policies()

    with it('restores the policy'):
        _, policies_before = self.secure.list_policies()
        ok_restore, res_restore = RestorePoliciesUseCase(self.secure, self.repository).execute()
        _, policies_after = self.secure.list_policies()

        expect(ok_restore).to(be_true)
        expect(len(policies_before) + 1).to(equal(len(policies_after)))
        expect(policies_before).to_not(contain(have_keys({'name': self.policy_test_name})))
        expect(policies_after).to(contain(have_keys({'name': self.policy_test_name})))

    with it('ignores the already restored policy'):
        RestorePoliciesUseCase(self.secure, self.repository).execute()

        _, policies_before = self.secure.list_policies()
        ok_restore, res_restore = RestorePoliciesUseCase(self.secure, self.repository).execute()
        _, policies_after = self.secure.list_policies()

        expect(ok_restore).to(be_true)
        expect(len(policies_before)).to(equal(len(policies_after)))
        expect(policies_before).to(contain(have_keys({'name': self.policy_test_name})))
        expect(policies_after).to(contain(have_keys({'name': self.policy_test_name})))

    with it('recreates a modified policy'):
        RestorePoliciesUseCase(self.secure, self.repository).execute()
        _, policies = self.secure.list_policies()
        restored = [policy for policy in policies if policy['name'] == self.policy_test_name][0]
        self.secure.update_policy(id=restored['id'], description='Updated description')

        _, policies_before = self.secure.list_policies()
        ok_restore, res_restore = RestorePoliciesUseCase(self.secure, self.repository).execute()
        _, policies_after = self.secure.list_policies()

        expect(ok_restore).to(be_true)
        expect(len(policies_before)).to(equal(len(policies_after)))
        expect(policies_before).to(
            contain(have_keys({'name': self.policy_test_name, 'description': 'Updated description'})))
        expect(policies_after).to(contain(have_keys({'name': self.policy_test_name, 'description': 'Description'})))

    with it('removes an unwanted policy and restores the policy in the backup'):
        ok, _ = self.secure.add_policy(f"[sdc-cli-test] random-unwanted-policy-{_rand_text()}", "Description")

        _, policies_before = self.secure.list_policies()
        ok_restore, res_restore = RemoveAndRestorePoliciesUseCase(self.secure, self.repository).execute()
        _, policies_after = self.secure.list_policies()

        expect(ok_restore).to(be_true)
        expect(len(policies_before)).to(equal(len(policies_after)))
        expect(policies_before).to(contain(have_keys({'name': start_with('[sdc-cli-test] random-unwanted-policy-')})))
        expect(policies_before).to_not(contain(have_keys({'name': self.policy_test_name})))
        expect(policies_after).to_not(
            contain(have_keys({'name': start_with('[sdc-cli-test] random-unwanted-policy-')})))
        expect(policies_after).to(contain(have_keys({'name': self.policy_test_name})))


    def cleanup_policies(self):
        ok, res = self.secure.list_policies()
        expect(ok).to(be_true)

        for policy in res:
            if policy["name"].startswith("[sdc-cli-test]"):
                ok, _ = self.secure.delete_policy_id(policy["id"])
                expect(ok).to(be_true)
