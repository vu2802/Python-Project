import csv
class Player:
    def __init__(self, name, disks, moves, time, score):
        self.name = name
        self.disks = disks
        self.moves = moves
        self.time = time
        self.score = score

    def __repr__(self):
        return (f"{self.name} - {self.disks} disks - {self.moves} moves - "
                f"{self.time} seconds - {self.score} points")

class PlayerManager:
    def __init__(self):
        self.players = []  

    def add_player(self, player):
        self.players.append(player)

    def load_players(self, filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                player = Player(row[0], int(row[1]), int(row[2]), float(row[3]), int(row[4]))
                self.add_player(player)

    def save_players(self, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            for player in self.players:
                writer.writerow([player.name, player.disks, player.moves, player.time, player.score])

    def show_players(self):
        for player in self.players:
            print(player)

    def sort_players(self):
        self.players.sort(key=lambda x: (x.disks, x.score), reverse=True)

    def find_player(self, name):
        for player in self.players:
            if player.name == name:
                return player
        return None



