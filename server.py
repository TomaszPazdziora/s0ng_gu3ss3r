
from random import randrange
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
        self.round_started_timestamp = 0
        self.paused = False
    
    def reset_round(self, socketio):
        self.songs_set = [
            rand_songs[randrange(len(rand_songs))]
            for _ in range(4)
        ]
        self.correct_ans = self.songs_set[3]

        # clear answered indications and activate game round
        self.round_active = True
        self._make_players_active()
        socketio.emit("reset_round_ind")
        self.round_started_timestamp = time.time()

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
        return True if time.time() - self.round_started_timestamp > TIME_FOR_ROUND else False

    def activate_server(self):
        self.active = True

    def pause_round(self):
        self.paused = True
        self.round_started_timestamp = time.time() - self.round_started_timestamp

    def resume_round(self):
        # resumes round with the same time delay
        self.paused = False
        self.round_started_timestamp = time.time() - self.round_started_timestamp

    def update_scoreboard(self):
        pass

    def get_player_score(self, username):
        idx = self._find_player_idx(username)
        score = 0
        if idx != NOT_FOUND:
            score = self.players[idx].score
        return score
    
    def emit_game_data(self, socketio):
        socketio.emit("new_songs", {
            "songs": self.songs_set,
            "time": round(TIME_FOR_ROUND - (time.time() - self.round_started_timestamp))
        })
    
    def emit_single_player_score(self, socketio, username, sid):
        socketio.emit("score_update", {"score": self.get_player_score(username)}, to=sid)

    def _make_players_active(self):
        for p in self.players:
            p.answered = False

    def _find_player_idx(self, username):
        idx = NOT_FOUND 
        for i in range(len(self.players)):
            if username == self.players[i].name:
                return i
        return idx
