"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# id authomatically
# not used for now, but will be for sure

class UserDetails(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    pseudonime = models.CharField(max_length=200)
    favorite_book = models.CharField(max_length=200)
    profile_pic = models.ImageField()


class ArtPublish(models.Model):
    author_id = models.ForeignKey(User, on_delete=models.CASCADE) #do I want to remove profile i.e. art when deleting user (?!)
    date = models.DateTimeField()
    views = models.BigIntegerField()
    upvotes = models.BigIntegerField()
    text = models.TextField()
    genre = models.CharField(max_length = 30)
    title = models.CharField(max_length = 100)

class ArtDraft(models.Model):
    author_id = models.ForeignKey(User, on_delete=models.CASCADE) #do I want to remove profile i.e. art when deleting user (?!)
    date = models.DateTimeField()
    text = models.TextField()
    genre = models.CharField(max_length = 30)
    title = models.CharField(max_length = 100)

# we seperate poetry and short storyies in art, and quotes seperately

class QuotePublish(models.Model):
    author_id = models.ForeignKey(User, on_delete=models.CASCADE) #do I want to remove profile i.e. art when deleting user (?!)
    date = models.DateTimeField()
    views = models.BigIntegerField()
    upvotes = models.BigIntegerField()
    text = models.TextField()
    genre = models.CharField(max_length = 30) #we should remove it but let's keep it for now
    title = models.CharField(max_length = 100)
    originalauthor = models.CharField(max_length = 100)

class QuoteDraft(models.Model):
    author_id = models.ForeignKey(User, on_delete=models.CASCADE) #do I want to remove profile i.e. art when deleting user (?!)
    date = models.DateTimeField()
    text = models.TextField()
    genre = models.CharField(max_length = 30)
    title = models.CharField(max_length = 100)
    originalauthor = models.CharField(max_length = 100)


class AuthorsUpvotes(models.Model):
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=30)
    art_id = models.BigIntegerField()

  

class Followers(models.Model):
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.BigIntegerField()

class Following(models.Model):
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.BigIntegerField()


class ArtPublishComment(models.Model):
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    artpublish_id = models.ForeignKey(ArtPublish, on_delete=models.CASCADE)
    date = models.DateTimeField()
    text = models.TextField()

class QuotePublishComment(models.Model):
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    quotepublish_id = models.ForeignKey(QuotePublish, on_delete=models.CASCADE)
    date = models.DateTimeField()
    text = models.TextField()



