class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_scores = self.load_high_scores()
        self.high_score = self.high_scores[0] if self.high_scores else 0

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def load_high_scores(self):
        try:
            with open("high_scores.txt", "r") as file:
                scores = {int(score.strip()) for score in file.readlines()}
                return sorted(scores, reverse=True)
        except FileNotFoundError:
            return []

    def save_high_scores(self):
        with open("high_scores.txt", "w") as file:
            for score in self.high_scores:
                file.write(f"{score}\n")

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score

        if self.score not in self.high_scores:
            self.high_scores.append(self.score)
            self.high_scores = sorted(set(self.high_scores), reverse=True)  
            self.save_high_scores()
