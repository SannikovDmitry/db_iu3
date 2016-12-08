from django.db import models
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.contrib.auth.models import User
from django.forms import ModelForm

# Create your models here.

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='static/profile_images', blank=True)
	def __unicode__(self):
		return self.user.username

class Hashtag(models.Model):
	tag = models.CharField(max_length = 22)
	def link(self):
		return '/tag/' + self.tag
	def __unicode__(self):
		return '#' + self.tag

def popular_tags():
	tags = Hashtag.objects.all()
	def cmptags(a_tag):
		return Question.objects.filter(hashtags=a_tag.id).count()
	return sorted(tags, key=cmptags)[:5]

class QuestionManager(models.Manager):

	def top(self):
		return getPager(Question, "-likes")

	def index(self):
		return getPager(Question, '-timeStamp')

	def by_tag(self, htag):
		try:
			this_tag = Hashtag.objects.get(tag = htag)
		except DoesNotExist:
			raise Http404
		return Paginator(self.filter(hashtags=this_tag.id), 5)

class Question(models.Model):
	author = models.ForeignKey(UserProfile, null=True)
	title = models.CharField(max_length = 50)
	text = models.TextField()
	timeStamp = models.DateTimeField()
	likes = models.IntegerField(default = 0)
	dislikes = models.IntegerField(default = 0)
	hashtags = models.ManyToManyField(Hashtag)
	answerCount = models.IntegerField(default = 0)
	objects = QuestionManager()

	def like(self):
		self.likes = self.likes + 1
		self.save()

	def dislike(self):
		self.dislikes = self.dislikes + 1
		self.save()

	def get_answers(self):
		return Paginator(Answer.objects.filter(
			question__id = self.id).order_by('-likes'), 5)

	def __unicode__(self):
		return self.title

def authors():
	author = Question.objects.all()
	return author

class Answer(models.Model):
	author = models.ForeignKey(UserProfile, null=True)
	title = models.CharField(max_length = 50)
	question = models.ForeignKey(Question)
	text = models.TextField()
	timeStamp = models.DateTimeField()
	correct = models.BooleanField(default = False)
	likes = models.IntegerField(default = 0)
	dislikes = models.IntegerField(default = 0)

	def __unicode__(self):
		return self.title

	def like(self):
		self.likes = self.likes + 1
		self.save()

	def dislike(self):
		self.dislikes = self.dislikes + 1
		self.save()

		
def getPager(model, order_by_what):
	return Paginator(model.objects.order_by(order_by_what), 5)

def findPage(pager, page):
	try:
		p = pager.page(page)
	except EmptyPage, e:
		raise Http404
	return p

