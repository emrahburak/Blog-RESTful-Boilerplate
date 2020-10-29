from django.db import models
from django.utils import timezone
from django.utils.text import slugify




class Corpus(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='corpus')
    title = models.CharField(max_length=120)
    content = models.TextField(editable=True)
    draft = models.BooleanField(default=False, editable=False)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)
    slug = models.SlugField(unique=True, max_length=150, editable=False)
    image = models.ImageField(upload_to='corpus', null=True, blank=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, editable=False, related_name='modified')

    class Meta:
        ordering = ['-created']

    
    def __str__(self):
        return self.title

    
    def get_slug(self):
        slug = slugify(self.title.replace('ı', 'i'))
        unique = slug
        number = 1

        while Corpus.objects.filter(slug=unique).exists():
            unique = '{}-{}'.format(slug,number)
            number += 1
        return unique



    def save(self, *args, **kwargs):
        "if first time create django puts new time"
        if not self.id:
            self.created = timezone.now()

        self.modified = timezone.now()
        self.slug = self.get_slug()
        return super(Corpus, self).save(*args, **kwargs)
