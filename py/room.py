import random


class Room:

    def __init__(self, is_dirty, room_letter, neighbor_rooms, dirt_prob):
        self.is_dirty = is_dirty
        self.room_letter = room_letter
        self.neighbor_rooms = neighbor_rooms
        self.dirt_prob = dirt_prob

    def update_dirt(self):
        self.is_dirty = random.random() < self.dirt_prob

    def room_dirty(self):
        if self.is_dirty:
            return "D"
        else:
            return "C"

    # Getters and setters
    def get_is_dirty(self):
        return self.is_dirty

    def get_room_letter(self):
        return self.room_letter

    def get_neighbor_rooms(self):
        return self.neighbor_rooms

    def get_dirt_prob(self):
        return self.dirt_prob

    def set_is_dirty(self, is_dirty):
        self.is_dirty = is_dirty

    def set_room_letter(self, room_letter):
        self.room_letter = room_letter

    def set_neighbor_rooms(self, neighbor_rooms):
        self.neighbor_rooms = neighbor_rooms

    def set_dirt_prob(self, dirt_prob):
        self.dirt_prob = dirt_prob
