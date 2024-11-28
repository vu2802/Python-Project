import csv

class Player:
    def __init__(self, name, disks=None, moves=None, time=None, score=0):
        self.name = name
        self.disks = disks
        self.moves = moves
        self.time = time
        self.score = score

    def __repr__(self):
        return f"{self.name} - Score: {self.score}"

class PlayerManager:
    def __init__(self):
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def load_players(self, filename):
        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 2:  # Bỏ qua các dòng không hợp lệ
                        try:
                            score = int(row[1])
                        except ValueError:
                            score = 0
                        player = Player(row[0], None, None, None, score)
                        self.add_player(player)
        except FileNotFoundError:
            print(f"File {filename} not found. Starting with an empty scoreboard.")




    def save_players(self, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            for player in self.players:
                writer.writerow([player.name, player.score])  # Chỉ lưu tên và điểm số
 # Chỉ lưu tên và điểm số


    def find_player(self, name):
        for player in self.players:
            if player.name == name:
                return player
        return None

    # player_manager.py - update_player_score
    def update_player_score(self, name, new_score):
        player = self.find_player(name)
        if player and new_score > 0:
            if new_score > player.score:
                player.score = new_score

