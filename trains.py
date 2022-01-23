from ast import Global
import typing
import sys
import pandas as pd
import numpy as np

#Global variables containing important overall information (waittimes and total boarded people)
class GlobalVar:
    def __init__(self):
        self.CURRENT_T = 0
        self.PEAK = 10
        self.TOTALPEOPLE = 4600
        self.PEOPLEA = 1100
        self.PEOPLEB = 1500
        self.PEOPLEC = 2000
        self.BOARDEDPEEPS = 0
        self.WAITTIME = 0

#Represents either a track between stations or a station itself. 
class Track:
    def __init__(self, name: str, next: 'Track', length: int):
        self.name = name
        self.next = next
        self.length = length

    def __str__(self):
        return f"Track {self.name}"
        
#Abstract class 
class Train:
    def __init___(self, track: Track, size: int, skips: typing.List[str]):
        self.track = track
        self.size = size
        self.time = 0
        self.skips = skips

    def skip(self):
        if self.track.name != "A" or self.track.name != "B" or self.track.name != "C":
            print('ERROR: cannot skip if not at station.')
            return 1
        self.time = 0
        self.track = self.track.next

    def increment(self):
        self.time += 1
        if self.time == self.track.length:
            self.track = self.track.next
            self.time = 0
            

    def board(self, group_size: int):
        if group_size > self.size: 
            print("ERROR: Size overflow. Cannot board a group larger than " + self.size)
            return 1
        else:
            self.size -= group_size

    def __str__(self):
        return f"Train at {self.track}\nsize: {self.size}\ntime: {self.time}"


class L4Train(Train):
    def __init__(self, skips = []):
        self.track = A
        self.size = 200
        self.time = 0
        self.skips = skips
        

class L8Train(Train):
    def __init__(self, skips = []):
        self.track = A
        self.size = 400
        self.time = 0
        self.skips = skips

#You ned to know the location of passenger groups at each moment, but it shouldn't matter once they board the train
#Represents a group of people that arrive at a station at the same time
#IGNORE wait_time, will remove
class PassengerGroup:

    def __init__(self, size: int, arrival_time: int):
        self.size = size
        self.arrival_time = arrival_time
        self.wait_time = 0

    def __str__(self):
        return f"Group arrived at {self.arrival_time}\nsize: {self.size}\ncurrent wait time: {self.wait_time}"

    def increment(self):
        self.wait_time += 1

    def subtract(self, people: int):
        if self.size < people:
            print("ERROR: cannot remove more than " + self.size)
            return 1
        else:
            self.size -= people


#Child class of track, handles train boarding
class Station(Track):
 
    def __init__(self, name: str, next: 'Track'):
        self.name = name
        self.next = next
        self.length = 3
        self.groups = []
        self.total = 0
    
    def __str__(self):
        return f"Station: {self.name}\ncurrent total: {self.total}"

    #adds a group of people that arrive at the same time to a station
    def addGroup(self, group: 'PassengerGroup'):
        self.groups.append(group)
        self.total += group.size

    #Determines how many of its groups can fit on a given train, and moves groups into the train
    #updates global waitime and boarded people
    def boardTrain(self, people: int, glovar: GlobalVar):
        if len(self.groups) == 0:
            return
        while people != 0 and self.total != 0:
            if people < self.groups[0].size:
                
                self.groups[0].size -= people
                self.total -= people
                glovar.BOARDEDPEEPS += people
                glovar.WAITTIME += people*(glovar.CURRENT_T-self.groups[0].arrival_time)

            if people >= self.groups[0].size:
                
                glovar.BOARDEDPEEPS += self.groups[0].size
                glovar.WAITTIME += self.groups[0].size*(glovar.CURRENT_T-self.groups[0].arrival_time)
                people -= self.groups[0].size
                self.total -= self.groups[0].size
                self.groups.pop(0)

            
            print(glovar.BOARDEDPEEPS)
            print(glovar.WAITTIME)
                


#def increment():

#Sends a train, starting at station A
def send_train(trains: typing.List[Train], type: str, skips = []):
    if type == "L4":
        new_train = L4Train(skips)
        trains.append(new_train)

    if type == "L8":
        new_train = L8Train(skips)
        trains.append(new_train)

#Global variables of each station, linked in a linked list
C = Station("C", None)
BC = Track("BC", C, 9)
B = Station("B", BC)
AB = Track("AB", B, 8)
A = Station("A", AB)


def main():
    
    stations = [A, B, C]
    #Setting up global variables
    glovar = GlobalVar()

    #getting train schedule from csv file
    schedule = pd.read_csv(sys.argv[1])
    train_times = schedule.iloc[:,0].tolist()

    #print(train_times)
    schedule = schedule.to_numpy().tolist()
    #print(schedule[0])

    #getting passenger schedule from csv file
    passenger_schedule = pd.read_csv(sys.argv[2])
    passenger_times = passenger_schedule.iloc()[:,0].tolist()

    passenger_schedule = passenger_schedule.to_numpy().tolist()

    #all trains currently running through the track that have not made it past station C
    all_trains = []

    #main loop
    while glovar.CURRENT_T < 3:
        
        #checking if at the current increment passengers should the added to the stations
        if len(passenger_times) == 0:
            pass
        elif glovar.CURRENT_T == passenger_times[0]:
            passenger_times.pop(0)
            pass_values = passenger_schedule.pop(0)
            
            for i in range(len(stations)):
                new_group = PassengerGroup(pass_values[i+1], glovar.CURRENT_T)
                stations[i].addGroup(new_group)

        #checking if at the current increment a train should be sent
        if len(train_times) == 0:
            pass
        else:
            while glovar.CURRENT_T == train_times[0]:
                train_times.pop(0)
                train_values = schedule.pop(0)
                if len(train_values) == 3:
                    send_train(all_trains, str(train_values[1]), [str(train_values[2])])
                elif len(train_values) == 4:
                    send_train(all_trains, str(train_values[1]), [str(train_values[2]), str(train_values[3])])
                else:
                    send_train(all_trains, str(train_values[1]))
        
        #loops through all the trains to update their position
        for i in all_trains:

            #checking if the train has finished at C
            if i.track.next == None:
                all_trains.pop(0)
            
            #checking if the train should skip a station
            if i.track.name in i.skips and i.time == 0:
                i.skip()

            i.increment()
            
            #boarding passengers onto the train
            if i.time >= 0 and i.time < 3 and isinstance(i.track, Station) and i.size != 0:
                boarders = min(i.size, i.track.total)
                i.board(boarders)
                i.track.boardTrain(boarders, glovar)

        
        glovar.CURRENT_T += 1
        

    print("=============================================")
    print(glovar.WAITTIME)
    print(glovar.BOARDEDPEEPS)
    print("Average Wait Time: "+ str(glovar.WAITTIME/glovar.BOARDEDPEEPS))

    # for i in stations:
    #     print(i)
    #     for j in i.groups: 
    #         print(j)

    for i in all_trains:
        print(i)
    

if __name__ == "__main__":
    main()