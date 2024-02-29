from .views import *
from django.urls import path
from rest_framework import routers
from django.http import HttpResponse
import socket

router = routers.DefaultRouter()
router.get_api_root_view().cls.__doc__ = "This is running on host: " + str(socket.gethostname())

router.register('users', UserViewSet, 'users')

urlpatterns = router.urls