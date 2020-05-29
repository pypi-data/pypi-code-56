# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

from .utils import NamespacedClient, query_params, _make_path, SKIP_IN_PATH


class SnapshotClient(NamespacedClient):
    @query_params("master_timeout", "wait_for_completion")
    def create(self, repository, snapshot, body=None, params=None, headers=None):
        """
        Creates a snapshot in a repository.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/modules-snapshots.html>`_

        :arg repository: A repository name
        :arg snapshot: A snapshot name
        :arg body: The snapshot definition
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        :arg wait_for_completion: Should this request wait until the
            operation has completed before returning
        """
        for param in (repository, snapshot):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_snapshot", repository, snapshot),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("master_timeout")
    def delete(self, repository, snapshot, params=None, headers=None):
        """
        Deletes a snapshot.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/modules-snapshots.html>`_

        :arg repository: A repository name
        :arg snapshot: A snapshot name
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        """
        for param in (repository, snapshot):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_snapshot", repository, snapshot),
            params=params,
            headers=headers,
        )

    @query_params("ignore_unavailable", "master_timeout", "verbose")
    def get(self, repository, snapshot, params=None, headers=None):
        """
        Returns information about a snapshot.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/modules-snapshots.html>`_

        :arg repository: A repository name
        :arg snapshot: A comma-separated list of snapshot names
        :arg ignore_unavailable: Whether to ignore unavailable
            snapshots, defaults to false which means a SnapshotMissingException is
            thrown
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        :arg verbose: Whether to show verbose snapshot info or only show
            the basic info found in the repository index blob
        """
        for param in (repository, snapshot):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "GET",
            _make_path("_snapshot", repository, snapshot),
            params=params,
            headers=headers,
        )

    @query_params("master_timeout", "timeout")
    def delete_repository(self, repository, params=None, headers=None):
        """
        Deletes a repository.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/modules-snapshots.html>`_

        :arg repository: Name of the snapshot repository to unregister.
            Wildcard (`*`) patterns are supported.
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        :arg timeout: Explicit operation timeout
        """
        if repository in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'repository'.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_snapshot", repository),
            params=params,
            headers=headers,
        )

    @query_params("local", "master_timeout")
    def get_repository(self, repository=None, params=None, headers=None):
        """
        Returns information about a repository.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/modules-snapshots.html>`_

        :arg repository: A comma-separated list of repository names
        :arg local: Return local information, do not retrieve the state
            from master node (default: false)
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        """
        return self.transport.perform_request(
            "GET", _make_path("_snapshot", repository), params=params, headers=headers
        )

    @query_params("master_timeout", "timeout", "verify")
    def create_repository(self, repository, body, params=None, headers=None):
        """
        Creates a repository.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/modules-snapshots.html>`_

        :arg repository: A repository name
        :arg body: The repository definition
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        :arg timeout: Explicit operation timeout
        :arg verify: Whether to verify the repository after creation
        """
        for param in (repository, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_snapshot", repository),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("master_timeout", "wait_for_completion")
    def restore(self, repository, snapshot, body=None, params=None, headers=None):
        """
        Restores a snapshot.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/modules-snapshots.html>`_

        :arg repository: A repository name
        :arg snapshot: A snapshot name
        :arg body: Details of what to restore
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        :arg wait_for_completion: Should this request wait until the
            operation has completed before returning
        """
        for param in (repository, snapshot):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "POST",
            _make_path("_snapshot", repository, snapshot, "_restore"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("ignore_unavailable", "master_timeout")
    def status(self, repository=None, snapshot=None, params=None, headers=None):
        """
        Returns information about the status of a snapshot.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/modules-snapshots.html>`_

        :arg repository: A repository name
        :arg snapshot: A comma-separated list of snapshot names
        :arg ignore_unavailable: Whether to ignore unavailable
            snapshots, defaults to false which means a SnapshotMissingException is
            thrown
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        """
        return self.transport.perform_request(
            "GET",
            _make_path("_snapshot", repository, snapshot, "_status"),
            params=params,
            headers=headers,
        )

    @query_params("master_timeout", "timeout")
    def verify_repository(self, repository, params=None, headers=None):
        """
        Verifies a repository.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/modules-snapshots.html>`_

        :arg repository: A repository name
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        :arg timeout: Explicit operation timeout
        """
        if repository in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'repository'.")

        return self.transport.perform_request(
            "POST",
            _make_path("_snapshot", repository, "_verify"),
            params=params,
            headers=headers,
        )

    @query_params("master_timeout", "timeout")
    def cleanup_repository(self, repository, params=None, headers=None):
        """
        Removes stale data from repository.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/clean-up-snapshot-repo-api.html>`_

        :arg repository: A repository name
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        :arg timeout: Explicit operation timeout
        """
        if repository in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'repository'.")

        return self.transport.perform_request(
            "POST",
            _make_path("_snapshot", repository, "_cleanup"),
            params=params,
            headers=headers,
        )
