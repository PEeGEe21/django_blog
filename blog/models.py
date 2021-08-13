from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from autoslug import AutoSlugField

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

    objects = models.Manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    @property
    def number_of_comments(self):
        return Comment.objects.filter(post=self).count()

    @property
    def total_likes(self):
        return self.likes.count()



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_added= models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_added']

    def __str__(self):
        return f'{self.post.title} - {self.author}'

# class Like(models.Model):
#     user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)