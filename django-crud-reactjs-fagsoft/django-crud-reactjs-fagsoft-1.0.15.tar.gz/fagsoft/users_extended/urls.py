from rest_framework import routers
from fagsoft.users_extended.views import (
    UserViewSet,
    LoginViewSet
)

router = routers.DefaultRouter()
router.register(r'authentication', LoginViewSet)
router.register(r'users', UserViewSet)
