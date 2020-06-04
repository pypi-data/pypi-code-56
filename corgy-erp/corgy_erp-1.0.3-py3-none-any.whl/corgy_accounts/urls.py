from django.conf.urls import url
from django.views import generic
from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    url('^$', generic.RedirectView.as_view(url='./accountmodel/'), name="index"),
    url('^accountmodel/', include(views.AccountModelViewSet().urls)),
    path('', generic.TemplateView.as_view(template_name="corgy_accounts/index.html"), name="index"),

    path('api/', include(router.urls)),
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>/', views.snippet_detail),

]