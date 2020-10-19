

from post.models import Post
from post.api.permissions import IsOwner #custom permissions
from post.api.paginations import PostPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from post.api.serializers import (PostSerializer,
                                  PostUpdateCreateSerializer)
from rest_framework.generics import (ListAPIView,
                                     RetrieveAPIView,
                                     RetrieveUpdateAPIView,
                                     DestroyAPIView,
                                     CreateAPIView)



class PostListApiView(ListAPIView):
    serializer_class = PostSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title','content')
    pagination_class = PostPagination


    def get_queryset(self):
        queryset = Post.objects.filter(draft=False).order_by('-created')
        return queryset



class PostDetailApiView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'


class PostDeleteApiView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwner]


class PostUpdateApiView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateCreateSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwner]


    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class PostCreateApiView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateCreateSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



    
