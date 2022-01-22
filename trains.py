import sys
import pandas as pd
import numpy as np
import asyncio as asy

CURRENT_T = (7,0)
PEAK = 10
TOTALPEOPLE = 4600
PEOPLEA = 1100
PEOPLEB = 1500
PEOPLEC = 2000


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

class Track:
    def __init__(self):
        pass

class Station:
    q_people = asy.Queue()
    
    def __init__(self, name, num_people, time_to_next):
        self.name = name
        self.num_people = num_people
        q_people.put((num_people, current_t))
        self.time_to_next = time_to_next
    
    def addPeople(self, num):
	    self.num_people += num

    def getNumPeople(self):
	    return self.num_people
    
    def getName(self):
	    return self.name

    def getTimeToNext(self):
	    return self.time_to_next

    def trainTake(train):
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


#def increment():

A = Station()
AB = Track()
B = Station()
BC = Track ()
C = Station()

TRACK = [A, AB, B, BC, C]

def main():

    
