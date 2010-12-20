from django.db import models
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db import models
from models import Project, Question, Answer
from django import forms

class ProjectForm(ModelForm):
	owner = forms.CharField(required=False)
	class Meta:
		model = Project
		exclude = ('owner')
		
#Copied form Google Groups, Rodney, http://groups.google.com/group/django-users/browse_thread/thread/9cea885e914b8240		 
class LongUserCreationForm(UserCreationForm): 
    class Meta: 
        model = User 
        fields = ['email'] 
		
class QuestionForm(ModelForm):
	explanation = forms.CharField(required=False, widget=forms.Textarea(attrs={'name': 'editor1', 'style': 'height: 200px;' } ))
	
	class Meta:
		model = Question
		exclude = ('relatedProject', 'answered')
		
	
	#title = forms.CharField(max_length=100)
	#explanation = forms.CharField(required=False)
	#relatedProject = forms.ModelChoiceField()
	#tags = forms.CharField(required=False)

class AnswerForm(ModelForm):
	explanation = forms.CharField(widget=forms.Textarea(attrs={'name': 'editor1', 'style': 'height: 200px;'}))
	
	class Meta:
		model = Answer
		exclude = ('question')
		
#class UserCreationForm(ModelForm):
	
