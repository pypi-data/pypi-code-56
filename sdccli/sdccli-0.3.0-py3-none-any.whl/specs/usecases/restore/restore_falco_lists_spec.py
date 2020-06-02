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


# TODO: Move this to the python-sdc-client
def get_user_created_lists(secure: SdSecureClient):
    ok, res = secure.list_falco_lists()
    if not ok:
        return False, res

    user_created_lists = []
    for list in res:
        for j, id in enumerate(list['ids']):
            if list['publishedBys'][j]['origin'] == 'Secure UI':
                user_list = list.copy()

                user_list['id'] = list['ids'][j]
                del user_list['ids']

                user_list['publishedBy'] = list['publishedBys'][j]
                del user_list['publishedBys']

                user_created_lists.append(user_list)

    return True, user_created_lists


with description("Backup restore falco lists") as self:
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

        self.cleanup_lists()
        self.list_to_test = f'sdc_cli_test_list_{_rand_text()}'
        ok, res = self.secure.add_falco_list(self.list_to_test, ["a", "b", "c"])
        expect(ok).to(be_true)

        DumpUserCreatedFalcoListsUseCase(self.secure, self.repository).execute()

        self.cleanup_lists()

    with after.each:
        self.cleanup_lists()

    with it("restores the list"):
        _, lists_before = get_user_created_lists(self.secure)
        ok_restore, res_restore = RestoreFalcoListsUseCase(self.secure, self.repository).execute()
        _, lists_after = get_user_created_lists(self.secure)

        expect(ok_restore).to(be_true)
        expect(len(lists_before) + 1).to(equal(len(lists_after)))
        expect(lists_after).to(contain(have_keys({"name": self.list_to_test})))

    with it("ignores the already created list"):
        RestoreFalcoListsUseCase(self.secure, self.repository).execute()

        _, lists_before = get_user_created_lists(self.secure)
        ok_restore, res_restore = RestoreFalcoListsUseCase(self.secure, self.repository).execute()
        _, lists_after = get_user_created_lists(self.secure)

        expect(ok_restore).to(be_true)
        expect(len(lists_before)).to(equal(len(lists_after)))
        expect(lists_after).to(contain(have_keys({"name": self.list_to_test})))

    with it("restores a modified list"):
        RestoreFalcoListsUseCase(self.secure, self.repository).execute()
        restored = [list for list in get_user_created_lists(self.secure)[1] if list['name'] == self.list_to_test][0]
        self.secure.update_falco_list(restored['id'], ['a', 'b', 'c', 'd'])

        _, lists_before = get_user_created_lists(self.secure)
        _, list_before = self.secure.get_falco_list_id(restored['id'])
        ok_restore, res_restore = RestoreFalcoListsUseCase(self.secure, self.repository).execute()
        _, lists_after = get_user_created_lists(self.secure)
        _, list_after = self.secure.get_falco_list_id(restored['id'])

        expect(ok_restore).to(be_true)
        expect(len(lists_before)).to(equal(len(lists_after)))
        expect(list_before).to(have_keys({"name": self.list_to_test, 'items': {'items': ['a', 'b', 'c', 'd']}}))
        expect(list_after).to(have_keys({"name": self.list_to_test, 'items': {'items': ['a', 'b', 'c']}}))

    with it("removes an unwanted list"):
        unwanted_list_name = f"sdc_cli_test_unwanted_falco_list_{_rand_text()}"
        self.secure.add_falco_list(unwanted_list_name, ['a', 'b'])

        _, lists_before = get_user_created_lists(self.secure)
        ok_restore, res_restore = RemoveAndRestoreFalcoListsUseCase(self.secure, self.repository).execute()
        _, lists_after = get_user_created_lists(self.secure)

        expect(ok_restore).to(be_true)
        expect(len(lists_before)).to(equal(len(lists_after)))
        expect(lists_before).to(contain(have_keys({"name": unwanted_list_name})))
        expect(lists_before).to_not(contain(have_keys({"name": self.list_to_test})))
        expect(lists_after).to(contain(have_keys({"name": self.list_to_test})))
        expect(lists_after).to_not(contain(have_keys({"name": unwanted_list_name})))


    def cleanup_lists(self):
        ok, user_created_lists = get_user_created_lists(self.secure)
        expect(ok).to(be_true)

        for list in user_created_lists:
            if list['name'].startswith('sdc_cli_test'):
                ok, res = self.secure.delete_falco_list(list['id'])
                expect(ok).to(be_true)
