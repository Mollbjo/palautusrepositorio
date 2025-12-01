LOVE = 0
FIFTEEN = 1
THIRTY = 2
FORTY = 3
ENDGAME_THRESHOLD = 4
ADVANTAGE_MARGIN = 1
WIN_MARGIN = 2


class TennisGame:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_score = LOVE
        self.player2_score = LOVE

    def won_point(self, player_name):
        if player_name == "player1":
            self.player1_score = self.player1_score + 1
        else:
            self.player2_score = self.player2_score + 1

    def _score_name(self, numeric_score):
        names = {
            LOVE: "Love",
            FIFTEEN: "Fifteen",
            THIRTY: "Thirty",
            FORTY: "Forty",
        }
        return names.get(numeric_score, "Unknown")

    def _tied_score_text(self, score_value):
        if score_value in (LOVE, FIFTEEN, THIRTY):
            return f"{self._score_name(score_value)}-All"
        return "Deuce"

    def _endgame_score_text(self):
        difference = self.player1_score - self.player2_score
        if difference == ADVANTAGE_MARGIN:
            return "Advantage player1"
        if difference == -ADVANTAGE_MARGIN:
            return "Advantage player2"
        if difference >= WIN_MARGIN:
            return "Win for player1"
        return "Win for player2"

    def _running_score_text(self):
        return f"{self._score_name(self.player1_score)}-{self._score_name(self.player2_score)}"

    def get_score(self):
        if self.player1_score == self.player2_score:
            return self._tied_score_text(self.player1_score)
        if self.player1_score >= ENDGAME_THRESHOLD or self.player2_score >= ENDGAME_THRESHOLD:
            return self._endgame_score_text()
        return self._running_score_text()
