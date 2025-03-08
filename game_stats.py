class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score = self.load_high_score()

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                high_scores = [int(score.strip()) for score in file.readlines()]
                if high_scores:
                    return max(high_scores)  
        except FileNotFoundError:
            pass
        return 0

    def save_high_score(self):
        with open("high_scores.txt", "a") as file:
            file.write(f"{self.high_score}\n")
            print("score saved")

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
        self.save_high_score()  
