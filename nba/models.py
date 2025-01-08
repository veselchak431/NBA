from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date

CURRENT_DATE = date(2017, 10, 5)


def validate_gender(value):
    if value not in ['F', 'M']:
        raise ValidationError("Gender must be 'F' or 'M'")


class Role(models.Model):
    role_id = models.CharField(max_length=1, primary_key=True)
    role_name = models.CharField(max_length=50)

    def __str__(self):
        return self.role_name


class Conference(models.Model):
    conference_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Division(models.Model):
    division_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=50)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    coach = models.CharField(max_length=50)
    abbr = models.CharField(max_length=3)
    stadium = models.CharField(max_length=100, blank=True, null=True)
    logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)

    def __str__(self):
        return self.team_name


class Country(models.Model):
    country_code = models.CharField(max_length=3, primary_key=True)
    country_name = models.CharField(max_length=50)

    def __str__(self):
        return self.country_name


class Position(models.Model):
    position_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    abbr = models.CharField(max_length=3)

    def __str__(self):
        return self.name


class Admin(AbstractUser):
    jobnumber = models.CharField(max_length=6, unique=True)
    gender = models.CharField(max_length=10, validators=[validate_gender])
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    REQUIRED_FIELDS = ['date_of_birth', 'role_id']

    def __str__(self):
        return self.username  # Or self.jobnumber or any other field you prefer to represent the admin

    class Meta:
        verbose_name = 'Administrator'
        verbose_name_plural = 'Administrators'


class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    join_year = models.DateField()
    height = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_birth = models.DateField(blank=True, null=True)
    college = models.CharField(max_length=50, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='player_images/', blank=True, null=True)
    is_retirement = models.BooleanField()
    retirement_time = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

    def calculate_experience(self, current_date=CURRENT_DATE):

        if current_date is None:
            current_date = timezone.now().date()

        if self.is_retirement and self.retirement_time:
            end_date = self.retirement_time
        else:
            end_date = current_date

        if self.join_year is None:
            start_date = end_date
        else:
            start_date = self.join_year

        experience_years = end_date.year - start_date.year - (
                (end_date.month, end_date.day) < (start_date.month, start_date.day))

        return experience_years


class Season(models.Model):
    season_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class MatchupType(models.Model):
    matchup_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Matchup(models.Model):
    matchup_id = models.AutoField(primary_key=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    matchup_type = models.ForeignKey(MatchupType, on_delete=models.CASCADE)
    team_away = models.ForeignKey(Team, related_name='team_away', on_delete=models.CASCADE)
    team_home = models.ForeignKey(Team, related_name='team_home', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    team_away_score = models.IntegerField()
    team_home_score = models.IntegerField()
    location = models.CharField(max_length=200, blank=True, null=True)
    status = models.IntegerField()
    current_quarter = models.CharField(max_length=50, blank=True, null=True)

    def status_description(self):
        if self.status == -1:
            return "Not started"
        elif self.status == 0:
            return "Running"
        elif self.status == 1:
            return "Finished"

    def __str__(self):
        return f"{self.team_away} vs {self.team_home} - {self.start_time}"


class PlayerInTeam(models.Model):
    player_in_team_id = models.AutoField(primary_key=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    shirt_number = models.CharField(max_length=10)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    starter_index = models.IntegerField()

    def __str__(self):
        return f"{self.player} in {self.team} - {self.season}"


class PlayerStatistics(models.Model):
    id = models.AutoField(primary_key=True)
    matchup = models.ForeignKey(Matchup, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    is_starting = models.IntegerField()
    min = models.DecimalField(max_digits=10, decimal_places=2)
    point = models.IntegerField()
    assist = models.IntegerField()
    field_goal_made = models.IntegerField()
    field_goal_missed = models.IntegerField()
    three_point_field_goal_made = models.IntegerField()
    three_point_field_goal_missed = models.IntegerField()
    free_throw_made = models.IntegerField()
    free_throw_missed = models.IntegerField()
    rebound = models.IntegerField()
    offr = models.IntegerField()
    dffr = models.IntegerField()
    steal = models.IntegerField()
    block = models.IntegerField()
    turnover = models.IntegerField()
    foul = models.IntegerField()

    def __str__(self):
        return f"{self.player} - {self.matchup}"


class MatchupDetail(models.Model):
    id = models.AutoField(primary_key=True)
    matchup = models.ForeignKey(Matchup, on_delete=models.CASCADE)
    quarter = models.IntegerField()
    team_away_score = models.IntegerField()
    team_home_score = models.IntegerField()

    def __str__(self):
        return f"Matchup {self.matchup} - Quarter {self.quarter}"


class MatchupLog(models.Model):
    id = models.AutoField(primary_key=True)
    matchup = models.ForeignKey(Matchup, on_delete=models.CASCADE)
    quarter = models.IntegerField()
    occur_time = models.CharField(max_length=10)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    action_type = models.ForeignKey('ActionType', on_delete=models.CASCADE)
    remark = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return f"Log {self.matchup} - Quarter {self.quarter} - {self.occur_time}"


class ActionType(models.Model):
    action_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class PostSeason(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    rank = models.IntegerField()

    class Meta:
        unique_together = (('team', 'season'),)

    def __str__(self):
        return f"{self.team} - {self.season} - Rank {self.rank}"


class Pictures(models.Model):
    id = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to='pictures/')
    description = models.CharField(max_length=50, blank=True, null=True)
    number_of_like = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Picture {self.id} - {self.description}"
