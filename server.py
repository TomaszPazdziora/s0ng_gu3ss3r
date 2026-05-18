from random import randrange, randint

SERVER_NAMES = [
    "Metal Cave",
    "Jazz Club",
    "Pop Festival",
    "Punk Pit",
    "Rock Arena",
    "Blues Basement",
    "Disco Dungeon",
    "Techno Temple",
    "Indie Garage",
    "Rap Rooftop",
    "LoFi Lounge",
    "Hardcore Hangar",
    "Funk Factory",
    "Opera House",
]

rand_songs = ['a', 'v', 'b', 'c', 'f', 'k', 'l', 'p']

class Server():
    def __init__(self):
        self.name = SERVER_NAMES[randrange(len(SERVER_NAMES))]
        self.players = []
        self.active = False
        self.correct_ans = -1
        self.songs_set = []
        self.round_active = False
    
    def load_songs(self):
        self.songs_set = [
            rand_songs[randrange(len(rand_songs))]
            for _ in range(3)
        ]
        self.correct_ans = self.songs_set[0]

    def validate_answer(self):
        # check answers
        pass

    def activate_server(self):
        # when scoreboard is running and all players are ready
        self.active = True
        self.round_active = True
        pass

    def update_scoreboard(self):
        pass

