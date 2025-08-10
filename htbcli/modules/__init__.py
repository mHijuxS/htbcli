"""
Modules package for HTB CLI
"""

from .machines import machines, MachinesModule
from .challenges import challenges, ChallengesModule
from .user import user, UserModule
from .season import season, SeasonModule
from .sherlocks import sherlocks, SherlocksModule
from .badges import badges, BadgesModule
from .career import career, CareerModule
from .connection import connection, ConnectionModule
from .fortresses import fortresses, FortressesModule
from .home import home, HomeModule
from .platform import platform, PlatformModule
from .prolabs import prolabs, ProlabsModule
from .pwnbox import pwnbox, PwnBoxModule
from .ranking import ranking, RankingModule
from .review import review, ReviewModule
from .starting_point import starting_point, StartingPointModule
from .team import team, TeamModule
from .tracks import tracks, TracksModule
from .universities import universities, UniversitiesModule
from .vm import vm, VMModule

__all__ = [
    'machines', 'MachinesModule',
    'challenges', 'ChallengesModule', 
    'user', 'UserModule',
    'season', 'SeasonModule',
    'sherlocks', 'SherlocksModule',
    'badges', 'BadgesModule',
    'career', 'CareerModule',
    'connection', 'ConnectionModule',
    'fortresses', 'FortressesModule',
    'home', 'HomeModule',
    'platform', 'PlatformModule',
    'prolabs', 'ProlabsModule',
    'pwnbox', 'PwnBoxModule',
    'ranking', 'RankingModule',
    'review', 'ReviewModule',
    'starting_point', 'StartingPointModule',
    'team', 'TeamModule',
    'tracks', 'TracksModule',
    'universities', 'UniversitiesModule',
    'vm', 'VMModule'
]
