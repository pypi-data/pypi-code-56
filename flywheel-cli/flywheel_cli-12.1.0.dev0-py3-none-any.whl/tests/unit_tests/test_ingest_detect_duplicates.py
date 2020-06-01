"""Ingest DetectDuplicatesTask tests"""

from uuid import uuid4
from unittest import mock

from flywheel import Flywheel

from flywheel_cli.ingest import detect_duplicates, errors
from flywheel_cli.ingest import schemas as T
from flywheel_cli.ingest.client import db as db_client


# Item errors

def test_detect_study_instance_uid_conflicts_in_item_ok():
    """ one item, all uid@study_instance_uid is the same """
    item = T.ItemIn(
        id=uuid4(),
        dir="dir",
        type="file",
        files_cnt=2,
        bytes_sum=1,
        files=["file1", "file2"]
    )

    uids = [
        T.UIDIn(
            item_id=item.id,
            filename="file1",
            study_instance_uid="uid1",
            series_instance_uid="uid2",
            sop_instance_uid="uid3"
        ),
        T.UIDIn(
            item_id=item.id,
            filename="file2",
            study_instance_uid="uid1",
            series_instance_uid="uid2",
            sop_instance_uid="uid3"
        )
    ]

    insert_error = mock.Mock(spec=db_client.BatchWriter)

    ret = detect_duplicates.detect_uid_conflicts_in_item(item, uids, insert_error)

    assert ret

    insert_error.push.assert_not_called()


def test_detect_study_instance_uid_conflicts_in_item_error():
    """ one item, different uid@study_instance_uid """
    item = T.ItemIn(
        id=uuid4(),
        dir="dir",
        type="file",
        files_cnt=1,
        bytes_sum=1,
        files=["file1", "file2"]
    )

    uids = [
        T.UIDIn(
            item_id=item.id,
            filename="file1",
            study_instance_uid="uid",
            series_instance_uid="sid",
            sop_instance_uid="uid3"
        ),
        T.UIDIn(
            item_id=item.id,
            filename="file2",
            study_instance_uid="uid1",
            series_instance_uid="sid",
            sop_instance_uid="uid3"
        )
    ]

    insert_error = mock.Mock(spec=db_client.BatchWriter)

    ret = detect_duplicates.detect_uid_conflicts_in_item(item, uids, insert_error)

    assert not ret

    assert insert_error.push.call_count == 1
    insert_error.push.assert_called_once_with(
        {
            "item_id": item.id,
            "code": errors.DifferentStudyInstanceUID.code
        }
    )


def test_detect_series_instance_uid_conflicts_in_item_error():
    """ one item, same uid@series_instance_uid """
    item = T.ItemIn(
        id=uuid4(),
        dir="dir",
        type="file",
        files_cnt=1,
        bytes_sum=1,
        files=["file1", "file2"]
    )

    uids = [
        T.UIDIn(
            item_id=item.id,
            filename="file1",
            study_instance_uid="sid",
            series_instance_uid="uid",
            sop_instance_uid="uid3"
        ),
        T.UIDIn(
            item_id=item.id,
            filename="file2",
            study_instance_uid="sid",
            series_instance_uid="uid1",
            sop_instance_uid="uid3"
        )
    ]

    insert_error = mock.Mock(spec=db_client.BatchWriter)

    ret = detect_duplicates.detect_uid_conflicts_in_item(item, uids, insert_error)

    assert not ret

    assert insert_error.push.call_count == 1
    insert_error.push.assert_called_once_with(
        {
            "item_id": item.id,
            "code": errors.DifferentSeriesInstanceUID.code
        }
    )


def test_correct_sop_instace_uids(db):
    db.create_ingest()
    container1 = db.create_container(path="path", level=T.ContainerLevel.session, existing=False)
    container2 = db.create_container(path="path", level=T.ContainerLevel.session, existing=False)

    item1 = db.create_item(container_id=container1.id)
    create_uid(db, item_id=item1.id, sop_instance_uid="uid1", session_container_id=container1.id)
    create_uid(db, item_id=item1.id, sop_instance_uid="uid2", session_container_id=container1.id)
    create_uid(db, item_id=item1.id, sop_instance_uid="uid3", session_container_id=container1.id)

    item2 = db.create_item(container_id=container2.id)
    create_uid(db, item_id=item2.id, sop_instance_uid="uid4", session_container_id=container2.id)
    create_uid(db, item_id=item2.id, sop_instance_uid="uid5", session_container_id=container2.id)
    create_uid(db, item_id=item2.id, sop_instance_uid="uid6", session_container_id=container2.id)


    item_ids = db.client.duplicated_sop_instance_uid_item_ids()
    assert len(item_ids) == 0


def test_duplicated_sop_instace_uids(db):
    db.create_ingest()
    container1 = db.create_container(path="path", level=T.ContainerLevel.session, existing=False)
    container2 = db.create_container(path="path", level=T.ContainerLevel.session, existing=False)

    item1 = db.create_item(container_id=container1.id)
    create_uid(db, item_id=item1.id, sop_instance_uid="uid1", session_container_id=container1.id)
    create_uid(db, item_id=item1.id, sop_instance_uid="uid2", session_container_id=container1.id)
    create_uid(db, item_id=item1.id, sop_instance_uid="uid3", session_container_id=container1.id)

    item2 = db.create_item(container_id=container2.id)
    create_uid(db, item_id=item2.id, sop_instance_uid="uid1", session_container_id=container2.id)
    create_uid(db, item_id=item2.id, sop_instance_uid="uid5", session_container_id=container2.id)
    create_uid(db, item_id=item2.id, sop_instance_uid="uid6", session_container_id=container2.id)


    item_ids = db.client.duplicated_sop_instance_uid_item_ids()
    assert set(item_ids) == set([item1.id, item2.id])


def create_uid(db, **kwargs):
    kwargs.setdefault("study_instance_uid", str(uuid4()))
    kwargs.setdefault("series_instance_uid", str(uuid4()))
    kwargs.setdefault("sop_instance_uid", str(uuid4()))
    kwargs.setdefault("filename", "file1")

    return db.create_uid(**kwargs)
