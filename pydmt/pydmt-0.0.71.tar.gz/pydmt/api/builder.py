import abc
from typing import List


class Builder(metaclass=abc.ABCMeta):
    """
    A Builder is what really builds things in the system.
    A builder knows on which inputs it relies and what
    outputs it generates (sometimes before build and sometimes
    after).
    """
    __metaclass__ = abc.ABCMeta

    def get_name(self) -> str:
        return self.__class__.__name__+" "+",".join(self.get_sources())+"->"+",".join(self.get_targets())

    @abc.abstractmethod
    def __init__(self):
        """ initialize your builder here """
        pass

    @abc.abstractmethod
    def build(self) -> None:
        """
        this method actually does the building
        Just do whatever you want here. Options are:
        - Write pure python code
        - Call native code
        - Call external programs
        - A combination of the above
        If there are any problems then throw an exception.
        Try not to segfault the interpreter in this method...:)
        """
        pass

    @abc.abstractmethod
    def get_sources(self) -> List[str]:
        """
        return the name of the source files for this builder
        If the builder takes a whole folder the list all the filers in that folder.
        If a built takes all the .py files in a folder then list those.
        In the current implementation this method is not really that important because
        it is not used to calculate the signature of the input to the build.
        The @get_signature method is use for that.
        In the future the get_signature method will go away.
        """
        pass

    def get_targets(self) -> List[str]:
        """ return the names of the files that you are sure you produce. If you do not know them,
        you must implement the 'get_targets_post_build' method and return None here."""
        return []

    def get_targets_post_build(self) -> List[str]:
        """ find out the names of the files that you produced.
        If you implemented the get_results_names and there you return all the results
        that you created then you don't need to implement anything here """
        return []

    @abc.abstractmethod
    def get_signature(self) -> str:
        """
        return the sha1 of anything that identifies the sources of the build
        Techically this is the sha1 of the file content of the list of files
        returned from :func:`~get_sources`
        """
        pass
