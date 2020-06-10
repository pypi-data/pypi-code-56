from mailchimp3.entities.batchoperations import \
    BatchOperations as OriginalBatchOperations


class BatchOperations(OriginalBatchOperations):
    def create(self, data):
        if type(data) is dict:
            batch = None
            return super(BatchOperations, self).create(data)
        batch = data
        if batch._run:
            raise Exception('That batch has already been created.')
        batch._mc_client = self._mc_client
        data = {
            'operations': batch.operations,
        }
        resp = super(BatchOperations, self).create(data)
        batch.id = resp.get('id')
        batch._run = True
        batch._status = 'started'
        return batch

    def get(self, batch_id, **queryparams):
        if type(batch_id) is not str:
            batch = batch_id
            if not batch._mc_client:
                batch._mc_client = self._mc_client
            if not batch._run:
                return {'status': 'not started'}
            batch_id = batch.id
        return super(BatchOperations, self).get(batch_id, **queryparams)

    def delete(self, batch_id):
        if type(batch_id) is not str:
            batch = batch_id
            if not batch._mc_client:
                batch._mc_client = self._mc_client
            if not batch._run:
                raise Exception('That batch hasn\'t been created yet.')
            batch_id = batch.id
        return super(BatchOperations, self).delete(batch_id)
