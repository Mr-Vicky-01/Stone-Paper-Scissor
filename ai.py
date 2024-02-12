import random


class Ai:
    def __init__(self):
        self.labels = ['Paper', 'Rock', 'Scissor']

    def get_random(self):
        ai_predicted = random.choice(self.labels)
        return ai_predicted

    def who_wins_logic(self, user_predicted):
        ai_predicted = self.get_random()
        if user_predicted == ai_predicted:
            return "Draw", ai_predicted
        elif user_predicted == "Rock" and ai_predicted == "Paper":
            return "AI Win", ai_predicted
        elif user_predicted == "Rock" and ai_predicted == "Scissor":
            return "You Won", ai_predicted
        elif user_predicted == "Paper" and ai_predicted == "Rock":
            return  "You Won", ai_predicted
        elif user_predicted == "Paper" and ai_predicted == "Scissor":
            return "AI Win", ai_predicted
        elif user_predicted == "Scissor" and ai_predicted == "Rock":
            return "AI Win", ai_predicted
        elif user_predicted == "Scissor" and ai_predicted == "Paper":
            return "You Won", ai_predicted
        else:
            return "error", ai_predicted

    def unbeatable_ai(self, user_predicted):
        if user_predicted == "Rock":
            ai_predicted = "Paper"
            return "AI Win", ai_predicted
        elif user_predicted == "Paper":
            ai_predicted = "Scissor"
            return "AI Win", ai_predicted
        elif user_predicted == "Scissor":
            ai_predicted = "Rock"
            return "AI Win", ai_predicted
