import requests
from player import Player
from rich.table import Table
from rich.console import Console

def main():
    season = input("Enter NHL season (example: 2024-25): ")
    nationality = input("Enter nationality code (example: FIN): ")
    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    players = stats.top_scorers_by_nationality(nationality)

    console = Console()
    table = Table(title=f"Top NHL Players from {nationality} ({season})")
    table.add_column("Name", style="cyan")
    table.add_column("Team", style="magenta")
    table.add_column("Games", justify="right")
    table.add_column("Goals", justify="right")
    table.add_column("Assists", justify="right")
    table.add_column("Points", justify="right")

    for player in players:
        table.add_row(
            player.name,
            player.team,
            str(player.games),
            str(player.goals),
            str(player.assists),
            str(player.points)
        )
    console.print(table)

class PlayerReader:
    def __init__ (self, url):
        self.url = url
    
    def get_players(self):
        response = requests.get(self.url).json()
        print("JSON-muotoinen vastaus:")
        print(response)

        players = []

        for player_dict in response:
            player = Player(player_dict)
            players.append(player)
        return players
    
class PlayerStats:
    def __init__ (self, reader: PlayerReader):
        self.players = reader.get_players()

    def top_scorers_by_nationality(self, nationality: str):
        nationality_filter = [player for player in self.players if player.nationality == nationality]
        nationality_filter.sort(key=lambda player: player.points, reverse=True)
        return nationality_filter

if __name__ == "__main__":
    main()