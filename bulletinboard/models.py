from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    '''
        user model
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    birth_date = models.DateField('Users date of birth', null=True, blank=True)
    avatar = models.ImageField(upload_to='images/', default=None)

    def __str__(self):
        return str(self.user.username)


class Category(models.Model):
    '''
        announcements category model
    '''
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.category_name)


class PostQuerySet(models.QuerySet):
    def publish(self):
        from django.utils.timezone import now
        return self.filter(published_date__lte=now())


class Post(models.Model):
    '''
        sale announcement model
    '''
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement_title = models.CharField(max_length=200)
    description = models.TextField(max_length=1500, blank=True)
    announcement_image = models.ImageField(upload_to='images/', default=None)
    category = models.ForeignKey(Category,  on_delete=models.CASCADE, related_name='posts')
    published_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    price = models.FloatField(blank=True)
    objects = PostQuerySet.as_manager()

    def __str__(self):
        return 'Announcement: {}, date: {}, Author: {}'.format(
            self.announcement_title, self.published_date.date(), self.author.username
        )


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=700, blank=False)
    in_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{0} : {1}".format(self.author, self.text[:10] + "...")