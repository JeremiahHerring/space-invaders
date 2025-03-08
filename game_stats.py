class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score = 0
        self.load_high_scores()

    def reset_stats(self):
        """Reset statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def load_high_scores(self):
        """Load high scores from a file."""
        try:
            with open("high_scores.txt", "r") as file:
                self.high_scores = [int(score.strip()) for score in file.readlines()]
                self.high_scores.sort(reverse=True) 
        except FileNotFoundError:
            self.high_scores = []

    def save_high_scores(self):
        """Save high scores to a file."""
        with open("high_scores.txt", "w") as file:
            for score in self.high_scores:
                file.write(f"{score}\n")

    def update_high_scores(self):
        """Update the high scores list with the current score."""
        if self.score > 0:
            self.high_scores.append(self.score)
            self.high_scores.sort(reverse=True)  
            self.high_scores = self.high_scores[:10] 
            self.save_high_scores() 