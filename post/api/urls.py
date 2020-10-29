
from django.urls import path, include
from django.views.decorators.cache import cache_page

from post.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'users', views.UserViewSet)


app_name = "post"
urlpatterns = [
    path('', include(router.urls)),

    ]

