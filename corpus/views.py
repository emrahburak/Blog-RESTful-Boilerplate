

from django.contrib.auth.models import User
from corpus.models import Corpus
from corpus.serializers import CorpusSerializer, UserSerializer
from corpus.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django_filters import FilterSet
from django_filters import rest_framework as filters



class OwnerUsernameFilter(FilterSet):
    """
    Custom Filter for owner.username
    """

    username = filters.CharFilter('owner__username')


    class Meta:
        model = Corpus
        fields = ('username',)



class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    automaticli provide 'list and 'detail' ancitions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,SearchFilter)
    filter_fields = ('username',)
    search_fields = ('username',)
    ordering = ['username']


class CorpusViewSet(viewsets.ModelViewSet):

    """
       This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Corpus.objects.all()
    serializer_class = CorpusSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend,SearchFilter)
    filter_class = OwnerUsernameFilter
    search_fields = ('owner__username',)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
