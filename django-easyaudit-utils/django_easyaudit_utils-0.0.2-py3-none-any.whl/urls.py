# from django.urls import path
from cbs.apps.core.urls import path
from . import views

app_name = "easyaudit_utils"
urlpatterns = [
    path("events/index/", views.IndexView.as_view(), name="index", verbose_name="AUDIT INDEX"),
    path(
        "events/crud/list/",
        views.CRUDEventListView.as_view(),
        name="crud_event_list",
        verbose_name="AUDIT CRUD EVENT LIST",
    ),
    path(
        "events/login/list/",
        views.LoginEventListView.as_view(),
        name="login_event_list",
        verbose_name="AUDIT LOGIN EVENT LIST",
    ),
    path(
        "events/request/list/",
        views.RequestEventListView.as_view(),
        name="request_event_list",
        verbose_name="AUDIT REQUEST EVENT LIST",
    ),
]
