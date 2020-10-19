from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Post


class BasicTest(TestCase):

    def setUp(self):
        self.post = Post()
        self.post.user = User(username='testAlpha',password='011305006a')
        self.post.title = 'I am a title'
        self.post.created = timezone.now()
        self.post.save()

    def test_fields(self):
        post = Post()
        post.user = 'Alex'
        post.title = 'make more test'
        post.created = timezone.now()
        post.save()


        record = Post.objects.get(pk=post.id)
        self.assertEqual(record, post)

