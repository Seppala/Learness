from django.conf.urls.defaults import *
from django.contrib.auth.views import *
from django.views.generic import list_detail
from django.contrib.auth.decorators import login_required
from Learness.flow.models import Project, Question

info_dict = {
    'queryset': Project.objects.all(),
	'template_object_name' : 'project',
    }

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^comments/', include('django.contrib.comments.urls')),
	(r'^flow/', include('Learness.flow.urls')),
	(r'^front/', include('Learness.flow.front.urls')),
	(r'^$', include('Learness.flow.urls')),
	#(r'^$', 'Learness.flow.frontviews.first', {'template_name': 'flow/project_list_front.html'}),
	#(r'^', 'Learness.flow.frontviews.first')),
	#(r'^search/', include('haystack.urls')),
	(r'^accounts/login/$', 'django.contrib.auth.views.login'),
	(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
	(r'^accounts/profile/$', 'Learness.flow.views.projects_user'),
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', 
	{'document_root': '/Users/rikuseppala/Dropbox/Learness/mediat'}),

	# Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
	# to INSTALLED_APPS to enable admin documentation:
	# (r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),
)
