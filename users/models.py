from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from autoslug import AutoSlugField
from django.urls import reverse




# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    displayname = models.CharField('Name', default='', max_length=25)
    slug = AutoSlugField(populate_from='user', null=True)
    bio = models.TextField(default='')
    birthday = models.DateTimeField('Birthday', blank=True, null=True)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    coverimage = models.ImageField(default='default.png', upload_to='cover_pics')


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