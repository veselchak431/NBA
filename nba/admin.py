from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Admin
from .models import Role, Conference, Division, Team, Country, Position, Admin, Player, Season, MatchupType, \
    Matchup, PlayerInTeam, PlayerStatistics, MatchupDetail, MatchupLog, ActionType, PostSeason, Pictures


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('jobnumber', 'gender', 'date_of_birth', 'phone', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('jobnumber', 'gender', 'date_of_birth', 'phone', 'role')}),
    )


admin.site.register(Admin, CustomUserAdmin)

from django.contrib import admin
from .models import Role, Conference, Division, Team, Country, Position, Admin, Player, Season, MatchupType, \
    Matchup, PlayerInTeam, PlayerStatistics, MatchupDetail, MatchupLog, ActionType, PostSeason, Pictures

# Register your models here.
admin.site.register(Role)
admin.site.register(Conference)
admin.site.register(Division)
admin.site.register(Team)
admin.site.register(Country)
admin.site.register(Position)
admin.site.register(Player)
admin.site.register(Season)
admin.site.register(MatchupType)
admin.site.register(Matchup)
admin.site.register(PlayerInTeam)
admin.site.register(PlayerStatistics)
admin.site.register(MatchupDetail)
admin.site.register(MatchupLog)
admin.site.register(ActionType)
admin.site.register(PostSeason)
admin.site.register(Pictures)