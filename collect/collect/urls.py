from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'collect.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$', 'collection.views.index', name='index'),
    url(r'^programme/(?P<br>[A-Za-z]{2})/$', 'collection.views.programme_list'),
    url(r'^programme/(?P<kr>[A-Za-z]{2})/(?P<pro>[A-Za-z]+)/$', 'collection.views.pro_course_list'),
    url(r'proposecourse', 'collection.views.proposecourse', name='proposecourse'),

)
