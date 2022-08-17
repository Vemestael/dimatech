from django.urls import path, include
from rest_framework import routers

from main import views

router = routers.DefaultRouter()
urlpatterns = router.urls
