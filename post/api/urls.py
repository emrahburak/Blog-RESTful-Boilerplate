
from django.urls import path, include
from post.api.views import (PostListApiView,
                            PostDetailApiView,
                            PostDeleteApiView,
                            PostUpdateApiView,
                            PostCreateApiView
                            )

app_name= 'post'

urlpatterns = [

    path('list', PostListApiView.as_view(), name='list'),
    path('detail/<slug>', PostDetailApiView.as_view(), name='detail'),
    path('delete/<slug>', PostDeleteApiView.as_view(), name='delete'),
    path('update/<slug>', PostUpdateApiView.as_view(), name='update'),
    path('create/', PostCreateApiView.as_view(), name='create')
]
