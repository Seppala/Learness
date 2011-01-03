from django.db import models
from django.forms import ModelForm
#from tagging.fields import TagField
#from tagging.models import Tag
from django.contrib.auth.models import User

# Create your models here.

#class User(models.Model):
 #   name = models.CharField(max_length=20)
  #  email = models.EmailField()
    # shot = models.ImageField(upload_to='userimage')

   # def __str__(self):
    #    return self.name

    # class Admin: pass
    
class Project(models.Model):
	name = models.CharField(max_length=50)
	owner = models.ForeignKey(User, related_name = "owner")
	#tags = TagField()
	datecreated = models.DateField(auto_now_add=True, null = True)
	collaborators = models.ManyToManyField(User, related_name = "collaborators", blank = True)
	appliers = models.ManyToManyField(User, related_name = "appliers", blank = True)

	class Admin: pass
	   

	#def set_tags(self, tags):
	#	Tag.objects.update_tags(self, tags)

	#def get_tags(self, tags):
	#	return Tag.objects.get_for_object(self) 

	def __str__(self):
	   return self.name

class Question(models.Model):
    title = models.CharField(max_length=200)
    #slug= models.SlugField(
    #    unique_for_date='pub_date',
    #    help_text='automatically built from the title.'
    #)
    explanation = models.TextField(blank=True)
    relatedProject = models.ForeignKey(Project)
    datecreated = models.DateField(auto_now_add=True)
    datemodified = models.DateField(auto_now=True)
    ANSWERED_CHOICES = (
        ('p', 'pending'),
        ('r', 'resolved'),
        ('s', 'answered'),
        )
    answered = models.CharField(max_length=1, choices=ANSWERED_CHOICES, default='p')
    #tags = TagField()

    class Admin: pass

    #def set_tags(self, tags):
     #   Tag.objects.update_tags(self, tags)

    #def get_tags(self, tags):
     #   return Tag.objects.get_for_object(self) 

    def __unicode__(self):
        return self.title
    

class Answer(models.Model):
    explanation = models.TextField()
    question = models.ForeignKey(Question)
    #tags = TagField()

    class Admin: pass

    #def set_tags(self, tags):
     #   Tag.objects.update_tags(self, tags)

    #def get_tags(self, tags):
     #   return Tag.objects.get_for_object(self) 


    def __unicode__(self):
        return self.question.title

class Comment(models.Model):
    comment = models.TextField()
    commenttoanswer = models.ForeignKey(Answer)
    commenttoquestion = models.ForeignKey(Question)

    class Admin: pass

    def __str__(self):
        return self.comment
    
class Link(models.Model):
    link = models.URLField()
    commentlink = models.ForeignKey(Comment)
    answerlink = models.ForeignKey(Answer)
    questionlink = models.ForeignKey(Question)

    class Admin: pass
    

    def __str__(self):
        return self.link



