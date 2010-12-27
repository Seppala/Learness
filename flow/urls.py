from django.conf.urls.defaults import *
from django.contrib.auth.views import *
from django.views.generic import list_detail
from django.contrib.auth.decorators import login_required
from Learness.flow.models import Project, Question

info_dict = {
    'queryset': Project.objects.all(),
	'template_object_name' : 'project',
    }

urlpatterns = patterns('',
    #(r'^$', 'limited_object_list'),
	
	#Working generic view for the project list page
	#(r'^$', login_required(list_detail.object_list), info_dict),
	(r'^$', 'Learness.flow.views.projects_user'),
	
    #(r'^(?P<project_id>\d+)/$', 'question_list'),
    #(r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', info_dict),
    	)
	
urlpatterns += patterns('Learness.flow.views',
	(r'^register/$', 'register'),
	(r'^(?P<project_id>\d+)/$', 'question_list'),
    (r'^(?P<project_id>\d+)/(?P<question_id>\d+)/$', 'question_list'), 
    (r'^create/$', 'createProject'),
    (r'^edit/(?P<project_id>\d+)/(?P<question_id>\d+)/(?P<answer_id>\d+)/$', 'editAnswer'),
	(r'^edit/(?P<project_id>\d+)/(?P<question_id>\d+)/$', 'editQuestion'),
    (r'^answer/(?P<project_id>\d+)/(?P<question_id>\d+)/$', 'createAnswer'),
    (r'^question/(?P<project_id>\d+)/$', 'createQuestion'),
    (r'^project/$', 'createProject'),
  	(r'^delete/(?P<project_id>\d+)/$', 'deleteProject'),
	(r'^delete/(?P<project_id>\d+)/(?P<question_id>\d+)/(?P<answer_id>\d+)/$', 'deleteAnswer'),
	(r'^delete/(?P<project_id>\d+)/(?P<question_id>\d+)/$', 'deleteQuestion'),
	(r'^collaborate/(?P<project_id>\d+)/$', 'applyToCollaborate'),
  
         
    #url(r'^(?P<object_id>\d+)/results/$', 'django.views.generic.list_detail.object_detail', dict(info_dict, template_name='polls/results.html'), 'poll_results'),
    #(r'^(?P<poll_id>\d+)/vote/$', 'Learness.polls.views.vote'),

)
