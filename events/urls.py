from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('events/register/<int:event_id>/',views.register_event,name='register_event'),
    path('create-team/',views.create_team,name='create_team'),
    path('teams/',views.team_list,name='team_list'),
    path('apply-team/<int:team_id>/',views.apply_team,name='apply_team'),
    path('my-applications/',views.my_applications,name='my_applications'),
    path('leader-dashboard/',views.leader_dashboard,name='leader_dashboard'),
    path('accept/<int:application_id>/',views.accept_application,name='accept_application'),
    path('reject/<int:application_id>/',views.reject_application,name='reject_application'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('team-members/<int:team_id>/',views.team_members,name='team_members'),

]
