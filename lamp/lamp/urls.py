from django.conf.urls import patterns, include, url
from django.contrib import admin
from streetlights import views
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lamp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index,name='index'),
    url(r'^lampfall$', views.geodata,  name='data'),
    url(r'^denthi$', views.denthialma, name='denthi')
)
