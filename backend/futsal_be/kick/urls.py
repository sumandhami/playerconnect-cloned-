from django.urls import path
from .views import views_admin
from .views import views_user

urlpatterns = [
    #admin user's
    path('csrf-token/', views_admin.csrf_token_view,name='csrf-token'),
    path('players/', views_admin.player_list, name='player_list'),
    path('signup/', views_admin.signup, name='signup'),
    path('add_futsal/',views_admin.addfutsal,name='add_futsal'),
    path('complete_game_request/',views_admin.complete_game_request,name='complete_game_request'),
    path('add_timeslotfutsal/',views_admin.addtimeSlotbyFutsal,name='add_timeslotfutsal'),
    #user api's
    path('login/', views_user.login, name='login'),
    path('pick_time_slot/',views_user.pick_time_slot,name='pick_time_slot'),
    path('join_request/',views_user.join_request,name='join_request'),
    path('handleparticipation/',views_user.handleparticiation,name='handleparticipation'),
    path('change_state/',views_user.Change_state,name='change_state'),
    path('near_by/',views_user.near_by,name='near_by')
]