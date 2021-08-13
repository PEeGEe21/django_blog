from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from django.http import HttpResponse
from django.db import models
from .models import Post, Comment



class PostCreationForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = '__all__'
        template_name = 'blog/home.html'


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'textarea-form trans-bg',
                # 'width':'100%',
                'placeholder': 'Enter your comment....'
            })
        }