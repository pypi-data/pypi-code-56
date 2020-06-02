import os
import random
import string

from expects import *
from mamba import *

from sdccli.falco_macro import SortMacrosByDepedency
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


with description("Backup restore falco macros") as self:
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

        self.cleanup_macros()
        self.macro_to_test = f'sdc_cli_test_always_true_{_rand_text()}'
        ok, _ = self.secure.add_falco_macro(self.macro_to_test, 'always_true')
        expect(ok).to(be_true)

        DumpUserCreatedFalcoMacrosUseCase(self.secure, self.repository).execute()

        self.cleanup_macros()

    with after.each:
        self.cleanup_macros()

    with it("restores the macro"):
        _, macros_before = drop.get_user_created_macros(self.secure)
        ok_restore, res_restore = RestoreFalcoMacrosUseCase(self.secure, self.repository).execute()
        _, macros_after = drop.get_user_created_macros(self.secure)

        expect(ok_restore).to(be_true)
        expect(len(macros_before) + 1).to(equal(len(macros_after)))
        expect(macros_after).to(contain(have_keys({"name": self.macro_to_test})))

    with it("ignores the already restored macro"):
        RestoreFalcoMacrosUseCase(self.secure, self.repository).execute()

        _, macros_before = drop.get_user_created_macros(self.secure)
        ok_restore, res_restore = RestoreFalcoMacrosUseCase(self.secure, self.repository).execute()
        _, macros_after = drop.get_user_created_macros(self.secure)

        expect(ok_restore).to(be_true)
        expect(len(macros_before)).to(equal(len(macros_after)))
        expect(macros_after).to(contain(have_keys({"name": self.macro_to_test})))

    with it("restores a modified macro"):
        RestoreFalcoMacrosUseCase(self.secure, self.repository).execute()
        restored = \
            [macro for macro in drop.get_user_created_macros(self.secure)[1] if macro['name'] == self.macro_to_test][0]
        self.secure.update_falco_macro(restored['id'], 'always_true and always_true')

        _, macros_before = drop.get_user_created_macros(self.secure)
        _, macro_before = self.secure.get_falco_macro_id(restored['id'])
        ok_restore, res_restore = RestoreFalcoMacrosUseCase(self.secure, self.repository).execute()
        _, macros_after = drop.get_user_created_macros(self.secure)
        restored = \
            [macro for macro in drop.get_user_created_macros(self.secure)[1] if macro['name'] == self.macro_to_test][0]
        _, macro_after = self.secure.get_falco_macro_id(restored['id'])

        expect(ok_restore).to(be_true)
        expect(len(macros_before)).to(equal(len(macros_after)))
        expect(macros_after).to(contain(have_keys({"name": self.macro_to_test})))
        expect(macro_before).to(
            have_keys({"name": self.macro_to_test, "condition": {"condition": "always_true and always_true"}}))
        expect(macro_after).to(have_keys({"name": self.macro_to_test, "condition": {"condition": "always_true"}}))

    with it("removes an unwanted macro"):
        self.secure.add_falco_macro(f"sdc_cli_test_unwanted_falco_macro_{_rand_text()}", "always_true")
        RestoreFalcoMacrosUseCase(self.secure, self.repository).execute()

        _, macros_before = drop.get_user_created_macros(self.secure)
        ok_restore, res_restore = RemoveAndRestoreFalcoMacrosUseCase(self.secure, self.repository).execute()
        _, macros_after = drop.get_user_created_macros(self.secure)

        expect(ok_restore).to(be_true)
        expect(len(macros_before) - 1).to(equal(len(macros_after)))
        expect(macros_after).to(contain(have_keys({"name": self.macro_to_test})))

    with it("resolves macro dependencies gracefully and removes and restores them"):
        rand_name = _rand_text()
        self.secure.add_falco_macro(f"sdc_cli_test_unwanted_falco_macro_A_{rand_name}", "always_true")
        self.secure.add_falco_macro(f"sdc_cli_test_unwanted_falco_macro_B_{rand_name}", "always_true")
        self.secure.add_falco_macro(f"sdc_cli_test_unwanted_falco_macro_C_{rand_name}",
                                    f"sdc_cli_test_unwanted_falco_macro_A_{rand_name} and sdc_cli_test_unwanted_falco_macro_B_{rand_name}")
        self.secure.add_falco_macro(f"sdc_cli_test_unwanted_falco_macro_D_{rand_name}",
                                    f"sdc_cli_test_unwanted_falco_macro_C_{rand_name} and sdc_cli_test_unwanted_falco_macro_A_{rand_name}")
        self.secure.add_falco_macro(f"sdc_cli_test_unwanted_falco_macro_E_{rand_name}",
                                    f"sdc_cli_test_unwanted_falco_macro_D_{rand_name}")
        new_repository = _InMemoryRepository()
        ok, res = DumpUserCreatedFalcoMacrosUseCase(self.secure, new_repository).execute()

        ok_restore, res_restore = RemoveAndRestoreFalcoMacrosUseCase(self.secure, new_repository).execute()
        expect(ok_restore).to(be_true)


    def cleanup_macros(self):
        ok, user_created_macros = drop.get_full_user_created_macros(self.secure)
        user_created_macros = SortMacrosByDepedency(user_created_macros).sort()
        expect(ok).to(be_true)

        for macro in user_created_macros:
            if macro['name'].startswith('sdc_cli_test'):
                ok, res = self.secure.delete_falco_macro(macro['id'])
                expect(ok).to(be_true)
