from random import randrange

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
    "Funk Factory"
]

class Server():
    def __init__(self):
        self.name = SERVER_NAMES[randrange(len(SERVER_NAMES))]