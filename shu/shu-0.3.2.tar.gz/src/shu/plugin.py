# This is the class you derive to create a plugin
import os
from airflow.plugins_manager import AirflowPlugin


# NOTE: This is necessary to make shu testable. The plugin mechanism import this
# module whenever airflow is imported. The effect is a loop in the import
# dependencies. Setting the environment variable 'TEST_SHU' avoids this loop.
if "TEST_SHU" not in os.environ:
    import logging

    import airflow.www.app as www
    import airflow.www_rbac.app as www_rbac

    from shu.api import create_api, create_swagger
    from shu.resources import dags

    log = logging.getLogger(__name__)

    def create_blueprints():
        api = create_api("internal")
        api.add_namespace(dags)
        swagger = create_swagger()
        blueprints = [api.blueprint, swagger]
        for bp in blueprints:
            www.csrf.exempt(bp)
            www_rbac.csrf.exempt(api.blueprint)
        return blueprints

    class Plugin(AirflowPlugin):
        name = "internal"
        operators = []
        sensors = []
        hooks = []
        executors = []
        macros = []
        admin_views = []
        flask_blueprints = create_blueprints()
        menu_links = []
        appbuilder_views = []
        appbuilder_menu_items = []
        global_operator_extra_links = []


else:

    class Plugin(AirflowPlugin):
        name = "test"
        operators = []
        sensors = []
        hooks = []
        executors = []
        macros = []
        admin_views = []
        flask_blueprints = []
        menu_links = []
        appbuilder_views = []
        appbuilder_menu_items = []
        global_operator_extra_links = []
