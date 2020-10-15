
from rest_framework.generics import (ListAPIView,
                                     RetrieveAPIView,
                                     UpdateAPIView,
                                     DestroyAPIView,
                                     CreateAPIView)
                                     
from post.models import Post
from post.api.serializers import PostSerializer


class PostListApiView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer



class PostDetailApiView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'


class PostDeleteApiView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'


class PostUpdateApiView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'


class PostCreateApiView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer



    
