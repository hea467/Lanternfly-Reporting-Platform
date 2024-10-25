from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    bio = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50)
    following = models.ManyToManyField(User, related_name="following")

    def __str__(self):
        return 'id=' + str(self.id) + ',text="' + self.bio + '"'

class Spotting(models.Model):
    # latitude = models.FloatField(min_value=-90, max_value=90)
    # longitude = models.FloatField(min_value=-180, max_value=180)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kill_num = models.IntegerField(default = 0)
    see_num = models.IntegerField(default = 0)
    tree_num = models.IntegerField(default = 0)
    picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50)



class Post(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)

    creation_time = models.DateTimeField()

    # class Meta:
    #     ordering = ('-creation_time',)
        # date:"n/j/Y g:i A"

    def __str__(self):
        return f'id={self.id}, text="{self.text}"'
    

class Comment(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    creation_time = models.DateTimeField()
    posts = models.ForeignKey(Post, default=None, on_delete=models.PROTECT)