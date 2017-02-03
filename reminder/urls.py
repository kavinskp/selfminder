from django.conf.urls import url
from . import views

app_name = 'reminder'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
   # url(r'^profile_user/$', views.update_profile, name='profile_user'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<note_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<list_id>[0-9]+)/important/$', views.important, name='important'),
    url(r'^lists/(?P<filter_by>[a-zA_Z]+)/$', views.lists, name='lists'),
    url(r'^create_note/$', views.create_note, name='create_note'),
    url(r'^(?P<note_id>[0-9]+)/create_list/$', views.create_list, name='create_list'),
    url(r'^(?P<note_id>[0-9]+)/delete_list/(?P<list_id>[0-9]+)/$', views.delete_list, name='delete_list'),
    url(r'^(?P<note_id>[0-9]+)/important_note/$', views.important_note, name='important_note'),
    url(r'^(?P<note_id>[0-9]+)/delete_note/$', views.delete_note, name='delete_note'),
]
