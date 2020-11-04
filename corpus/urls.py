
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from corpus import views


# Create a router and register our viewsets with it

router = DefaultRouter()

router.register(r'corpus', views.CorpusViewSet)
router.register(r'users', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),

    ]


#corpus_list = views.CorpusViewSet.as_view({
#    'get':'list',
#    'post':'create'
#
#    })
#
#corpus_detail = views.CorpusViewSet.as_view({
#    'get': 'retrieve',
#    'put': 'update',
#    'patch': 'partial_update',
#    'delete': 'destroy'
#    })
#
#user_list = views.UserViewSet.as_view({
#    'get': 'list'
#
#    })
#
#user_detail = views.UserViewSet.as_view({
#    'get': 'retrieve'
#
#    })
#
#urlpatterns = [
#    path('', views.api_root),
#    path('corpus/', corpus_list, name='corpus-list'),
#    path('corpus/<slug>', corpus_detail, name='corpus-detail'),
#    path('users/', user_list, name='user-list'),
#    path('users/<int:pk>', user_detail, name='user-detail')
#
#    ]



#urlpatterns = [
#    path('', views.api_root),
#    path('corpus/',views.CorpusList.as_view(),
#         name='corpus-list'),
#    path('corpus/<slug>', views.CorpusDetail.as_view(),
#         name='corpus-detail'),
#    path('users/', views.UserList.as_view(),
#         name='user-list'),
#    path('users/<int:pk>', views.UserDetail.as_view(),
#         name='user-detail')
#    ]

#urlpatterns = format_suffix_patterns(urlpatterns)
