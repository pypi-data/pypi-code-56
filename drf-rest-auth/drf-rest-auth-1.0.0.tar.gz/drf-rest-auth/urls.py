"""
# Copyright © Nico Huebschmann
# Licensed under the terms of the MIT License
"""

from django.urls import path

from rest_framework import routers
from rest_framework_jwt.views import refresh_jwt_token

from .views import AuthViewSet

router = routers.DefaultRouter()
router.register('', AuthViewSet, basename='drf-rest-auth')

urlpatterns = router.urls + [
    path('refresh-token/', refresh_jwt_token, name='refresh-token'),
]
