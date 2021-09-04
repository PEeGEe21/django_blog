from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from autoslug import AutoSlugField
from django.urls import reverse
from django.conf import settings
from cloudinary.models import CloudinaryField






# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    displayname = models.CharField('Name', default='', max_length=25, blank=True, null=True)
    slug = AutoSlugField(populate_from='user', null=True)
    bio = models.TextField(default='', blank=True, null=True)
    birthday = models.DateField('Birthday', blank=True, null=True)
    image = models.ImageField(default='default.png', upload_to='profile_pics', blank=True, null=True)
    coverimage = models.ImageField(default='default_cover.jpg', upload_to='cover_pics', blank=True, null=True)

    # image = CloudinaryField('image', blank=True, default='default.png')
    # coverimage = CloudinaryField('coverimage', blank=True, default='default.png')
    followers = models.ManyToManyField("Profile", blank=True)
    # following = models.ManyToManyField("FollowProfile", blank=True)


    def __str__(self):
        return f'{self.user.username} Profile'

    def get_absolute_url(self):
        return "/users/profile/{}".format(self.slug)
        # return reverse('profile_view', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class FollowRequest(models.Model):
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)
# class Following(models.Model):
#     to_user_follow = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user_follow', on_delete=models.CASCADE)
#     from_user_follow = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user_follow', on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return "From {}, to {}".format(self.from_user_follow.username, self.to_user_follow.username)