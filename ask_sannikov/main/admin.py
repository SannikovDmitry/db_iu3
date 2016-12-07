from django.contrib import admin
from .models import Question, Hashtag, Answer, UserProfile

# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
	list_filter = ['title']
	search_fields = ['text']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Hashtag)
admin.site.register(UserProfile)