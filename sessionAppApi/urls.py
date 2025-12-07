from rest_framework.routers import DefaultRouter
from .views import SessionViewSet
from django.urls import path ,include
router = DefaultRouter()
router.register('session',SessionViewSet)
urlpatterns=[
    path('',include(router.urls))

]