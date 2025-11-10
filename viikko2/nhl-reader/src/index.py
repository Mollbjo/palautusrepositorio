
from rich.table import Table
from rich.console import Console
import requests
from player import Player

def get_season_and_nationality():
 season = input("Enter NHL season (example: 2024-25): ")
 nationality = input("Enter nationality (example: FIN): ")
 return season, nationality

def display_players(players, nationality, season):
 console = Console()
 table = Table(title=f"Top NHL Players from {nationality} ({season})")
 for col, opts in [
  ("Name", {"style": "cyan"}),
  ("Team", {"style": "magenta"}),
  ("Games", {"justify": "right"}),
  ("Goals", {"justify": "right"}),
  ("Assists", {"justify": "right"}),
  ("Points", {"justify": "right"}),
 ]:
  table.add_column(col, **opts)
 for player in players:
  table.add_row(
   player.name,
   player.team,
   str(player.games),
   str(player.goals),
   str(player.get_assists()),
   str(player.points),
  )
 console.print(table)

def fetch_players_by_nationality(url, nationality):
 reader = PlayerReader(url)
 stats = PlayerStats(reader)
 return stats.top_scorers_by_nationality(nationality)

def main():
 season, nationality = get_season_and_nationality()
 url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
 players = fetch_players_by_nationality(url, nationality)
 display_players(players, nationality, season)

class PlayerReader:
 def __init__(self, url):
  self.url = url

 def get_players(self):
  response = requests.get(self.url, timeout=10).json()
  print("JSON-muotoinen vastaus:")
  print(response)
  players = []
  for player_dict in response:
   player = Player(player_dict)
   players.append(player)
  return players

 def get_url(self):
  return self.url

class PlayerStats:
 def __init__(self, reader: PlayerReader):
  self.players = reader.get_players()

 def top_scorers_by_nationality(self, nationality: str):
  nationality_filter = [player for player in self.players if player.nationality == nationality]
  nationality_filter.sort(key=lambda player: player.points, reverse=True)
  return nationality_filter

 def get_player_count(self):
  return len(self.players)

if __name__ == "__main__":
 main()
