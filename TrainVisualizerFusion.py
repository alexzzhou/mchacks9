from ast import Global
import typing
import sys
import pandas as pd
import numpy as np
import pygame
import time
import math

pygame.init()

screen = pygame.display.set_mode((649, 451))
pygame.display.set_caption("Please Don't Make Me Wait")

bg = pygame.image.load('./assets/background2.jpg')
bg = pygame.transform.scale(bg, (649, 451))

font = pygame.font.Font('./assets/Manrope-Bold.ttf', 24)

Apos = (110, 126)
Bpos = (306, 126)
BCpos = (342, 194)
Cpos = (505, 205)
USpos = (515, 377)

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
        
        #display variables
        self.L4total = 4
        self.L8total = 12
        
        #averagetime, peopleatA, peopleatB, peopleatC, numofpeople at us or num of people people that got on train)


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
        if self.track.name not in ["A","B","C"]:
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



#def increment():

#Sends a train, starting at station A
def send_train(trains: typing.List[Train], type: str, glovar: 'GlobalVar', skips = []):
    if type == "L4":
        new_train = L4Train(skips)
        trains.append(new_train)
        glovar.L4total -= 1

    if type == "L8":
        new_train = L8Train(skips)
        trains.append(new_train)
        glovar.L8total -= 1

#Global variables of each station, linked in a linked list

US = Station("US", None)
CU = Track("CU", US, 11)
C = Station("C", CU)
BC = Track("BC", C, 9)
B = Station("B", BC)
AB = Track("AB", B, 8)
A = Station("A", AB)

def move(t):
    if t.track == A or t.track == None:
        return Apos
    elif t.track == B:
        return Bpos
    elif t.track == C:
        return Cpos
    elif t.track == AB:
        origin = Apos
        destination = Bpos
    elif t.track == CU:
        origin = Cpos
        destination = USpos
    elif t.track == BC:
        if t.time <= 2:
            origin = Bpos
            destination = BCpos
        else:
            x1, y1 = BCpos
            x2, y2 = Cpos
            return (((x2 - x1) / t.track.length) * (t.time - 2) +x1, ((y2 - y1) / t.track.length) * (t.time - 2)  + y1)
    elif t.track == AB:
        origin = Apos
        destination = Bpos
    else:
        return Apos
    x1, y1 = origin
    x2, y2 = destination
    return (((x2 - x1) / t.track.length) * (t.time+1) + x1, ((y2 - y1) / t.track.length) * (t.time+1) + y1)

def displayUI(t, l4, l8, av, ac, bc, cc, tc):
    clock = font.render(str((t // 60) + 7)+":"+f"{(t % 60):02d}", True, (0, 0, 0))
    traincount = font.render("L4: "+str(l4)+"/4   L8: "+str(l8)+"/12", True, (0, 0, 0))
    AvgWait = font.render("Average:"+ str("{:.2f}".format(av)) +"minutes", True, (0, 0, 0))
    AwaitingCount = font.render(str(ac), True, (0, 0, 0))
    BwaitingCount = font.render(str(bc), True, (0, 0, 0))
    CwaitingCount = font.render(str(cc), True, (0, 0, 0))
    TotalCount = font.render(str(tc)+"/4600", True, (0, 0, 0))
    US = font.render('Union Station', True, (0, 0, 0))

    clockR = clock.get_rect()
    traincountR = traincount.get_rect()
    AvgWaitR = AvgWait.get_rect()
    AWCR = AwaitingCount.get_rect()
    BWCR = BwaitingCount.get_rect()
    CWCR = CwaitingCount.get_rect()
    TCR = TotalCount.get_rect()
    USR = US.get_rect()

    clockR.center = (40, 436)
    traincountR.center = (100, 15)
    AvgWaitR.center = (500, 15)
    AWCR.center = (110, 155)
    BWCR.center = (306, 95)
    CWCR.center = (505, 180)
    TCR.center = (575, 436)
    USR.center = (565, 410)

    screen.blit(clock, clockR)
    screen.blit(traincount, traincountR)
    screen.blit(AvgWait, AvgWaitR)
    screen.blit(AwaitingCount, AWCR)
    screen.blit(BwaitingCount, BWCR)
    screen.blit(CwaitingCount, CWCR)
    screen.blit(TotalCount, TCR)
    screen.blit(US, USR)

def main():
    
    print("Starting Code")
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
    #====================================================================================
    while glovar.CURRENT_T < 230:
        
        


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

        while len(train_times) != 0 and glovar.CURRENT_T == train_times[0]:
            train_times.pop(0)
            
            train_values = schedule.pop(0)
            print(train_values)
            if len(train_values) == 3:
                send_train(all_trains, str(train_values[1]), glovar, [str(train_values[2])])
            elif len(train_values) == 4:
                send_train(all_trains, str(train_values[1]), glovar, [str(train_values[2]), str(train_values[3])])
            else:
                send_train(all_trains, str(train_values[1]), glovar)
        
        
        #loops through all the trains to update their position
        for i in all_trains:
            
                
            #checking if the train should skip a station
            if i.track.name in i.skips and i.time == 0:
                i.skip()

             #boarding passengers onto the train
            if i.time >= 0 and i.time < 3 and isinstance(i.track, Station) and i.size > 0:
                boarders = min(i.size, i.track.total)
                i.board(boarders)
                i.track.boardTrain(boarders, glovar)

            #incrementing
            i.increment()
            
            if i.track is US:
                all_trains.pop(0)

        #VISUALIZING
        screen.blit(bg, (0, 0))
        for t in all_trains:
            pos = move(t)  
            pygame.draw.circle(screen, (0, 0, 0), pos, 5)
        pygame.time.delay(100)
        #TO DO 
        avg_waittime = 0
        if glovar.BOARDEDPEEPS != 0:
            avg_waittime = glovar.WAITTIME/glovar.BOARDEDPEEPS

        displayUI(glovar.CURRENT_T, glovar.L4total, glovar.L8total, avg_waittime, stations[0].total,\
            stations[1].total, stations[2].total, glovar.BOARDEDPEEPS)
        pygame.display.flip()
        #VISUALIZING
            
           

        
        glovar.CURRENT_T += 1
        

    print("=============================================")
    print(glovar.WAITTIME)
    print(glovar.BOARDEDPEEPS)
    print("Average Wait Time: "+ str(glovar.WAITTIME/glovar.BOARDEDPEEPS))
    

if __name__ == "__main__":
    main()