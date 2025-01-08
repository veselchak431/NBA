from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'nba'
urlpatterns = [
    path('', views.home, name='home'),
    path('visitor_menu/', views.visitor_menu, name='visitor_menu'),

    path('players_main/', views.players_main, name='players_main'),
    path('player/<int:player_id>/', views.player_detail, name='player_detail'),

    path('teams_main/', views.teams_main, name='teams_main'),
    path('team_detail/<int:team_id>/', views.team_detail, name='team_detail'),

    path('matchups_list/', views.matchup_list, name='matchups_list'),
    path('matchup/<int:matchup_id>/', views.matchup_detail, name='matchup_detail'),

    path('photos/', views.photos, name='photos'),

    path('admin_login/', views.admin_login, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
