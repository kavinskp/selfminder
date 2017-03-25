from django.conf.urls import url
from .views_1 import users
from . import views
app_name = 'reminder'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.signup, name='register'),
  #  url(r'^changepass/$',views.passchange,name = "changepass"),
    url(r'^profile_user/$', views.userprofile, name='profile_user'),
    url(r'^login_user/$', views.userlogin, name='login_user'),
   # url(r'^user/password/reset/$', views.password_reset, {'post_reset_redirect': '/user/password/reset/done/',
           #                 'template_name': 'registration/password_reset_form.html'},name="password_reset"),
   # url(r'^user/password/reset/done/$', views.password_reset_done),
  #  url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.password_reset_confirm,
      #  {'post_reset_redirect': '/user/password/done/'}, name='urlreset'),
  # url(r'^user/password/done/$',views.password_reset_complete),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^new-activation-link/(?P<user_id>\d+)$', views.new_activation_link,name='new_activation_link'),
    url(r'^activate/(?P<key>.+)$', views.activation, name='activation'),
    url(r'^(?P<note_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<list_id>[0-9]+)/important/$', views.important, name='important'),
    url(r'^lists/(?P<filter_by>[a-zA_Z]+)/$', views.lists, name='lists'),
    url(r'^create_note/$', views.create_note, name='create_note'),
    url(r'^(?P<note_id>[0-9]+)/create_list/$', views.create_list, name='create_list'),
    url(r'^(?P<note_id>[0-9]+)/delete_list/(?P<list_id>[0-9]+)/$', views.delete_list, name='delete_list'),
    url(r'^(?P<note_id>[0-9]+)/important_note/$', views.important_note, name='important_note'),
    url(r'^(?P<note_id>[0-9]+)/delete_note/$', views.delete_note, name='delete_note'),
]
