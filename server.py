from random import randrange, randint
import time

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

TIME_FOR_ROUND = 20
NOT_FOUND = -1
rand_songs = ['a', 'v', 'b', 'c', 'f', 'k', 'l', 'p']

class Server():
    def __init__(self):
        self.name = SERVER_NAMES[randrange(len(SERVER_NAMES))]
        self.players = []
        self.active = False
        self.correct_ans = -1
        self.songs_set = []
        self.round_active = False
        self.sec_elapsed = 0
    
    def load_songs(self):
        self.songs_set = [
            rand_songs[randrange(len(rand_songs))]
            for _ in range(3)
        ]
        self.correct_ans = self.songs_set[0]

        # clear answered indications and activate game round
        self.round_active = True
        self._make_players_active()
        self.sec_elapsed = time.time()

    def validate_answer(self, username, ans):
        if self.round_active:
            idx = self._find_player_idx(username)
            print(f"found idx: {idx}")
            if idx != NOT_FOUND and self.players[idx].answered is not True:
                self.players[idx].answered = True
                if ans == self.correct_ans:
                    self.players[idx].score += 1
                    self.round_active = False

    def is_round_time_elapsed(self):
        return True if time.time() - self.sec_elapsed > TIME_FOR_ROUND else False

    def activate_server(self):
        # when scoreboard is running and all players are ready
        self.active = True
        pass

    def update_scoreboard(self):
        pass
    
    def _make_players_active(self):
        for p in self.players:
            p.answered = False

    def _find_player_idx(self, username):
        idx = NOT_FOUND 
        for i in range(len(self.players)):
            if username == self.players[i].name:
                return i
        return idx
