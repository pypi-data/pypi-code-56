# pylint: disable=no-self-use
import logging

from flask import request
from flask_restplus import Namespace, Resource, inputs, abort
from flask_restplus.reqparse import RequestParser
from spectacular import FailedToValidate

from airflow import settings
from airflow.models import DAG
from shu.interactions import Interactions, InteractionError, NotFound
from shu.wrappers import DagRunWrapper
from shu.adapters import create_adapters


dags = Namespace("dags")
log = logging.getLogger(__name__)


class Parser:
    @staticmethod
    def get_dag_collection():
        parser = RequestParser()
        parser.add_argument("prefix", type=str, required=False)
        parser.add_argument("is_active", type=inputs.boolean)
        return parser

    @staticmethod
    def get_dag_run_collection():
        parser = RequestParser()
        parser.add_argument("prefix", type=str, required=False)
        parser.add_argument("state", type=str, required=False)
        return parser


def interactions():
    adapters = create_adapters(settings.Session())
    return Interactions(adapters)


@dags.route("")
class DagCollection(Resource):
    @dags.expect(Parser.get_dag_collection())
    def get(self):
        """List DAGs"""
        try:
            arguments = Parser.get_dag_collection().parse_args()
            return interactions().find_dags(arguments).to_dict()
        except (InteractionError, FailedToValidate) as exc:
            abort(400, error=exc.to_dict())


@dags.route("/<string:dag_id>/runs")
class DagRunCollection(Resource):
    @dags.expect(dags.schema_model("DagRun", DagRunWrapper.schema(ignored=["dag_id"])))
    def post(self, dag_id):
        try:
            return interactions().create_dag_run(dag_id, request.json).to_dict()
        except (InteractionError, FailedToValidate) as exc:
            abort(400, error=exc.to_dict())

    @dags.expect(Parser.get_dag_run_collection())
    def get(self, dag_id):
        """List DAG runs"""
        try:
            return interactions().find_dag_run(dag_id, request.args).to_dict()
        except NotFound as exc:
            if exc.cls == DAG:
                abort(404, error=exc.to_dict())
        except (InteractionError, FailedToValidate) as exc:
            abort(400, error=exc.to_dict())


@dags.errorhandler
def default_error_handler(error):
    log.info(error)
