class Player:
 def __init__(self, player_dict):
  self.name = player_dict['name']
  self.nationality = player_dict['nationality']
  self.goals = player_dict['goals']
  self.team = player_dict['team']
  self.games = player_dict['games']
  self._assists = player_dict['assists']
  self._id = player_dict['id']

 def __str__(self):
  return f" {self.name:20} {self.team:20} {self.goals} + {self._assists} = {self.points}"

 @property
 def points(self):
  return self.goals + self._assists

 def get_id(self):
  return self._id

 def get_assists(self):
  return self._assists
