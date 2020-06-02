import os
import random
import string

from expects import *
from mamba import *

from sdccli.usecases.backup.dump import *
from sdccli.usecases.backup.restore import *

ORIGIN_SECURE_UI = 'Secure UI'

class _InMemoryRepository(object):
    def __init__(self):
        self.data = ""

    def write(self, data):
        self.data += data

    def read(self):
        return self.data


def _rand_text():
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=10))


# TODO: Move this to the python-sdc-client
def get_user_created_rules(secure: SdSecureClient):
    ok, res = secure.list_rules()
    if not ok:
        return False, res

    user_created_rules = []
    for list in res:
        for j, id in enumerate(list['ids']):
            if list['publishedBys'][j]['origin'] == ORIGIN_SECURE_UI:
                user_rules = list.copy()

                user_rules['id'] = list['ids'][j]
                del user_rules['ids']

                user_rules['publishedBy'] = list['publishedBys'][j]
                del user_rules['publishedBys']

                user_created_rules.append(user_rules)

    return True, user_created_rules


with description("Backup restore falco rules") as self:
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

        self.cleanup_rules()

        self.rule_to_test = f'sdc_cli_test_rule_{_rand_text()}'
        ok, res = self.add_test_rule(self.rule_to_test)
        expect(ok).to(be_true)
        DumpUserCreatedRulesUseCase(self.secure, self.repository).execute()

        self.cleanup_rules()

    with after.each:
        self.cleanup_rules()

    with it("restores the rule"):
        _, rules_before = get_user_created_rules(self.secure)
        ok_restore, res_restore = RestoreFalcoRulesUseCase(self.secure, self.repository).execute()
        _, rules_after = get_user_created_rules(self.secure)

        expect(ok_restore).to(be_true)
        expect(len(rules_before) + 1).to(equal(len(rules_after)))
        expect(rules_before).to_not(contain(have_keys({"name": self.rule_to_test})))
        expect(rules_after).to(contain(have_keys({"name": self.rule_to_test})))

    with it("ignores the already created rule"):
        RestoreFalcoRulesUseCase(self.secure, self.repository).execute()

        _, rules_before = get_user_created_rules(self.secure)
        ok_restore, res_restore = RestoreFalcoRulesUseCase(self.secure, self.repository).execute()
        _, rules_after = get_user_created_rules(self.secure)

        expect(ok_restore).to(be_true)
        expect(len(rules_before)).to(equal(len(rules_after)))
        expect(rules_before).to(contain(have_keys({"name": self.rule_to_test})))
        expect(rules_after).to(contain(have_keys({"name": self.rule_to_test})))

    with it("restores a modified rule"):
        RestoreFalcoRulesUseCase(self.secure, self.repository).execute()
        restored = [rule for rule in get_user_created_rules(self.secure)[1] if rule['name'] == self.rule_to_test][0]
        self.secure.update_rule(id=restored['id'], description='Updated rule')

        _, rules_before = get_user_created_rules(self.secure)
        _, rule_before = self.secure.get_rule_id(restored['id'])
        ok_restore, res_restore = RestoreFalcoRulesUseCase(self.secure, self.repository).execute()
        _, rules_after = get_user_created_rules(self.secure)
        _, rule_after = self.secure.get_rule_id(restored['id'])

        expect(ok_restore).to(be_true)
        expect(len(rules_before)).to(equal(len(rules_after)))
        expect(rules_before).to(contain(have_keys({"name": self.rule_to_test})))
        expect(rules_after).to(contain(have_keys({"name": self.rule_to_test})))
        expect(rule_before).to(have_keys({"name": self.rule_to_test, "description": "Updated rule"}))
        expect(rule_after).to(have_keys({"name": self.rule_to_test, "description": "Match all K8s Audit Events"}))

    with it("removes an unwanted rule"):
        unwanted_rule_name = f"sdc_cli_test_unwanted_rule_{_rand_text()}"
        self.add_test_rule(unwanted_rule_name)

        _, rules_before = get_user_created_rules(self.secure)
        ok_restore, res_restore = RemoveAndRestoreFalcoRulesUseCase(self.secure, self.repository).execute()
        _, rules_after = get_user_created_rules(self.secure)

        expect(ok_restore).to(be_true)
        expect(len(rules_before)).to(equal(len(rules_after)))
        expect(rules_before).to(contain(have_keys({"name": unwanted_rule_name})))
        expect(rules_before).to_not(contain(have_keys({"name": self.rule_to_test})))
        expect(rules_after).to(contain(have_keys({"name": self.rule_to_test})))
        expect(rules_after).to_not(contain(have_keys({"name": unwanted_rule_name})))


    def cleanup_rules(self):
        ok, user_created_rules = get_user_created_rules(self.secure)
        expect(ok).to(be_true)

        for rule in user_created_rules:
            if rule['name'].startswith('sdc_cli_test'):
                ok, res = self.secure.delete_rule(rule['id'])
                expect(ok).to(be_true)


    def add_test_rule(self, rule_name):
        return self.secure.add_rule(rule_name,
                                    details={'ruleType': 'FALCO',
                                             'condition': {'condition': 'kall', 'components': []},
                                             'priority': 'DEBUG',
                                             'source': 'k8s_audit',
                                             'append': 'false',
                                             'output': 'K8s Audit Event received (user=%ka.user.name verb=%ka.verb uri=%ka.uri obj=%jevt.obj)'},
                                    description='Match all K8s Audit Events')
