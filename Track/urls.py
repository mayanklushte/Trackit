from django.urls import path, re_path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.registers, name="registers"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('r_com/', views.reg_com, name='r_com'),
    path('r_com/<int:id>/', views.project, name='a_form'),

    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('event/new/', views.event, name='event_new'),
    re_path(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    path('comlist/', views.comlist, name='comlist'),
    path('comlist/<int:id>/', views.comd, name='comdetaails'),
    path('u_list/', views.u_project, name='u_list'),
    path('a_comlist/', views.a_comlist, name='a_comlist'),
    path('a_comlist/<int:id>/', views.a_comd, name='a_comdetaails'),
    path('u_event/', views.u_event, name='u_event'),

    path('u_event/<int:id>/', views.event_d, name='event_d'),

    path('u_plist/', views.project_list, name='project_l'),
    path('u_plist/<int:id>/', views.project_details, name='project_d'),
    path('accept/<int:id>/', views.accept, name='accept'),
    path('reject/<int:id>/', views.reject, name='reject'),
    path('accp_list/', views.accp_list, name='accp_list'),
    path('accp_list/<int:id>/', views.accp_details, name='accp_details'),
    path('user_event/new/', views.user_event, name='user_e'),

    # user chat
    path('chat/', views.u_comlist, name='u_chat'),
    path('chat/<int:id>/', views.u_comd, name='uchat_d'),


    # mini admin url
    path('ap_list/', views.mi_add, name='ap_list'),
    path('ap_list/<int:id>/', views.mi_p_det, name='mi_pdet'),
    path('ma_event/', views.au_event, name='ma_event'),
    path('ma_event/<int:id>/', views.aevent_d, name='ma_event_d'),
    path('ma_chat/', views.acomlist, name='ma_chat'),
    path('ma_chat/<int:id>/', views.acomd, name='ma_chatr'),


]
