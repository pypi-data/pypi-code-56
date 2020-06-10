from mailchimp3 import MailChimp

from .batch_operations import BatchOperations


class Batch:
    def __init__(self):
        self.operations = []
        self._run = False
        self._mc_client = None
        self.id = None

    def __repr__(self):
        return '<{}.{}: {} operation{}{}>'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            len(self.operations),
            's' if len(self.operations) != 1 else '',
            '*' if not self._run else '',
        )

    def status(self, **kwargs):
        if not self._mc_client:
            return {'status': 'not started'}
        return self._mc_client.batch_operations.get(self, **kwargs)

    def run(self, client=None):
        if client:
            self._mc_client = client
        if not self._mc_client:
            raise Exception('No MailChimp client specified.')
        return self._mc_client.batch_operations.create(self)

    def delete(self):
        if not self._mc_client:
            raise Exception('No MailChimp client specified.')
        return self._mc_client.batch_operations.delete(self)


class BatchMailChimp(MailChimp):
    def __init__(self, *args, **kwargs):
        super(BatchMailChimp, self).__init__(*args, **kwargs)
        # Batch Operations
        self.batches = self.batch_operations = BatchOperations(self)

    def _post(self, url, data=None, batch=None):
        if batch:
            if not batch._mc_client:
                batch._mc_client = self
            batch.operations.append(dict(
                method='POST',
                path=url,
                body=data,
            ))
            return batch
        return super(BatchMailChimp, self)._post(url, data=data)

    def _get(self, url, batch=None, **queryparams):
        if batch:
            if not batch._mc_client:
                batch._mc_client = self
            batch.operations.append(dict(
                method='GET',
                path=url,
                params=queryparams,
            ))
            return batch
        return super(BatchMailChimp, self)._get(url, **queryparams)

    def _delete(self, url, batch=None):
        if batch:
            if not batch._mc_client:
                batch._mc_client = self
            batch.operations.append(dict(
                method='DELETE',
                path=url,
            ))
            return batch
        return super(BatchMailChimp, self)._delete(url)

    def _patch(self, url, data=None, batch=None):
        if batch:
            if not batch._mc_client:
                batch._mc_client = self
            batch.operations.append(dict(
                method='PATCH',
                path=url,
                body=data,
            ))
            return batch
        return super(BatchMailChimp, self)._patch(url, data=data)

    def _put(self, url, data=None, batch=None):
        if batch:
            if not batch._mc_client:
                batch._mc_client = self
            batch.operations.append(dict(
                method='PUT',
                path=url,
                body=data,
            ))
            return batch
        return super(BatchMailChimp, self)._put(url, data=data)
