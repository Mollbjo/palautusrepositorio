import unittest
from statistics_service import StatisticsService, SortBy
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_correct_player(self):
        player = self.stats.search("Kurri")
        self.assertEqual(player.name, "Kurri")
        self.assertEqual(player.team, "EDM")
        self.assertEqual(player.goals, 37)

    def test_unknown_player(self):
        player = self.stats.search("Selänne")
        self.assertIsNone(player)

    def test_team_players(self):
        players_from_edm = self.stats.team("EDM")
        self.assertEqual(len(players_from_edm),3)
        players_names = [p.name for p in players_from_edm]
        self.assertIn("Gretzky", players_names)
        self.assertIn("Semenko",players_names)
        self.assertIn("Kurri", players_names)

    def test_top_scorers_amount(self):
        top_players = self.stats.top(3)
        self.assertEqual(len(top_players), 3)

    def test_top_scorers_names(self):
        top_players = self.stats.top(3)
        top_score_players = [p.name for p in top_players]
        self.assertEqual(top_score_players[0], "Gretzky")
        self.assertEqual(top_score_players[1], "Lemieux")
        self.assertEqual(top_score_players[2], "Yzerman")
    
    ##def test_top_with_zero_players(self):
        ##top_players = self.stats.top(0)
        ##self.assertEqual(len(top_players), 1)

    def test_top_scorers_by_points(self):
        top_players = self.stats.top(3, SortBy.POINTS)
        top_score_players = [p.name for p in top_players]
        self.assertEqual(top_score_players[0], "Gretzky")
        self.assertEqual(top_score_players[1], "Lemieux")
        self.assertEqual(top_score_players[2], "Yzerman")

    def test_top_scorers_by_goals(self):
        top_players = self.stats.top(3, SortBy.GOALS)
        top_goal_players = [p.name for p in top_players]
        self.assertEqual(top_goal_players[0], "Lemieux")
        self.assertEqual(top_goal_players[1], "Yzerman")
        self.assertEqual(top_goal_players[2], "Kurri")

    def test_top_scorers_by_assists(self):
        top_players = self.stats.top(3, SortBy.ASSISTS)
        top_assist_players = [p.name for p in top_players]
        self.assertEqual(top_assist_players[0], "Gretzky")
        self.assertEqual(top_assist_players[1], "Yzerman")
        self.assertEqual(top_assist_players[2], "Lemieux")
