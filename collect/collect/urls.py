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
    url(r'^programme/(?P<kr>[A-Za-z]{2})/(?P<pro>[A-Za-z]+)/(?P<sem>\d+)/print/$', 'collection.views.pro_course_list_print'),
    url(r'^programme/(?P<kr>[A-Za-z]{2})/(?P<pro>[A-Za-z]+)/(?P<sem>\d+)/submit/$', 'collection.views.add_teacher'),
    url(r'^programme/(?P<br>[A-Za-z]{2})/(?P<pro>[A-Za-z]+)/(?P<sem>\d+)/delete/(?P<entry>\d+)/$', 'collection.views.delete_teacher'),
    url(r'^programme/(?P<br>[A-Za-z]{2})/activity_log/$', 'collection.views.activity_log_details'),
    url(r'^programme/(?P<br>[A-Za-z]{2})/(?P<pro>[A-Za-z]+)/(?P<sem>\d+)/fr/$', 'collection.views.fr_course_list'),
    url(r'^programme/(?P<br>[A-Za-z]{2})/(?P<pro>[A-Za-z]+)/(?P<sem>\d+)/fr/submit/$', 'collection.views.fr_submit'),
    url(r'^programme/(?P<br>[A-Za-z]{2})/(?P<pro>[A-Za-z]+)/(?P<sem>\d+)/fr/delete/(?P<entry>\d+)/$', 'collection.views.fr_delete'),
    url(r'^programme/(?P<br>[A-Za-z]{2})/(?P<pro>[A-Za-z]+)/(?P<sem>\d+)/fr/print/$', 'collection.views.fr_course_list_print'),
)
handler404='views.custom_404'