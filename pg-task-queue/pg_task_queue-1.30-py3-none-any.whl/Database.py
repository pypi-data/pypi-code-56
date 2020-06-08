import datetime
import socket
import json
from pg_tasks_queue.Config import cfg as config

from sqlalchemy import create_engine
from sqlalchemy import schema as sqlalchemy_schema
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, Text, VARCHAR)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
# from sqlalchemy_utils import database_exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import and_
from sqlalchemy import or_
# from sqlalchemy.ext.declarative import declared_attr
# from sqlalchemy import MetaData


import logging
logger = logging.getLogger(__name__)

# config.set_config_dir(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'conf'))

database_cfg = None
db_engine = None
session = None
db_schema = None
project = None

# database_cfg = config.cfg.get('database')
# if isinstance(database_cfg, dict):
#     db_schema = database_cfg.get('schema')


def get_repr(_class):
    repr = f'<{_class.__class__.__name__}('
    for i in range(len(_class.__table__.columns)):
        column = list(_class.__table__.columns)[i]
        val = getattr(_class, column.name)
        repr += f'{column.name}={val}'
        if i < len(_class.__table__.columns) - 1:
            repr += ', '
    repr += ')>'
    return repr


# # https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/mixins.html
# class Base(object):
#     _schema = None
#     # if db_schema:
#     #     _schema = db_schema
#
#     @declared_attr
#     def __table_args__(cls):
#         args = dict()
#         if cls._schema:
#             args.update({'schema': cls._schema})
#         print(f'CronjobTask: args: {args}')
#         return args
# Base = declarative_base(cls=Base)
# Base._schema = db_schema
# Base = declarative_base(metadata=MetaData(schema=db_schema))

Base = declarative_base()


class CronjobTask(Base):
    __tablename__ = 'cronjob'
    # if db_schema:
    #     __table_args__ = {'schema': db_schema}

    task_id = Column(Integer, primary_key=True)
    module = Column(VARCHAR, nullable=False)
    func = Column(VARCHAR, nullable=False)
    params = Column(JSONB)
    project = Column(VARCHAR)
    max_retry_count = Column(Integer)
    schedule = Column(VARCHAR)
    enabled = Column(Boolean)
    last_start_time = Column(DateTime)
    next_start_time = Column(DateTime)

    def __repr__(self):
        return get_repr(self)


class Worker(Base):
    __tablename__ = 'worker'

    worker_id = Column(Integer, primary_key=True)
    project = Column(VARCHAR)
    host = Column(VARCHAR)
    status = Column(VARCHAR)
    started_time = Column(DateTime)
    finished_time = Column(DateTime)
    success_tasks = Column(Text)
    failed_tasks = Column(Text)
    current_task_id = Column(Integer)
    error = Column(Text)

    def __repr__(self):
        return get_repr(self)


class Task(Base):
    __tablename__ = 'task'

    task_id = Column(Integer, primary_key=True)
    module = Column(VARCHAR, nullable=False)
    func = Column(VARCHAR, nullable=False)
    params = Column(JSONB)
    project = Column(VARCHAR)
    result = Column(Text)
    status = Column(VARCHAR)
    retry_count = Column(Integer)
    max_retry_count = Column(Integer)
    scheduled_time = Column(DateTime)
    defer_time = Column(DateTime)
    create_time = Column(DateTime)
    started_time = Column(DateTime)
    finished_time = Column(DateTime)
    priority = Column(Integer)
    worker_host = Column(VARCHAR)
    failed_email = Column(VARCHAR)
    success_email = Column(VARCHAR)
    parent_task_id = Column(Integer)
    cronjob_task_id = Column(Integer, ForeignKey(CronjobTask.task_id))
    worker_id = Column(Integer, ForeignKey(Worker.worker_id))

    cronjob_task = relationship("CronjobTask")
    worker = relationship("Worker")

    def __repr__(self):
        return get_repr(self)


class Config(Base):

    __tablename__ = 'config'

    config_id = Column(Integer, primary_key=True)
    config = Column(JSONB)

    def __repr__(self):
        return get_repr(self)

# ======================================================================================================================


def get_connection_string():
    host = database_cfg.get('host')
    if host is None:
        logger.error(f"Error in Database.get_connection_string(): host is None...")
        return None
    dbname = database_cfg.get('dbname')
    if dbname is None:
        logger.error(f"Error in Database.get_connection_string(): dbname is None...")
        return None
    user = database_cfg.get('user')
    if user is None:
        logger.error(f"Error in Database.get_connection_string(): user is None...")
        return None
    password = database_cfg.get('password')
    if password is None:
        logger.error(f"Error in Database.get_connection_string(): password is None...")
        return None
    port = database_cfg.get('port')

    schema = database_cfg.get('schema')
    if schema is None:
        logger.error(f"Error in Database.get_connection_string(): schema is None...")
        return None
    if port:
        connection_string = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}'
    else:
        connection_string = f'postgresql+psycopg2://{user}:{password}@{host}/{dbname}'
    return connection_string


def init(cfg=None, use_project=True, create=True):

    if cfg is None:
        if not isinstance(config.cfg, dict):
            logger.error(f"Error in Database.init(): not isinstance(config.cfg, dict)...")
            return False
        cfg = config.cfg.get('database')
    global database_cfg
    database_cfg = cfg

    if not isinstance(database_cfg, dict):
        logger.error(f'Error in Database.init(): not isinstance(database_cfg, dict)...')
        return False

    if use_project:
        global project
        project = database_cfg.get('project')
        if not isinstance(project, str):
            logger.error(f'Error in Database.init(): not isinstance(project, str)...')
            return False

    global db_schema
    db_schema = database_cfg.get('schema')
    if not isinstance(db_schema, str):
        logger.error(f'Error in Database.init(): not isinstance(db_schema, str)...')
        return False

    connection_string = get_connection_string()
    if connection_string is None:
        logger.error(f"Error in Database.init(): connection_string is None...")
        return False

    # if not database_exists(connection_string):
    #     logger.error(f"Error in Database.init(): database '{database_cfg.get('dbname')}' not exists ...")
    #     return False

    global db_engine
    # connect_args = {'options': f'-csearch_path={db_schema}'}
    # db_engine = create_engine(connection_string, echo=database_cfg.get('echo', False), connect_args=connect_args)
    db_engine = create_engine(connection_string, echo=database_cfg.get('echo', False))

    if not db_engine.dialect.has_schema(db_engine, db_schema):
        if not create:
            logger.error(f"Error in Database.init(): schema '{db_schema}' not exists in database "
                         f"'{database_cfg.get('dbname')}'...")
            return False
        logger.warning(f"Try to create schema '{db_schema}' for database {database_cfg.get('dbname')}'...")
        db_engine.execute(sqlalchemy_schema.CreateSchema(db_schema))
        if not db_engine.dialect.has_schema(db_engine, db_schema):
            logger.error(f"Error in Database.init(): schema '{db_schema}' not exists in database "
                         f"'{database_cfg.get('dbname')}'...")
            return False
        logger.warning(f"Schema '{db_schema}' created successfully...")

    global Base
    # Base.metadata.schema = db_schema
    for table_name in Base.metadata.tables:
        Base.metadata.tables[table_name].schema = db_schema

    if create:
        Base.metadata.create_all(db_engine)

    return True


def get_table_columns(_table):
    columns = dict()
    for column in _table.__table__.columns:
        columns[column.name] = column.type.python_type.__name__
    return columns


def update_elem(elem, **kwargs):
    for key, value in kwargs.items():
        if hasattr(elem, key):
            setattr(elem, key, value)


def get_record_dict(_record):
    _dict = dict()
    for column in _record.__table__.columns:
        _dict[column.name] = getattr(_record, column.name)
    return _dict


def get_html_table(query_list, columns=None, table=None):
    if len(query_list) == 0:
        if table is None:
            return None
        types = get_table_columns(table)
    else:
        types = get_table_columns(query_list[0])
    if columns is None:
        columns = list(types.keys())
    else:
        keys = list(types.keys())
        for key in keys:
            if key not in columns:
               del types[key]

    values = list()
    for row in query_list:
        row_dict = dict()
        for column in columns:
            value = getattr(row, column)
            value_type = types.get(column)
            if value_type == 'datetime' and value is not None:
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            row_dict[column] = value
        values.append(row_dict)
    return {'columns': columns, 'values': values, 'types': types}


def get_session(autocommit=False):
    global session
    if session is None:
        if db_engine is None:
            logger.error(f'Error in Database.get_session(): db_engine is None...')
            return False
        try:
            Session = sessionmaker(bind=db_engine)
            session = Session()
        except Exception as e:
            logger.exception(f'Exception in Database.get_session(): {type(e)}: {str(e)}...')
            session = None
    if session is None:
        logger.error(f'Error in Database.get_session(): session is None...')
        return False
    session.autocommit = autocommit
    return True


def close_session():
    global session
    try:
        if session is not None:
            session.close()
    except Exception as e:
        logger.exception(f'Exception in Database.close_session(): {type(e)}: {str(e)}...')
    finally:
        session = None


def get_table(_value, _class):
    if isinstance(_value, dict):
        _value = _class(**_value)
    return _value


def add_common_columns(_value):
    if 'project' in _value.__table__.columns:
        if _value.project is None:
            _value.project = project
    if 'params' in _value.__table__.columns:
        if _value.params is None:
            _value.params = dict()
    if 'create_time' in _value.__table__.columns:
        if _value.create_time is None:
            _value.create_time = datetime.datetime.now()
    return _value


def add_new_record(_add_value, _class, func=None):
    if session is None:
        error = f'Error in Database.add_new_record(): session is None...'
        logger.error(error)
        return error
    _add_value = get_table(_add_value, _class)
    if not isinstance(_add_value, _class):
        error = f'Error in Database.add_new_record(): not isinstance(_add_value, {_class.__class__.__name__})...'
        logger.error(error)
        return error
    if func is not None:
        _add_value.module = func.__module__
        _add_value.func = func.__name__

    session.add(add_common_columns(_add_value))
    session.commit()
    return _add_value


def add_cornjob_task(_add_value, func=None, commit=True):
    return add_new_record(_add_value, CronjobTask, func=func)


def add_task(_add_value, func=None):
    return add_new_record(_add_value, Task, func=func)


def get_new_worker():
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    host = f'{host_ip} : {host_name}'
    started_time = datetime.datetime.now()
    success_tasks = json.dumps(list())
    failed_tasks = json.dumps(list())
    new_worker = Worker(host=host, status='working', started_time=started_time,
                        success_tasks=success_tasks, failed_tasks=failed_tasks)
    return add_new_record(new_worker, Worker)


def get_new_task(worker=None):
    if session is None:
        error = f'Error in Database.get_new_task(): session is None...'
        logger.error(error)
        return error

    # 1. status is null and scheduled_time <= NOW()
    filter_value = and_(Task.status.is_(None),
                        Task.scheduled_time.isnot(None),
                        Task.scheduled_time <= datetime.datetime.now())
    if project:
        filter_value = and_(filter_value, Task.project == project)
    task = session.query(Task).with_for_update(skip_locked=True).filter(filter_value).order_by(
        Task.scheduled_time.asc(), Task.priority.desc()).first()

    if task is None:
        # 2. status = 'error' max_retry_count > retry_count
        filter_value = and_(Task.status == 'error',
                            or_(Task.retry_count.is_(None), Task.max_retry_count > Task.retry_count))
        if project:
            filter_value = and_(filter_value, Task.project == project)
        task = session.query(Task).with_for_update(skip_locked=True).filter(filter_value).order_by(
            Task.finished_time.asc(), Task.priority.desc()).first()

    if task is None:
        # 3. Simple Tasks
        filter_value = and_(Task.status.is_(None), Task.scheduled_time.is_(None))
        if project:
            filter_value = and_(filter_value, Task.project == project)
        task = session.query(Task).with_for_update(skip_locked=True).filter(filter_value).order_by(
            Task.priority.desc(), Task.task_id.asc()).first()

    if task is not None:
        if worker is None:
            host_name = socket.gethostname()
            host_ip = socket.gethostbyname(host_name)
            task.worker_host = f'{host_ip} : {host_name}'
        else:
            task.worker_host = worker.host
            task.worker_id = worker.worker_id
            worker.current_task_id = task.task_id
        task.started_time = datetime.datetime.now()
        task.status = 'working'

    session.commit()
    return task


def get_new_tasks(task_limit, worker=None):
    if session is None:
        error = f'Error in Database.get_new_task(): session is None...'
        logger.error(error)
        return error

    # 1. status is null and scheduled_time <= NOW()
    filter_value_1 = and_(Task.status.is_(None),
                          Task.scheduled_time.isnot(None),
                          Task.scheduled_time <= datetime.datetime.now())

    # 2. status = 'error' max_retry_count > retry_count
    filter_value_2 = and_(Task.status == 'error',
                          or_(Task.retry_count.is_(None), Task.max_retry_count > Task.retry_count))

    # 3. Simple Tasks
    filter_value_3 = and_(Task.status.is_(None), Task.scheduled_time.is_(None))

    filter_value = or_(filter_value_1, filter_value_2, filter_value_3)

    if project:
        filter_value = and_(filter_value, Task.project == project)

    query = session.query(Task).with_for_update(skip_locked=True).filter(filter_value).order_by(
        Task.task_id.asc()).limit(task_limit)

    tasks = query.all()
    for task in tasks:
        if worker is None:
            host_name = socket.gethostname()
            host_ip = socket.gethostbyname(host_name)
            task.worker_host = f'{host_ip} : {host_name}'
        else:
            task.worker_host = worker.host
            task.worker_id = worker.worker_id
            # worker.current_task_id = task.task_id
        # task.started_time = datetime.datetime.now()
        task.status = 'working'

    session.commit()
    return tasks


def update_worker_task(_result, task, worker):
    if session is None:
        error = f'Error in Database.update_worker_task(): session is None...'
        logger.error(error)
        return error

    finished_time = datetime.datetime.now()
    error = None
    if isinstance(_result, dict):
        status = _result.get('status')
        result = _result.get('result', '')
        if not isinstance(status, str):
            error = f'Error in Database.update_worker_task(): not isinstance(status, strt)...'
            logger.error(error)
        elif status == 'error':
            error = result
    else:
        status = 'finished'
        result = _result

    if error is not None:
        task.status = 'error'
        task.result = error

        max_retry_count = task.max_retry_count
        max_retry_count = 0 if max_retry_count is None else max_retry_count
        if max_retry_count > 0:
            retry_count = task.retry_count
            retry_count = 0 if retry_count is None else retry_count
            task.retry_count = retry_count + 1

        if worker:
            failed_tasks = json.loads(worker.failed_tasks)
            failed_tasks.append(task.task_id)
            worker.failed_tasks = json.dumps(failed_tasks)

    else:
        task.status = status
        task.result = result

        if worker:
            success_tasks = json.loads(worker.success_tasks)
            success_tasks.append(task.task_id)
            worker.success_tasks = json.dumps(success_tasks)

    if worker:
        worker.current_task_id = None

    task.finished_time = finished_time
    session.commit()

    return None


def set_worker_error(error, worker, task):
    if session is None:
        error = f'Error in Database.set_worker_error(): session is None...'
        logger.error(error)
        return error

    finished_time = datetime.datetime.now()

    if task:
        task.status = 'error'
        task.result = error
        task.finished_time = finished_time

        max_retry_count = task.max_retry_count
        max_retry_count = 0 if max_retry_count is None else max_retry_count
        if max_retry_count > 0:
            retry_count = task.retry_count
            retry_count = 0 if retry_count is None else retry_count
            task.retry_count = retry_count + 1

        failed_tasks = json.loads(worker.failed_tasks)
        failed_tasks.append(task.task_id)
        worker.failed_tasks = json.dumps(failed_tasks)

    worker.status = 'error'
    worker.error = error
    worker.finished_time = finished_time

    session.commit()

# ======================================================================================================================


if __name__ == '__main__':
    name = 'Database'
    ver = '1.2'
    release_date = '2020-06-05 10:00'
    version = f'{name}. ver: {ver} ({release_date})'
    from pg_tasks_queue.Logging import init_logger
    init_logger()
    logger.warning(version)

    cfg = config.cfg.get('database')

    if not init(cfg):
        logger.warning(f"not init()")
    else:
        if not get_session():
            logger.warning(f"not get_session()")
        else:
            # get_new_task()

            new_cornjob_task = {'schedule': '*/1 * * * *',
                                'module': 'Modules.TestTasks',
                                'func': 'raise_exception',  # raise_exception, sleep_false, sleep
                                'params': {"counter": 4},
                                'project': 'project_2',
                                'max_retry_count': 2,
                                'enabled': True}
            # new_cornjob_task = CronjobTask(**new_cornjob_task)
            # from Modules import TestTasks
            # new_cornjob_task = add_cornjob_task(new_cornjob_task, TestTasks.raise_exception)
            new_cornjob_task = add_cornjob_task(new_cornjob_task)
            print(f'new_cornjob_task: {new_cornjob_task}')

            import datetime
            new_task = {'module': 'Modules.TestTasks',
                        'func': 'raise_exception',
                        'params': {"counter": 4},
                        'max_retry_count': 20,
                        'scheduled_time': datetime.datetime.now(),
                        'priority': 1}
            new_task = add_task(new_task)
            print(f'new_task: {new_task}')

            close_session()
