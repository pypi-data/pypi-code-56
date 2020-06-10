import red_raccoon.platforms
import hodgepodge.helpers
import unittest


class PlatformHelperTestCases(unittest.TestCase):
    def test_parse_platform(self):
        for platform, expected in (
                ("win", "windows"),
                ("windows", "windows"),
                ("osx", "macos"),
                ("macOS", "macos"),
                ("darwin", "macos"),
                ("mac os x", "macos"),
                ("OS X", "macos"),
                ("ubuntu", "ubuntu"),
                ("Ubuntu", "ubuntu"),
                ("CentOS", "centos"),
                ("RHEL", "rhel")
        ):
            result = red_raccoon.platforms.parse_platform(platform)
            self.assertEqual(expected, result)

    def mutate_platforms(self, platforms):
        mutations = set()
        for platform in hodgepodge.helpers.as_set(platforms):
            for func in [str.title, str.capitalize, str.lower, str.upper]:
                mutation = func(platform)
                if mutation not in mutations:
                    mutations.add(mutation)
        else:
            return mutations

    def test_list_includes_windows(self):
        for platforms, expected in (
                (["windows", "win"], True),
                (["win"], True),
                (["linux"], False),
        ):
            for mutation in self.mutate_platforms(platforms):
                result = red_raccoon.platforms.list_includes_windows(mutation)
                self.assertEqual(expected, result, mutation)

    def test_list_includes_linux(self):
        for platforms, expected in (
                (["linux"], True),
                (["ubuntu"], True),
                (["rhel"], True),
                (["centos"], True),
                (["suse"], True),
                (["opensuse"], True),
                (["fedora"], True),
                (["debian"], True),
                (["windows"], False),
        ):
            for mutation in self.mutate_platforms(platforms):
                result = red_raccoon.platforms.list_includes_linux(mutation)
                self.assertEqual(expected, result, mutation)

    def test_list_includes_macos(self):
        for platforms, expected in (
                (["osx"], True),
                (["os x"], True),
                (["mac os x"], True),
                (["macos"], True),
                (["mac"], True),
                (["windows"], False),
        ):
            for mutation in self.mutate_platforms(platforms):
                result = red_raccoon.platforms.list_includes_macos(mutation)
                self.assertEqual(expected, result)

    def test_list_includes_aws(self):
        for platforms, expected in (
                (["aws"], True),
                (["windows"], False),
        ):
            for mutation in self.mutate_platforms(platforms):
                result = red_raccoon.platforms.list_includes_aws(mutation)
                self.assertEqual(expected, result)

    def test_list_includes_azure(self):
        for platforms, expected in (
                (["azure"], True),
                (["azure ad"], True),
                (["windows"], False),
        ):
            for mutation in self.mutate_platforms(platforms):
                result = red_raccoon.platforms.list_includes_azure(mutation)
                self.assertEqual(expected, result)

    def test_list_includes_azure_ad(self):
        for platforms, expected in (
                (["azure"], False),
                (["azure ad"], True),
        ):
            for mutation in self.mutate_platforms(platforms):
                result = red_raccoon.platforms.list_includes_azure_ad(mutation)
                self.assertEqual(expected, result)

    def test_includes_gcp(self):
        for platforms, expected in (
                (["gcp"], True),
                (["aws"], False),
        ):
            for mutation in self.mutate_platforms(platforms):
                result = red_raccoon.platforms.list_includes_gcp(mutation)
                self.assertEqual(expected, result)

    def test_list_includes_android(self):
        for platforms, expected in (
                (["android"], True),
                (["ios"], False),
        ):
            for mutation in self.mutate_platforms(platforms):
                result = red_raccoon.platforms.list_includes_android(mutation)
                self.assertEqual(expected, result)

    def test_list_includes_ios(self):
        for platforms, expected in (
                (["ios"], True),
                (["android"], False),
        ):
            for mutation in self.mutate_platforms(platforms):
                result = red_raccoon.platforms.list_includes_ios(mutation)
                self.assertEqual(expected, result)

    def test_list_includes_mobile_platform(self):
        for platforms, expected in (
                (["android", "ios"], True),
                (["android"], True),
                (["ios"], True),
                (["windows", False]),
                (["linux", False]),
                (["macOS", False]),
        ):
            for mutation in self.mutate_platforms(platforms):
                result = red_raccoon.platforms.list_includes_mobile_platform(mutation)
                self.assertEqual(expected, result)

    def test_list_includes_office_365(self):
        for platforms, expected in (
                (["office 365"], True),
                (["office365"], True),
                (["o365"], True),
                (["azure", False]),
                (["windows", False]),
        ):
            for mutation in self.mutate_platforms(platforms):
                result = red_raccoon.platforms.list_includes_office_365(mutation)
                self.assertEqual(expected, result)

    def test_list_includes_software_as_a_service(self):
        for platforms, expected in (
                (["office365"], True),
                (["office 365"], True),
                (["o365"], True),
                (["saas"], True),
                (["windows", False]),
        ):
            for mutation in self.mutate_platforms(platforms):
                result = red_raccoon.platforms.list_includes_software_as_a_service(mutation)
                self.assertEqual(expected, result)

    def test_list_includes_infrastructure_as_a_service(self):
        for platforms, expected in (
                (["aws"], True),
                (["gcp"], True),
                (["azure"], True),
                (["azure ad"], False),
                (["windows", False]),
                (["linux"], False),
                (["macos"], False),
        ):
            for mutation in self.mutate_platforms(platforms):
                result = red_raccoon.platforms.list_includes_infrastructure_as_a_service(mutation)
                self.assertEqual(expected, result)
