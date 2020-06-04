import os


class VersionUtils(object):

    @staticmethod
    def get_version():
        root_dir = os.path.dirname(os.path.abspath(__file__)).replace("/securenative/utils", "")
        path = os.path.join(root_dir, "VERSION")
        with open(path) as f:
            return f.read()
