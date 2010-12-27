from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.list_detail import object_list
from django.template import RequestContext
#from django.contrib.auth.models import User
from django.contrib.auth import *
from django.template import RequestContext 
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response, get_object_or_404
from Learness.flow.models import Project, Question, Answer
from Learness.flow.CustomHtmlFilter import *
from forms import ProjectForm, QuestionForm, AnswerForm, LongUserCreationForm
from django.views.generic import list_detail

def first(request, template_name):
	return list_detail.object_list(
		request,
		queryset = Project.objects.all(),
		template_object_name = "project",
		template_name = template_name,
		)
		
def question_list(request, project_id, question_id=None):
	if question_id is None: 

		p = get_object_or_404(Project, pk = project_id)
		variables = RequestContext(request, { 'project' : p})
		return render_to_response('front/questions_list.html', variables)

	else:	
		p = get_object_or_404(Project, pk = project_id)
		q = get_object_or_404(Question, pk = question_id)

		variables = RequestContext(request, { 'project' : p, 'question' : q})
		return render_to_response('front/questions_list.html', variables)

	#question_list = login_required(question_list)
    
