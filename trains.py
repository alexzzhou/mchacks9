import pandas as pd
import numpy as np

class Train:
    pass

class L4Train(Train):
    def __init__(self, station, size, )

class L8Train(Train):
    pass

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

main:
