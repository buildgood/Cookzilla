from django.conf.urls import url

from . import views

app_name = 'cook'

urlpatterns = [
	#/cook/
    url(r'^$', views.index, name='index'),
    url(r'^login_user/', views.login_user, name='login_user'),
    url(r'^logout_user/', views.logout_user, name='logout_user'),
    url(r'^register/', views.register, name='register'),
    url(r'^recipe/$', views.recipe, name='recipe'),
    url(r'^group/$', views.group, name='group'),
    url(r'^event/$', views.event, name='event'),
    url(r'^search/$', views.search, name='search'),
    url(r'^search_tag/(?P<tag_tag>[a-zA-Z ]+)$', views.search_tag, name='search_tag'),
    url(r'^a_recipe/(?P<recipe_rid>[0-9]+)$', views.a_recipe, name='a_recipe'),
    url(r'^a_group/(?P<group_gid>[0-9]+)$', views.a_group, name='a_group'),
    url(r'^a_event/(?P<event_eid>[0-9]+)$', views.a_event, name='a_event'),
    url(r'^join_group/$', views.join_group, name='join_group'),
    url(r'^delete_group/(?P<group_gid>[0-9]+)$', views.delete_group, name='delete_group'),
    url(r'^rsvp/$', views.rsvp, name='rsvp'),
    url(r'^delete_rsvp/(?P<event_eid>[0-9]+)$', views.delete_rsvp, name='delete_rsvp'),
    url(r'^account/$', views.account, name='account'),
    url(r'^my_recipe/$', views.my_recipe, name='my_recipe'),
    url(r'^my_group/$', views.my_group, name='my_group'),
    url(r'^my_rsvp/$', views.my_rsvp, name='my_rsvp'),
    url(r'^my_review/$', views.my_review, name='my_review'),
    url(r'^my_report/$', views.my_report, name='my_report'),
    url(r'^delete_recipe/(?P<recipe_rid>[0-9]+)$', views.delete_recipe, name='delete_recipe'),
    url(r'^delete_review/(?P<review_revid>[0-9]+)$', views.delete_review, name='delete_review'),
    url(r'^delete_report/(?P<report_repid>[0-9]+)$', views.delete_report, name='delete_report'),
    url(r'^my_profile/$', views.my_profile, name='my_profile'),
    url(r'^update_user/$', views.update_user, name='update_user'),
    url(r'^add_recipe/$', views.add_recipe, name='add_recipe'),
]