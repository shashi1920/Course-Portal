from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'collect.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$', 'collection.views.index', name='index'),
    url(r'^login/$', 'collection.views.login_user', name='login_user'),
    url(r'^logout/$', 'collection.views.logout_user', name='logout_user'),
    url(r'^programme/(?P<br>[A-Za-z]{2})/$', 'collection.views.programme_list', name='programme_list'),
    url(r'^programme/(?P<kr>[A-Za-z]{2})/(?P<pro>[A-Za-z]+)/(?P<sem>\d+)/$', 'collection.views.pro_course_list'),
    url(r'^programme/(?P<kr>[A-Za-z]{2})/(?P<pro>[A-Za-z]+)/(?P<sem>\d+)/submit/$', 'collection.views.add_teacher'),
)
