from InMemoryCloudDatastoreStub import datastore_stub
from tests.models import SimpleModel


def test_get_or_insert_existing_by_id(
    ndb_stub: datastore_stub.LocalDatastoreStub,
) -> None:
    model = SimpleModel(id="test", str_prop="asdf",)
    ndb_stub._insert_model(model)

    model_res = SimpleModel.get_or_insert("test")
    assert model_res == model


def test_get_or_insert_doesnt_exist() -> None:
    model_res = SimpleModel.get_or_insert("test")
    assert model_res is not None
