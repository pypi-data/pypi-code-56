from expects import expect, have_keys, raise_error
from mamba import context, description, it

from sdccli.helpers import annotation_arguments_to_map

with description(annotation_arguments_to_map):
    with context("when we use annotations to create a dashboard"):
        with it("splits the arguments and creates a map of annotations"):
            annotation_arguments = ["a=b", "c=d"]

            annotation_map = annotation_arguments_to_map(annotation_arguments)

            expect(annotation_map).to(have_keys(a="b", c="d"))

        with context("but the user does not specify a key"):
            with it("raises an error of invalid key"):
                annotation_arguments = ["a=b", "=d"]

                expect(lambda: annotation_arguments_to_map(annotation_arguments)).to(
                    raise_error(KeyError, "found null key for annotation =d")
                )

        with context("but the user does not specify a value"):
            with it("raises an error of invalid value"):
                annotation_arguments = ["a=b", "c="]

                expect(lambda: annotation_arguments_to_map(annotation_arguments)).to(
                    raise_error(AttributeError, "found null value for annotation c=")
                )

        with context("but the user specifies an incorrect format for annotation"):
            with it("raises an error of invalid annotation format"):
                annotation_arguments = ["a=b", "foobar"]

                expect(lambda: annotation_arguments_to_map(annotation_arguments)).to(
                    raise_error(ValueError, "annotation format error - annotations must be of the form "
                                            "(--annotation key=value), found: foobar")
                )
