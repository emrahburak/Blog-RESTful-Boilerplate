
from rest_framework import serializers
from post.models import Post
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.HyperlinkedRelatedField(many=True,
                                                view_name='post-detail',
                                                read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'posts')


class PostSerializer(serializers.HyperlinkedModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(
        view_name = 'post-slug',

        )

    class Meta:
        model = Post
        fields = (
            'url',
            'id',
            'highlight',
            'owner',
            'title',
            'content',
            'image',
            'created',
            'modified_by'
            )


class PostUpdateCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'title',
            'content',
            'image'
            )

            

    

