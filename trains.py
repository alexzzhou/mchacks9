import sys
import pandas as pd
import numpy as np

class Train:
    def __init___(self, track, size):
        self.track = track
        self.size = size
        self.time = 0

    def skip(self):
        if self.track != "A" or self.track != "B" or self.track != "C":
            print('ERROR: cannot skip if not at station.')
            return 1
        self.time = 0

    def increment(self):
        self.time += 1
        if self.track == "A" or self.track == "B" or self.track == "C":
            if self.time == 3:
                self

    def __str__(self):
        return f"Train at {self.track} \n \
            size: {self.size}\
            time: {self.time}"

class L4Train(Train):
    def __init__(self):
        self.track = "A"
        self.size = 200
        self.time = 0
        

class L8Train(Train):
    def __init__(self):
        self.track = "A"
        self.size = 400
        self.time = 0

class Station:
    pass

#You ned to know the location of passenger groups at each moment, but it shouldn't matter once they board the traim
class PassengerGroup:

    def __init__(self, station, size, arrival_time):
        self.station = station
        self.size = size
        self.arrival_time = arrival_time
        self.wait_time = 0

    def __str__(self):
        return f"Group arrived at {self.arrival_time} \n \
            size: {self.size}\
            station: {self.station}\
            current wait time: {self.wait_time}"

    def increment(self):
        self.wait_time += 1


def increment():
    
main:

