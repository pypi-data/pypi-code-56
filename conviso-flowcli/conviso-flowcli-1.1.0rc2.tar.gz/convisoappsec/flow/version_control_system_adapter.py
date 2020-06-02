import git
import tempfile
import warnings

class GitAdapter(object):
    LIST_OPTION = '--list'
    SORT_OPTION = '--sort'
    OPTION_WITH_ARG_FMT = '{option}={value}'
    EMPTY_REPOSITORY_HASH = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'

    def __init__(self, repository_dir='.'):
        self._git_client = git.cmd.Git(repository_dir)

    def tags(self, sort='-taggerdate'):
        sort_option = self.OPTION_WITH_ARG_FMT.format(
            option=self.SORT_OPTION,
            value=sort,
        )

        args = (self.LIST_OPTION, sort_option)
        client_output = self._git_client.tag(args)
        tags = client_output.splitlines()
        return tags

    def diff(self, version, another_version):
        version = version or self.EMPTY_REPOSITORY_HASH

        if version == self.EMPTY_REPOSITORY_HASH:
            warnings.warn(
                "Creating diff comparing revision[{0}] and the repository beginning".format(
                    another_version
                )
            )

        diff_file = tempfile.TemporaryFile()
        self._git_client.diff(
            version,
            another_version,
            output_stream=diff_file
        )

        return diff_file