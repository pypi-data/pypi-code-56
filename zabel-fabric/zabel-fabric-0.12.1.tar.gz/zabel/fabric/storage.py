# Copyright (c) 2019 Martin Lafaix (martin.lafaix@external.engie.com)
#
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
#
# SPDX-License-Identifier: EPL-2.0

"""
**amac** storage wrappers.

Implements some internal classes:

- #Storag: an interface for storage classes
- #ObjectStorage: an interface for storage classes handling one object
- #CollectionStorage: an interface for storage classes handling a
    collection of objects.

- #AWSS3Storage: an abstract class providing AWS S3 helpers
- #AWSS3Object: a Storage class for JSON files stored on a S3
- #AWSS3Bucket: a Storage class for handling S3 buckets

- #ManagedDict: a simple class making use of an #ObjectStorage
    delegate.
"""

from typing import Any, Dict, Iterator, List, Optional

import json

from zabel.commons.exceptions import ApiError
from zabel.commons.utils import ensure_instance, ensure_nonemptystring


########################################################################
## Storage Interfaces
##
## Storage
## ObjectStorage
## CollectionStorage


class Storage:
    """Abstract base storage wrapper.

    Declares the minimal set of features storage implementation must
    provide:

    - constructor (`__init__`)

    The constructor will take one parameter, a dictionary.  Its content
    is implementation-dependent.
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, configuration: Dict[str, Any]) -> None:
        """Initialize a new storage object.

        # Required parameters

        - `configuration`: a dictionary

        The `configuration` dictionary content is
        implementation-dependent.
        """
        ensure_instance('configuration', dict)

        self.configuration = configuration


class ObjectStorage(Storage):
    """Abstract object storage wrapper.

    Declares the minimal set of features storage implementation must
    provide:

    - `read`
    - `create`
    - `update`
    - `delete`

    The data format is unspecified, and is implementation-dependent.
    """

    def read(self) -> Any:
        """Return object from storage."""
        raise NotImplementedError

    def create(self, data: Any) -> None:
        """Create object in storage."""
        raise NotImplementedError

    def update(self, data: Any) -> None:
        """Update object in storage."""
        raise NotImplementedError

    def delete(self) -> None:
        """Remove object from storage."""
        raise NotImplementedError


class CollectionStorage(Storage):
    """Abstract collection storage wrapper.

    Declares the minimal set of features storage implementation must
    provide:

    - `list`
    - `read`
    - `create`
    - `update`
    - `delete`

    The data format is unspecified, and is implementation-dependent.
    """

    def list(self) -> List[Dict[str, Any]]:
        """Return list of items in storage.

        # Returned value

        A list. Each element in the list is a dictionary with at least
        a `key` entry:

        - `key`: a string

        It may contain a `last_modified` entry too, if appropriate:

        - `last_modified`: a datetime object
        """
        raise NotImplementedError

    def read(self, key: str) -> Any:
        """Return specified item from storage."""
        raise NotImplementedError

    def create(self, key: str, data: Any) -> None:
        """Create specified item in storage."""
        raise NotImplementedError

    def update(self, key: str, data: Any) -> None:
        """Update specified item in storage."""
        raise NotImplementedError

    def delete(self, key: str) -> None:
        """Remove specified item from storage."""
        raise NotImplementedError


########################################################################
## AWS Storage


class AWSS3Storage(Storage):
    """A base Storage abstract class for AWS S3 classes.

    Assumes the configuration dictionary contains the following entries:

    ```python
    {
        'storage': {
            'bucket': 'a string'
        }
    }
    ```
    """

    # pylint: disable=too-few-public-methods
    def __init__(self, configuration: Dict[str, Any]) -> None:
        """Initialize a new AWSS3Storage object."""
        super().__init__(configuration)
        from boto3.resources.factory import ServiceResource

        self._s3: Optional[ServiceResource] = None

    # Helpers

    def _get_bucket(self) -> Any:
        """Return the bucket."""
        if self._s3 is None:
            import boto3

            self._s3 = boto3.resource('s3')
        if self._s3 is None:
            raise ApiError('AWS S3 service resource is None.')
        return self._s3.Bucket(self.configuration['storage']['bucket'])

    def _get_object(self, name: str) -> Any:
        """Return the object."""
        return self._get_bucket().Object(name)


class AWSS3Bucket(AWSS3Storage, CollectionStorage):
    """Simple AWS S3 Storage class.

    This class handles objects stored in a S3 bucket.

    It uses the following configuration entry:

    ```python
    {
        'storage': {
            'bucket': 'a string'
        }
    }
    ```

    It must be an existing bucket name.

    Objects are stored as JSON objects.
    """

    def list(self) -> List[Dict[str, Any]]:
        return [
            {'key': item.key, 'last_modified': item.last_modified}
            for item in self._get_bucket().objects.all()
        ]

    def read(self, key: str) -> Dict[str, Any]:
        ensure_nonemptystring('key')

        obj = self._get_object(key)
        return json.loads(obj.get()['Body'].read().decode('utf-8'))  # type: ignore

    def create(self, key: str, data: Dict[str, Any]) -> None:
        ensure_nonemptystring('key')
        ensure_instance('data', dict)

        if self._has(key):
            raise ApiError('Object %s already exist.' % key)

        obj = self._get_object(key)
        obj.put(Body=bytes(json.dumps(data, default=str), 'utf-8'))

    def update(self, key: str, data: Dict[str, Any]) -> None:
        ensure_nonemptystring('key')
        ensure_instance('data', dict)

        if not self._has(key):
            raise ApiError('Object %s does not exist.' % key)

        obj = self._get_object(key)
        obj.put(Body=bytes(json.dumps(data, default=str), 'utf-8'))

    def _has(self, key: str) -> bool:
        _exists = True
        import botocore

        try:
            self._get_object(key).load()
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == '404':
                _exists = False
            else:
                raise

        return _exists


class AWSS3Object(AWSS3Storage, ObjectStorage):
    """Simple AWS S3 Object Storage class.

    This class handles objects stored in a S3 bucket.

    It enhance the platform definition with the following entries:

    ```python
    {
        'storage': {
            'bucket': 'a string',
            'filename': 'a string'
        }
    }
    ```

    It must be an existing bucket name, and file name is expected to
    be an existing and valid JSON object.

    The bucket may contain other objects, they will be ignored.
    """

    def read(self) -> Dict[str, Any]:
        """Return stored object as JSON."""
        obj = self._get_object(self.configuration['storage']['filename'])
        return json.loads(obj.get()['Body'].read().decode('utf-8'))  # type: ignore

    def update(self, data: Dict[str, Any]) -> None:
        """Update stored object."""
        obj = self._get_object(self.configuration['storage']['filename'])
        obj.put(Body=bytes(json.dumps(data, default=str), 'utf-8'))


########################################################################
## Useful Helpers


class ManagedDict(Dict[str, Any]):
    """Simple wrapper for dictionaries.

    It expects an _ObjectStorage_ object defined in its configuration
    data.

    Entries starting with an underscore ('_') are 'hidden', in that they
    are not returned by the `__iter__` method and `__contains__` does
    not see them (but they can be used to store values and are
    persisted).

    In other words, assuming `foo` is a managed dictionary:

    ```python
    >>> foo['bar'] = 123
    >>> foo['_bar'] = 456

    >>> foo['bar']              # => 123
    >>> foo['_bar']             # => 456
    >>> 'bar' in foo            # => True
    >>> '_bar' in foo           # => False
    >>> keys = [k for k in foo] # => ['bar']
    >>> sorted(foo)             # => ['bar']

    >>> # but
    >>> len(foo)                # => 2
    >>> foo.keys()              # => dict_keys(['bar', '_bar'])
    >>> foo.items()             # => dict_items([('bar', 123),
    >>>                         #                ('_bar', 456)])
    >>> foo.values()            # => dict_values([123, 456])
    ```
    """

    def __init__(self, configuration: Dict[str, Any]) -> None:
        """Initialize a managed dict.

        The initial content of the managed dictionary is read according
        to `configuration`.

        Changes are allowed during the life of the managed dictionary.
        Use the `persist` method to save them.

        # Required parameters

        - `configuration`: a dictionary

        `configuration` is a dictionary with the following entry:

        - `storage`: a dictionary

        `storage` is a dictionary with at least the following entry:

        - `type`: a class subclassing __ObjectStorage__

        It may also contain additional entries, depending on its `type`
        class.
        """
        super().__init__()
        self._storage = configuration['storage']['type'](configuration)
        source = self._storage.read()
        for key in source:
            self[key] = source[key]

    def __iter__(self) -> Iterator[str]:
        for k in super().__iter__():
            if not k.startswith('_'):
                yield k

    def __contains__(self, key: object) -> bool:
        return (
            isinstance(key, str)
            and super().__contains__(key)
            and not key.startswith('_')
        )

    def persist(self) -> None:
        """Persist the dictionary."""
        self._storage.update(self)
