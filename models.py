from django.db import models
from datetime import datetime
from ckeditor.fields import RichTextField

# Create your models here.

class User(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.EmailField()
	username = models.CharField(max_length=40)
	password = models.CharField(max_length=100)
	bio = models.TextField(default="none")
	profile_pic = models.ImageField(upload_to='pictures', default='default.jpg')
	def __str__(self):
		return self.first_name

class Followers(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	another_user = models.ManyToManyField(User, related_name='another_user')

	def __str__(self):
		return self.user.first_name

class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	content = RichTextField(blank=True,null=True)
	creation_date = models.DateField(auto_now_add=True)
	likes = models.ManyToManyField(User, related_name='likes')

	def __str__(self):
		return self.title


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	name = models.CharField(default='no name',max_length=50)
	comment = models.CharField(max_length=400)

	def __str__(self):
		return self.name+"=>"+self.comment


class Contact(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField(default=None)
	message = models.TextField()

	def __str__(self):
		return self.name



