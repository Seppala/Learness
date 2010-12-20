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
from learness3.flow.models import Project, Question, Answer
from learness3.flow.CustomHtmlFilter import *
from forms import ProjectForm, QuestionForm, AnswerForm, LongUserCreationForm
from django.views.generic import list_detail

@login_required
def limited_object_list(request):
	return object_list(request, 
	queryset = Project.objects.all(), 
	#'template_object_name' : 'project',
	)

#For starting page wrapper	
def projects_user(request):
	u = request.user
	return list_detail.object_list(
		request,
		queryset = Project.objects.filter(owner = u),
		template_object_name = "project",
		)
projects_user = login_required(projects_user)

def projects_all(request):
	#u = request.user
	return list_detail.object_list(
		request,
		queryset = Project.objects.all(),
		template_object_name = "project",
		)
	
def question_list(request, project_id, question_id=None):
	
	p = get_object_or_404(Project, pk = project_id)
	
	#First test if the logged-in user is in the projects collaborators.
	if request.user in p.collaborators.all():
		isCollaborator = True
	else:
		isCollaborator = False
		
	#Test if the logged-in user is the owner of the project.
	if request.user == p.owner:
		isOwner = True
	else:
		isOwner = False
	
	#Test if the logged-in user has applied to collaborate (appliers)
	
	if request.user in p.appliers.all():
		isApplier = True
		
	else:
		isApplier = False
	
	#Depending on whether a question has been selected, either return the variables with the
	#question or without.
	if question_id is None: 
		
		p = get_object_or_404(Project, pk = project_id)
		variables = RequestContext(request, { 'project' : p, 'isCollaborator' : isCollaborator, 'isOwner' : isOwner, 'isApplier' : isApplier })
		return render_to_response('flow/questions_list.html', variables)
		
	else:	
		p = get_object_or_404(Project, pk = project_id)
		q = get_object_or_404(Question, pk = question_id)
	
		variables = RequestContext(request, { 'project' : p, 'question' : q, 'isCollaborator' : isCollaborator, 'isOwner' : isOwner  })
		return render_to_response('flow/questions_list.html', variables)

#question_list = login_required(question_list)

#Copied From Tyson at Stackoverflow.com
def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)

		if form.is_valid():
			message = None

			form.save()

			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']

			user = authenticate(username=username, password=password)

			email = user.email

			# If valid new user account
			if (user is not None) and (user.is_active):
				login(request, user)
				message = "<strong>Congratulations!</strong> You have been registered."

				# Send emails
				try:
					# Admin email
					pk = None
					try: pk = User.objects.filter(username=username)[0].pk
					except: pass

					admin_email_template = loader.get_template('accounts/email_notify_admin_of_registration.txt')
					admin_email_context = Context({
						'first_name': first_name,
						'last_name': last_name,
						'username': username,
						'email': email,
						'pk': pk,
					})
					admin_email_body = admin_email_template.render(admin_email_context)
					mail_admins("New User Registration", admin_email_body)

					# User email
					user_email_template = loader.get_template('accounts/email_registration_success.txt')
					user_email_context = Context({
						'first_name': form.cleaned_data['first_name'],
						'username': username,
						'password': password,
					})
					user_email_body = user_email_template.render(user_email_context)
					user.email_user("Successfully Registered at example.com", user_email_body)
				except:
					message = "There was an error sending you the confirmation email. You should still be able to login normally."
			else:
				message = "There was an error automatically logging you in. Try <a href=\"/login/\">logging in</a> manually."

			# Display success page
			return render_to_response('flow/project_list.html', {
					'username': username,
					'message': message,
				},
				context_instance=RequestContext(request)
			)
	else: # If not POST
		form = LongUserCreationForm()

	return render_to_response('register.html', {
			'form': form,
		},
		context_instance=RequestContext(request)
	)

def createProject(request):
    #un = User.__unicode__(request.user)
    #user = get_object_or_404(User, username = un)
    if request.method == 'POST': # If the form has been submitted...
        user = Project(owner = request.user)
        form = ProjectForm(request.POST, instance = user) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            new_project = form.save()           
            return HttpResponseRedirect('/flow/') # Redirect after POST
    else:
        form = ProjectForm() # An unbound form
        variables = RequestContext(request, { 'form': form })
        return render_to_response('flow/createproject.html', variables)
createProject = login_required(createProject)
	
def createAnswer(request, project_id, question_id):
	p = get_object_or_404(Project, pk = project_id, owner = request.user)
	q = get_object_or_404(Question, pk = question_id)	
	if request.method == 'POST': # If the form has been submitted...
		answer = Answer(question = q)
		form = AnswerForm(request.POST, instance = answer)
		#form = AnswerForm(request.POST, instance = answer) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
                      #  x = CustomHTMLFilter()
			#x.add_tags("body p")
			#new_answer = form.save(commit = False)
			#new_answer.explanation = x(new_answer.explanation)
			new_answer = form.save()		
			return HttpResponseRedirect('/flow/' + project_id + '/' + question_id + '/#' + question_id) # Redirect after POST
	else:
		form = AnswerForm() # An unbound form
		variables = RequestContext(request, { 'form': form,	 'url_project' : p, 'url_question' : q })	
		return render_to_response('flow/createanswer.html', variables)
createAnswer = login_required(createAnswer) 
	
def editAnswer(request, project_id, question_id, answer_id):
	p = get_object_or_404(Project, pk = project_id, owner = request.user)
	q = get_object_or_404(Question, pk = question_id)
	a = get_object_or_404(Answer, pk = answer_id)
	#answer = Answer.objects.get(pk=p)
	if request.method == 'POST': # If the form has been submitted...
		form = AnswerForm(request.POST, instance = a) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			form.save()			
			return HttpResponseRedirect('/flow/' + project_id + '/' + question_id + '/#' + question_id) # Redirect after POST
	else:
		form = AnswerForm(instance=a) # An unbound form
		variables = RequestContext(request, { 'form': form,	 'url_project' : p, 'url_question' : q, 'url_answer' : a})
		return render_to_response('flow/editanswer.html', variables)

editAnswer = login_required(editAnswer) 

def editQuestion(request, project_id, question_id):
	p = get_object_or_404(Project, pk = project_id, owner = request.user)
	q = get_object_or_404(Question, pk = question_id)
	
	#answer = Answer.objects.get(pk=p)
	if request.method == 'POST': # If the form has been submitted...
		form = QuestionForm(request.POST, instance = q) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			form.save()			
			return HttpResponseRedirect('/flow/' + project_id +'/#' + question_id) # Redirect after POST
	else:
		form = QuestionForm(instance=q) # A form initiated with the question data
		variables = RequestContext(request, { 'form': form,	 'url_project' : p, 'url_question' : q })
		return render_to_response('flow/editQuestion.html', variables)

editQuestion = login_required(editQuestion)

def createQuestion(request, project_id):
	p = get_object_or_404(Project, pk = project_id, owner = request.user) 
	if request.method == 'POST': # If the form has been submitted...
		question = Question(relatedProject = p) # set the relatedProject field which is not included in the form
		form = QuestionForm(request.POST, instance = question) # A form bound to the POST data
		
		if form.is_valid(): # All validation rules pass
			#title = form.cleaned_data['title']
			#explanation = form.cleaned_data['explanation']
			#relatedProject = form.cleaned_data['relatedProject']
			#tags = form.cleaned_data['tags']
			#new_question = 
			new_question = form.save()	
			qid = str(new_question.pk)		
			return HttpResponseRedirect('/flow/' + project_id + '/' + qid + '/' + '#' + qid) # Redirect after POST
	else:
		form = QuestionForm() # An unbound form
		variables = RequestContext(request, { 'form': form,	 'url_project' : p })
		return render_to_response('flow/createquestion.html', variables)
createQuestion = login_required(createQuestion)		
	
#Deleting a project

def deleteProject(request, project_id):
	o = get_object_or_404(Project, pk = project_id, owner = request.user)
	o.delete()
	return HttpResponseRedirect('/flow/') # Redirect after deletion

#Delete question
	
def deleteQuestion(request, project_id, question_id):
	o = get_object_or_404(Question, pk = question_id)
	qminusone = int(question_id)-1
	qminusone = str(qminusone)
	o.delete()
	return HttpResponseRedirect('/flow/' + project_id + '/' +'#' + qminusone)
	
	
deleteQuestion = login_required(deleteQuestion)
	
#Delete answer	
def deleteAnswer(request, project_id, question_id, answer_id):
	o = get_object_or_404(Answer, pk = answer_id)
	o.delete()
	return HttpResponseRedirect('/flow/' + project_id + '/' + question_id + '/' +'#' + question_id)

deleteAnswer = login_required(deleteAnswer)

def applyToCollaborate(request, project_id):
	o = get_object_or_404(Project, pk = project_id)
	o.appliers.add(request.user)
	return HttpResponseRedirect('/flow/' + project_id + '/')

applyToCollaborate = login_required(applyToCollaborate)
	
