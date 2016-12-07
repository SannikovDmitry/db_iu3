from django.contrib.auth.forms import UserCreationForm
from django.forms import *
from django import forms
from main.models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')

class TagsField(forms.CharField):
    def to_python(self, value):
        # Return an empty list if no input was given.
        if not value:
            return []
        tags = value.split(' ')

        cleaned_tags = []

        for tag in tags:
            tag_name = tag.strip()
            if tag_name != '':
                if not cleaned_tags.__contains__(tag_name):
                    cleaned_tags.append(tag_name)

        return cleaned_tags

    def validate(self, value):
        # Use the parent's handling of required fields, etc.
        super(TagsField, self).validate(value)
class ChangePasswordForm(forms.Form):
    password = forms.CharField(min_length=6, max_length=20, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'New password',
        'required': 'true',
    }))
class QuestionForm(forms.Form):
    title = forms.CharField(max_length=100, widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Question title',
        'required': 'true',
    }))
    text = forms.CharField(max_length=2048, widget=Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'The actual question',
        'rows': '5',
        'required': 'true',
    }))
    tags = TagsField(required=False, widget=TextInput( attrs={
        'class': 'form-control',
        'placeholder': 'Input your tags separated by space here'
    }))


class AnswerForm(forms.Form):
    title = forms.CharField(max_length=100, widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Answer title'
    }))
    content = forms.CharField(max_length=1024, widget=Textarea(attrs={
        'id': 'id_answer_content',
        'class': 'form-control',
        'placeholder': 'Input your answer here'
    }))