from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import views_admin
from .views import views_user

urlpatterns = [
    # Admin APIs
    path('csrf-token/', views_admin.csrf_token_view, name='csrf-token'),
    path('signup/', views_admin.signup, name='signup'),
    path('add_futsal/', views_admin.addfutsal, name='add_futsal'),
    path('complete_game_request/', views_admin.complete_game_request, name='complete_game_request'),
    path('add_timeslotfutsal/', views_admin.addtimeSlotbyFutsal, name='add_timeslotfutsal'),

    # User APIs
    path('login/', views_user.login, name='login'),
    path('getplayer/', views_user.getplayer, name='player_data'),
    path('update/', views_user.update, name='update'),
    path('pick_time_slot/', views_user.pick_time_slot, name='pick_time_slot'),
    path('join_request/', views_user.join_request, name='join_request'),
    path('handleparticipation/', views_user.handleparticiation, name='handleparticipation'),
    path('change_state/', views_user.Change_state, name='change_state'),
    path('near_by/', views_user.near_by, name='near_by'),
]

# **Serve Media Files in Development**
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
