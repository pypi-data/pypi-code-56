import os
from typing import Callable, Dict, List

from expiring_dict import ExpiringDict
from jinja2 import FileSystemLoader
from passlib.hash import pbkdf2_sha256
from pydantic import BaseConfig, BaseModel, validator
from sanic.response import html
from sanic_jinja2 import SanicJinja2

__version__ = "0.0.11(master)"


loader = FileSystemLoader(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
)


def render_with_updated_context(self):
    def render_with_updated_context_logic(
        template, request, status=200, headers=None, **context
    ):
        context["admin_panel_title"] = cfg.name
        context["objects"] = cfg.models
        context["url_prefix"] = cfg.route
        context["admin_panel_version"] = __version__
        context["round_number"] = cfg.round_number
        return html(
            self.render_string(template, request, **context),
            status=status,
            headers=headers,
        )

    return render_with_updated_context_logic


jinja = SanicJinja2(loader=loader)

jinja.render = render_with_updated_context(jinja)


class CompositeCsvSettings(BaseModel):
    ...
    # todo


class App:
    """ class to store links to main app data app.config and DB"""

    config = {}
    db = None


class Config(BaseModel):
    """ Gino Admin Panel settings """

    route: str = "/admin"
    jinja: SanicJinja2 = None
    app: App = App
    hash_method: Callable = pbkdf2_sha256.encrypt
    models: Dict = {}
    sessions: Dict = {}
    # upload from csv config
    upload_dir: str = "files/"
    max_file_size: int = 10485760
    allowed_file_types: List[str] = ["csv"]
    datetime_str_formats: List[str] = [
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%m-%d-%yT%H:%M:%S.%f",
        "%m-%d-%y %H:%M:%S",
        "%m-%d-%yT%H:%M:%S",
    ]
    presets_folder: str = "presets"
    presets: Dict = {}
    composite_csv_settings: Dict = {}
    history_table_name: str = "gino_admin_history"
    admin_users_table_name: str = "gino_admin_users"
    admin_roles_table_name: str = "gino_admin_roles"
    name: str = "Sanic-Gino Admin Panel"
    csv_update_existed: bool = True
    debug: bool = True
    displayable_setting: list = [
        "debug",
        "presets_folder",
        "composite_csv_settings",
        "name",
        "csv_update_existed",
    ]
    round_number: float = 3

    @validator("displayable_setting")
    def displayable_setting_cannot_be_changed(cls, value):
        return ["presets_folder", "composite_csv_settings", "name"]

    class Config(BaseConfig):
        arbitrary_types_allowed = True


# instance of config on current run
cfg = Config()
cfg.sessions = ExpiringDict(ttl=3600)
cfg.jinja = jinja
