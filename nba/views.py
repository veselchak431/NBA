from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from .models import (Team, Conference, Division, Season, PlayerInTeam, Matchup, Player, MatchupLog, MatchupDetail,
                     ActionType, Pictures, Player, PlayerStatistics, PlayerInTeam)

from django.db.models import Func, F, IntegerField, Count, Avg
from datetime import datetime


def home(request):
    title = 'Последние обновления на сайте'
    template = 'index.html'
    photo = Pictures.objects.all().order_by('create_time')[0:10]
    context = {'title': title,
               'photo': photo}
    return render(request, template, context)


def visitor_menu(request):
    title = 'меню посетителя'
    template = 'visitor/visitor_menu.html'
    context = {'title': title}
    return render(request, template, context)


def players_main(request):
    title = 'список игроков'
    template = 'visitor/players_main.html'
    season_id = request.GET.get('season', '')
    team_name = request.GET.get('team', '')
    player_name = request.GET.get('playername', '')

    players_in_team = PlayerInTeam.objects.all()
    if season_id:
        players_in_team = players_in_team.filter(season__name=season_id)
    if team_name:
        players_in_team = players_in_team.filter(team__team_name=team_name)
    if player_name:
        players_in_team = players_in_team.filter(player__name__icontains=player_name)

    paginator = Paginator(players_in_team, 6)  # Show 10 players per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    seasons = Season.objects.all()
    teams = Team.objects.all()

    context = {
        'title': title,
        'page_obj': page_obj,
        'seasons': seasons,
        'teams': teams,
        'selected_season': season_id,
        'selected_team': team_name,
        'selected_player_name': player_name,
    }

    return render(request, template, context)


def player_detail(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    player_in_team = PlayerInTeam.objects.filter(player=player).last()

    # For demonstration purposes, let's assume these statistics are calculated elsewhere and provided.
    season_stats = PlayerStatistics.objects.filter(player=player, matchup__season__name='2016-2017')
    total_games_season = season_stats.count()
    season_ppg = season_stats.aggregate(avg_points=Avg('point'))['avg_points']
    season_apg = season_stats.aggregate(avg_assists=Avg('assist'))['avg_assists']
    season_rpg = season_stats.aggregate(avg_rebounds=Avg('rebound'))['avg_rebounds']

    season_stats_data = {
        'ppg': round(season_ppg, 2) if season_ppg else 0,
        'apg': round(season_apg, 2) if season_apg else 0,
        'rpg': round(season_rpg, 2) if season_rpg else 0
    }

    # Career stats calculation
    career_stats = PlayerStatistics.objects.filter(player=player)
    total_games_career = career_stats.count()
    career_ppg = career_stats.aggregate(avg_points=Avg('point'))['avg_points']
    career_apg = career_stats.aggregate(avg_assists=Avg('assist'))['avg_assists']
    career_rpg = career_stats.aggregate(avg_rebounds=Avg('rebound'))['avg_rebounds']

    career_stats_data = {
        'ppg': round(career_ppg, 2) if career_ppg else 0,
        'apg': round(career_apg, 2) if career_apg else 0,
        'rpg': round(career_rpg, 2) if career_rpg else 0
    }

    player_in_team.salary_million = str(int(player_in_team.salary))
    context = {
        'player': player,
        'player_in_team': player_in_team,
        'season_stats': season_stats_data,
        'career_stats': career_stats_data
    }

    return render(request, 'visitor/player_detail.html', context)


def teams_main(request):
    title = 'список команд'
    template = 'visitor/teams_main.html'
    teams = Team.objects.all()
    conference = Conference.objects.all()
    divisions = Division.objects.all()
    context = {
        'title': title,
        'teams': teams,
        'conference': conference,
        'divisions': divisions
    }
    return render(request, template, context)


def team_detail(request, team_id):
    template = 'visitor/team_detail.html'
    team = get_object_or_404(Team, team_id=team_id)
    players_in_team = PlayerInTeam.objects.filter(team=team)
    players_in_team = players_in_team.order_by('player__position')
    for player in players_in_team:
        player.salary_million = str(int(player.salary)) + ",000,000"
    seasons = Season.objects.all()
    title = team.team_name

    matchups = Matchup.objects.filter(team_away=team) | Matchup.objects.filter(team_home=team)
    matchups = matchups.order_by('start_time')
    context = {
        'title': title,
        'team': team,
        'seasons': seasons,
        'players_in_team': players_in_team,
        'matchups': matchups
    }
    return render(request, template, context)


def matchup_list(request):
    title = 'список игр'
    template = 'visitor/matchup_list.html'

    date = request.GET.get('date', '')
    matchups = Matchup.objects.all()

    if date:
        try:
            # Преобразование строки в объект datetime
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            # Фильтрация и сортировка по дате

            matchups = matchups.filter(start_time__date=date_obj.date()).order_by('start_time')
        except ValueError:
            # Обработка неправильного формата даты
            pass

    teams = Team.objects.all()

    paginator = Paginator(matchups, 6)  # Show 10 players per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': title,
        'teams': teams,
        'date': date,
        'matchups': matchups,
        'page_obj': page_obj
    }
    return render(request, template, context)


def matchup_detail(request, matchup_id):
    template = 'visitor/matchup_detail.html'

    matchup = get_object_or_404(Matchup, matchup_id=matchup_id)
    matchup_details = MatchupDetail.objects.filter(matchup=matchup).order_by('quarter')
    title = matchup
    team_home = matchup.team_home
    team_away = matchup.team_away
    log = MatchupLog.objects.filter(matchup=matchup)

    # log = log.annotate(
    #     hour=Func(F('occur_time'), 1, 2, function='SUBSTR', output_field=IntegerField()),
    #     minute=Func(F('occur_time'), 4, 2, function='SUBSTR', output_field=IntegerField())
    # ).order_by('hour', 'minute')

    total_away_score = sum(detail.team_away_score for detail in matchup_details)
    total_home_score = sum(detail.team_home_score for detail in matchup_details)
    team_away_OT1 = matchup.team_away_score - total_away_score
    team_home_OT1 = matchup.team_home_score - total_home_score

    home_action_counts_queryset = log.filter(team=team_home).values('action_type__name').annotate(
        count=Count('action_type')).order_by('action_type__name')

    # Annotate the logs to count each action type for team_away
    away_action_counts_queryset = log.filter(team=team_away).values('action_type__name').annotate(
        count=Count('action_type')).order_by('action_type__name')

    # Convert the querysets into dictionaries
    all_action_counts_name = list(ActionType.objects.values_list('name', flat=True))
    all_action_counts = {x.replace(' ', '_').replace('3-', 'Three_'): 0 for x in all_action_counts_name}

    home_action_counts = {(item['action_type__name']).replace(' ', '_').replace('3-', 'Three_'): item['count'] for item
                          in home_action_counts_queryset}

    away_action_counts = {(item['action_type__name']).replace(' ', '_').replace('3-', 'Three_'): item['count'] for item
                          in away_action_counts_queryset}

    for key, value in all_action_counts.items():

        if key not in home_action_counts:
            home_action_counts[key] = value
        if key not in away_action_counts:
            away_action_counts[key] = value
    try:
        team_away_three_proc = away_action_counts['Three_Points_Field_Goal_Made'] * 100 / (
                away_action_counts['Three_Points_Field_Goal_Made'] + away_action_counts[
            'Three_Points_Field_Goal_Missed'])
    except:
        team_away_three_proc = 0

    try:
        team_home_three_proc = home_action_counts['Three_Points_Field_Goal_Made'] * 100 / (
                home_action_counts['Three_Points_Field_Goal_Made'] + home_action_counts[
            'Three_Points_Field_Goal_Missed'])
    except:
        team_home_three_proc = 0

    try:
        team_away_goal_proc = away_action_counts['Field_Goal_Made'] * 100 / (
                away_action_counts['Field_Goal_Made'] + away_action_counts['Field_Goal_Missed'])
    except:
        team_away_goal_proc = 0
    try:
        team_home_goal_proc = home_action_counts['Field_Goal_Made'] * 100 / (
                home_action_counts['Field_Goal_Made'] + home_action_counts['Field_Goal_Missed'])
    except:
        team_home_goal_proc = 0

    score_details = {
        'team_away_OT1': team_away_OT1,
        'team_home_OT1': team_home_OT1,
        'team_away_three_proc': team_away_three_proc,
        'team_home_three_proc': team_home_three_proc,
        'team_away_goal_proc': team_away_goal_proc,
        'team_home_goal_proc': team_home_goal_proc,

    }

    start_team_away = PlayerInTeam.objects.filter(team=team_away, season=matchup.season, starter_index=1)
    start_team_home = PlayerInTeam.objects.filter(team=team_home, season=matchup.season, starter_index=1)
    start_details = {
        'start_team_away': start_team_away,
        'start_team_home': start_team_home
    }

    context = {
        'title': title,
        'matchup': matchup,
        'team_home': team_home,
        'team_away': team_away,
        'log': log,
        'matchup_details': matchup_details,
        'score_details': score_details,
        'start_details': start_details,
        'home_action_counts': home_action_counts,
        'away_action_counts': away_action_counts

    }
    return render(request, template, context)


def photos(request):
    title = 'фотографии'
    template = 'visitor/photos.html'
    photo = Pictures.objects.all()
    paginator = Paginator(photo, 16)  # Show 10 players per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': title,
        'page_obj': page_obj
    }
    return render(request, template, context)


def admin_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('nba:home')
                # return redirect('admin_dashboard')  # Replace with your admin dashboard URL
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    title = 'вход администратора'
    template = 'admin/admin_login.html'
    context = {'title': title,
               'form': form}
    return render(request, template, context)


def logout_view(request):
    logout(request)
    return redirect('nba:home')


def admin_dashboard(request):
    pass
