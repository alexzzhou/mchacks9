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
    pass

class L4Train(Train):
    def __init__(self, station, size, )

class L8Train(Train):
    pass

class Station:
    q_people = asy.Queue()
    def __init__(self, name, num_people, time_to_next):
	self.name = name
	self.num_people = num_people
	q_people.put((num_people, current_t))
	self.time_to_next = time_to_next
    
    def addPeople(num):
	self.num_people += num
    
    def getNumPeople():
	return self.num_people
    
    def getName():
	return self.name

    def getTimeToNext()
	return self.time_to_next

    def trainTake(train):
	

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

main:
