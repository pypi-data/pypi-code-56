import datetime
import enum
from typing import Union

import pytz

from trompace import filter_none_args, StringConstant
from trompace.constants import SUPPORTED_LANGUAGES
from trompace.exceptions import UnsupportedLanguageException
from trompace.mutations import MUTATION
from trompace.mutations.templates import format_mutation


class AnnotationSchemaMotivation(enum.Enum):
    assessing = "62d7002d-b287-4a7a-a062-ec6671cd8308"
    bookmarking = "46ac7c02-3e97-4f9b-8f44-72460e49f0ed"
    classifying = "a26ee2b9-c499-42f5-8119-57159c29837f"
    commenting = "e2a0f1bf-f468-412a-badc-8568be0c148b"
    describing = "5882b199-67a2-4da2-914a-a545fc1287e3"
    editing = "296fb059-d268-420d-8f3d-1fa2150902de"
    highlighting = "d56c5c2b-06d8-4fa7-b117-2d053f583732"
    identifying = "59a49e56-86ed-412c-925d-1e8c9edcfb5c"
    linking = "6b016fbc-4048-4840-b7ba-8e1ea8f4293c"
    moderating = "7b8c4187-a802-4cb0-badd-26970a24ff42"
    questioning = "eb1dffeb-6f42-4460-99e6-840fdc7305dc"
    replying = "eddb01b5-08e7-49e4-ab19-ddf27eb700c9"
    tagging = "b2004aeb-0088-4509-8bbf-3365223f6b22"


def create_annotation_url_target(url: str):
    """Return a mutation for making an AnnotationURLTarget.
    An AnnotationURLTarget is a node that can be used for a
    web Annotation (https://www.w3.org/TR/annotation-model)
    as the target field, when the target refers to an external URL

    Arguments:
        url: a URL to the target of an annotation

    Returns:
        A GraphQL Mutation to create an AnnotationURLTarget in the Trompa CE
    """
    # TODO: Validate the format of a url?
    params = {"url": url}
    annurltarget = format_mutation(mutationname="CreateAnnotationURLTarget", args=params)
    mutation = MUTATION.format(mutation=annurltarget)
    return mutation


def create_annotation_ce_target(target: str, field: str, fragment: str = None):
    """Return a mutation for making an AnnotationCETarget.
    An AnnotationCETarget is a node that can be used for a
    web Annotation (https://www.w3.org/TR/annotation-model)
    as the target field, when the target refers to a node that already exists in the CE

    Arguments:
        target: the ID of a node that is in the CE
        field: the field of the node `target` that contains the URL to the target item
        fragment: If the target is a fragment, the value to be appended to the URL in field

    Returns:
        A GraphQL Mutation to create an AnnotationCETarget in the Trompa CE
    """
    params = {"target": target,
              "field": field,
              "fragment": fragment}
    params = filter_none_args(params)

    anncetarget = format_mutation(mutationname="CreateAnnotationCETarget", args=params)
    mutation = MUTATION.format(mutation=anncetarget)
    return mutation


def create_annotation_ce_motivation(parent_motivation: AnnotationSchemaMotivation, motivation: str):
    """Return a mutation for making an AnnotationCEMotivation.
    An AnnotationCEMotivation is a custom motivation for a
    web Annotation (https://www.w3.org/TR/annotation-model), which can be used to
    define the reason for which an annotation was made.
    Custom motivations should be derived from one of the existing motivation types, so that
    clients who do not understand this specific type can still show the motivation in a generic manner.

    Arguments:
        parent_motivation: an existing AnnotationSchemaMotivation which this new motivation is a special-case of
        motivation: the name of this new motivation

    Returns:
        A GraphQL Mutation to create an AnnotationCEMotivation in the Trompa CE
    """

    params = {"parent_motivation": parent_motivation,
              "motivation": motivation}

    anncemotivation = format_mutation(mutationname="CreateAnnotationCEMotivation", args=params)
    mutation = MUTATION.format(mutation=anncemotivation)
    return mutation


def create_annotation_textual_body(value: str, format_: str = None, language: str = None):
    """Return a mutation for making an AnnotationTextualBody.
    An AnnotationTextualBody is the main written body of a
    web Annotation (https://www.w3.org/TR/annotation-model).

    Arguments:
        value: the text for the body of the annotation
        format_: the mimetype that value is formatted in
        language: the language that value is written in

    Returns:
        A GraphQL Mutation to create an AnnotationTextualBody in the Trompa CE
    """

    if language and language.lower() not in SUPPORTED_LANGUAGES:
        raise UnsupportedLanguageException(language)

    params = {"value": value,
              "format": format_}

    if language is not None:
        params["language"] = StringConstant(language.lower())

    anntextbody = format_mutation(mutationname="CreateAnnotationTextualBody", args=params)
    mutation = MUTATION.format(mutation=anntextbody)
    return mutation


def create_annotation_ce_body(target: str):
    """Return a mutation for making an AnnotationCEBody.
    An AnnotationCEBody is a node that can be used for a
    web Annotation (https://www.w3.org/TR/annotation-model)
    as the body field, when the body refers to an external URL

    Arguments:
        target: the ID of a node that is in the CE

    Returns:
        A GraphQL Mutation to create an AnnotationCEBody in the Trompa CE
    """
    params = {"target": target}
    anncebody = format_mutation(mutationname="CreateAnnotationCEBody", args=params)
    mutation = MUTATION.format(mutation=anncebody)
    return mutation


def create_annotation_url_body(url: str):
    """Return a mutation for making an AnnotationURLBody.
    An AnnotationURLBody is a node that can be used for a
    web Annotation (https://www.w3.org/TR/annotation-model)
    as the body field, when the body refers to an external URL

    Arguments:
        url: a URL to the body of an annotation

    Returns:
        A GraphQL Mutation to create an AnnotationURLBody in the Trompa CE
    """
    # TODO: Validate the format of a url?
    params = {"target": url}
    annurlbody = format_mutation(mutationname="CreateAnnotationURLBody", args=params)
    mutation = MUTATION.format(mutation=annurlbody)
    return mutation


def create_annotation(target: str, motivation: Union[AnnotationSchemaMotivation, str], body: str, creator: str = None):
    """Return a mutation for making an Annotation.
    A web Annotation (https://www.w3.org/TR/annotation-model)
    # TODO: Finish

    Arguments:
        target: the ID of a target node (either an AnnotationURLTarget or an AnnotationCETarget)
        motivation: a AnnotationSchemaMotivation value, or the ID of an AnnotationCEMotivation node)
        body: the ID of a body node (AnnotationTextualBody, AnnotationCEBody, AnnotationURLBody)
        creator: a URI to the identity of the user who created this Annotation

    Returns:
        A GraphQL Mutation to create an Annotation in the Trompa CE
    """
    utcnow = datetime.datetime.now(pytz.UTC)

    params = {"target": target,
              "motivation": motivation,
              "body": body,
              "creator": creator,
              "created": utcnow}
    params = filter_none_args(params)

    annotation = format_mutation(mutationname="CreateAnnotation", args=params)
    mutation = MUTATION.format(mutation=annotation)
    return mutation


# TODO: Does it make sense to have update methods for these things? Other than body it seems like they're all joiners
#       and updating something should involve deleting it and creating a new one
def update_annotation_url_target(identifier: str, url: str = None):
    """Return a mutation for updating an AnnotationURLTarget.

    Returns:
        A GraphQL Mutation to update an AnnotationURLTarget in the Trompa CE
    """
    params = {"identifier": identifier,
              "url": url}
    params = filter_none_args(params)

    annurltarget = format_mutation(mutationname="UpdateAnnotationURLTarget", args=params)
    mutation = MUTATION.format(mutation=annurltarget)
    return mutation


def update_annotation_ce_target(identifier: str, target: str = None, field: str = None, fragment: str = None):
    """Return a mutation for updating an AnnotationCETarget.

    Returns:
        A GraphQL Mutation to update an AnnotationCETarget in the Trompa CE
    """
    params = {"identifier": identifier,
              "target": target,
              "field": field,
              "fragment": fragment}
    params = filter_none_args(params)

    anncetarget = format_mutation(mutationname="UpdateAnnotationCETarget", args=params)
    mutation = MUTATION.format(mutation=anncetarget)
    return mutation


def update_annotation_ce_motivation(identifier: str, parent_motivation: AnnotationSchemaMotivation = None, motivation: str = None):
    """Return a mutation for updating an AnnotationCEMotivation.

    Returns:
        A GraphQL Mutation to update an AnnotationCEMotivation in the Trompa CE
    """

    params = {"identifier": identifier,
              "parent_motivation": parent_motivation,
              "motivation": motivation}
    params = filter_none_args(params)

    anncemotivation = format_mutation(mutationname="UpdateAnnotationCEMotivation", args=params)
    mutation = MUTATION.format(mutation=anncemotivation)
    return mutation


def update_annotation_textual_body(identifier: str, value: str = None, format_: str = None, language: str = None):
    """Return a mutation for updating an AnnotationTextualBody.

    Returns:
        A GraphQL Mutation to update an AnnotationTextualBody in the Trompa CE
    """
    if language and language.lower() not in SUPPORTED_LANGUAGES:
        raise UnsupportedLanguageException(language)

    params = {"identifier": identifier,
              "value": value,
              "format": format_}
    params = filter_none_args(params)

    if language is not None:
        params["language"] = StringConstant(language.lower())

    anntextbody = format_mutation(mutationname="UpdateAnnotationTextualBody", args=params)
    mutation = MUTATION.format(mutation=anntextbody)
    return mutation


def update_annotation_ce_body(identifier: str, target: str = None):
    """Return a mutation for updating an AnnotationCEBody.

    Returns:
        A GraphQL Mutation to update an AnnotationCEBody in the Trompa CE
    """
    params = {"identifier": identifier,
              "target": target}
    params = filter_none_args(params)

    anncebody = format_mutation(mutationname="UpdateAnnotationCEBody", args=params)
    mutation = MUTATION.format(mutation=anncebody)
    return mutation


def update_annotation_url_body(identifier: str, url: str):
    """Return a mutation for updating an AnnotationURLBody.

    Returns:
        A GraphQL Mutation to update an AnnotationURLBody in the Trompa CE
    """
    params = {"identifier": identifier,
              "target": url}
    annurlbody = format_mutation(mutationname="UpdateAnnotationURLBody", args=params)
    mutation = MUTATION.format(mutation=annurlbody)
    return mutation


def update_annotation(identifier: str, target: str = None, motivation: Union[AnnotationSchemaMotivation, str] = None,
                      body: str = None, creator: str = None):
    """Return a mutation for updating an Annotation.

    Returns:
        A GraphQL Mutation to create an Annotation in the Trompa CE
    """
    utcnow = datetime.datetime.now(pytz.UTC)

    params = {"identifier": identifier,
              "target": target,
              "motivation": motivation,
              "body": body,
              "creator": creator,
              "modified": utcnow}
    params = filter_none_args(params)

    annotation = format_mutation(mutationname="UpdateAnnotation", args=params)
    mutation = MUTATION.format(mutation=annotation)
    return mutation


def delete_annotation_url_target(identifier: str):
    """Return a mutation for deleting an AnnotationURLTarget.

    Arguments:
        identifier: The identifier of the AnnotationURLTarget to delete

    Returns:
        A GraphQL Mutation to delete an AnnotationURLTarget from the Trompa CE
    """
    params = {"identifier": identifier}
    annurltarget = format_mutation(mutationname="DeleteAnnotationURLTarget", args=params)
    return MUTATION.format(mutation=annurltarget)


def delete_annotation_ce_target(identifier: str):
    """Return a mutation for deleting an AnnotationCETarget.

    Arguments:
        identifier: The identifier of the AnnotationCETarget to delete

    Returns:
        A GraphQL Mutation to delete an AnnotationCETarget from the Trompa CE
    """
    params = {"identifier": identifier}
    anncetarget = format_mutation(mutationname="DeleteAnnotationCETarget", args=params)
    return MUTATION.format(mutation=anncetarget)


def delete_annotation_ce_motivation(identifier: str):
    """Return a mutation for deleting an AnnotationCEMotivation.

    Arguments:
        identifier: The identifier of the AnnotationCEMotivation to delete

    Returns:
        A GraphQL Mutation to delete an AnnotationCEMotivation from the Trompa CE
    """
    params = {"identifier": identifier}
    anncemotiv = format_mutation(mutationname="DeleteAnnotationCEMotivation", args=params)
    return MUTATION.format(mutation=anncemotiv)


def delete_annotation_textual_body(identifier: str):
    """Return a mutation for deleting an AnnotationTextualBody.

    Arguments:
        identifier: The identifier of the AnnotationTextualBody to delete

    Returns:
        A GraphQL Mutation to delete an AnnotationTextualBody from the Trompa CE
    """
    params = {"identifier": identifier}
    anntextbody = format_mutation(mutationname="DeleteAnnotationTextualBody", args=params)
    return MUTATION.format(mutation=anntextbody)


def delete_annotation_ce_body(identifier: str):
    """Return a mutation for deleting an AnnotationCEBody.

    Arguments:
        identifier: The identifier of the AnnotationCEBody to delete

    Returns:
        A GraphQL Mutation to delete an AnnotationCEBody from the Trompa CE
    """
    params = {"identifier": identifier}
    anncebody = format_mutation(mutationname="DeleteAnnotationCEBody", args=params)
    return MUTATION.format(mutation=anncebody)


def delete_annotation_url_body(identifier: str):
    """Return a mutation for deleting an AnnotationURLBody.

    Arguments:
        identifier: The identifier of the AnnotationURLBody to delete

    Returns:
        A GraphQL Mutation to delete an AnnotationURLBody from the Trompa CE
    """
    params = {"identifier": identifier}
    annurlbody = format_mutation(mutationname="DeleteAnnotationURLBody", args=params)
    return MUTATION.format(mutation=annurlbody)


def delete_annotation(identifier: str):
    """Return a mutation for deleting an Annotation.

    Arguments:
        identifier: The identifier of the Annotation to delete

    Returns:
        A GraphQL Mutation to delete an Annotation from the Trompa CE
    """
    params = {"identifier": identifier}
    annotation = format_mutation(mutationname="DeleteAnnotation", args=params)
    return MUTATION.format(mutation=annotation)
