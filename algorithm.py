import pandas as pd

def calculateTime(current_time):
    time = ""

    time += str(7 + current_time//60)
    time += ":"
    time += str(current_time%60)

    return time


def main():

    passenger_arrivals = pd.read_csv('rail_data.csv')

    A_arrivals = passenger_arrivals['A'].tolist()
    print(A_arrivals)

    

    '''
    TrainNum = []
    TrainType = []
    A_ArrivalTime = []
    A_AvailCap = []
    A_Boarding = []
    B_ArrivalTime = []
    B_AvailCap = []
    B_Boarding = []
    C_ArrivalTime = []
    C_AvailCap = []
    C_Boarding = []
    U_Arrival = []
    U_AvailCap = []
    U_Offloading = []

    A_Passengers = [25,50,75,100,125,150,125,100,75,50,45,40,35,30,25,20,15,10,5]
    B_Passengers = [50,75,100,125,150,175,150,125,100,100,75,75,50,45,35,25,20,15,10]
    C_Passengers = [50,100,150,200,250,200,175,150,150,125,100,75,50,50,45,40,35,30,25]

    L4Trains = 4
    L8Trains = 12
    
    cur_time = 0

    A_remaining = 1100
    B_remaining = 1500
    C_remaining = 2000

    overflow = 0
    train_count = 0

    def addTrain(Station, P_TrainNum, P_TrainType, ArrivalTime, AvailCap, PossiblePassengers, X_remaining):
        index = P_TrainNum - 1
        
        if(Station == "A"):
            TrainNum[index] = P_TrainNum
            TrainType[index] = P_TrainType
            A_ArrivalTime[index] = ArrivalTime
            A_AvailCap[index] = AvailCap

            if(AvailCap == PossiblePassengers):
                A_Boarding[index] = AvailCap
                X_remaining -= AvailCap

            elif(AvailCap < PossiblePassengers):
                A_Boarding[index] = AvailCap
                X_remaining -= AvailCap
                A_Passengers[TrainNum + 1] += PossiblePassengers - AvailCap

            else:
                A_Boarding[index] = PossiblePassengers
                X_remaining -= PossiblePassengers

        elif(Station == "B"):
            TrainNum[index] = P_TrainNum
            TrainType[index] = P_TrainType
            B_ArrivalTime[index] = ArrivalTime
            B_AvailCap[index] = AvailCap
            
            if(AvailCap == PossiblePassengers):
                B_Boarding[index] = AvailCap
                X_remaining -= AvailCap

            elif(AvailCap < PossiblePassengers):
                B_Boarding[index] = AvailCap
                B_Passengers[TrainNum + 1] += PossiblePassengers - AvailCap
                X_remaining -= AvailCap

            else:
                B_Boarding[index] = PossiblePassengers
                X_remaining -= PossiblePassengers

        elif(Station == "C"):
            TrainNum[index] = P_TrainNum
            TrainType[index] = P_TrainType
            C_ArrivalTime[index] = ArrivalTime
            C_AvailCap[index] = AvailCap

            if(AvailCap == PossiblePassengers):
                C_Boarding[index] = AvailCap
                X_remaining -= AvailCap

            elif(AvailCap < PossiblePassengers):
                C_Boarding[index] = AvailCap
                C_Passengers[TrainNum + 1] += PossiblePassengers - AvailCap
                X_remaining -= AvailCap

            else:
                C_Boarding[index] = PossiblePassengers
                X_remaining -= PossiblePassengers

    ##### start

    # send a train straight to C
    addTrain("C", train_count + 1, "L4", calculateTime(17), 200, (C_Passengers[0] + C_Passengers[1]), C_remaining)
    train_count += 1
    L4Trains -= 1

    # send a train to A immediately after C leaves
    addTrain("A", train_count + 1, "L8", calculateTime(cur_time), 400, (A_Passengers[0] + A_Passengers[1]), A_remaining)
    train_count += 1
    L8Trains -= 1

    cur_time = 10

    ##### rush hour
    while(A_remaining > 1100/3 and B_remaining > 1500/3 and C_remaining > 2000/3):
        
        # if the current time ends with minute 8
        if(str(cur_time)[-1] == "0"):
            
            # calculate potential overflow
            overflow = (A_Passengers[cur_time/10] + B_Passengers[(cur_time/10)*2] + C_Passengers[(cur_time/10)*3] + overflow) - 400

            if(overflow >= 100):
                if(L4Trains > 0):
                    addTrain("A", train_count + 1, "L4", calculateTime(cur_time + 7), 200, A_Passengers[cur_time/10], A_remaining)
                    train_count += 1
                    L4Trains -= 1

                else:
                    addTrain("A", train_count + 1, "L8", calculateTime(cur_time + 7), 400, A_Passengers[cur_time/10], A_remaining)
                    train_count += 1
                    L8Trains -= 1

            addTrain("A", train_count + 1, "L8", calculateTime(cur_time - 2), 400, A_Passengers[cur_time/10], A_remaining)
            train_count += 1
            L8Trains -= 1

        cur_time += 10

    ##### final third
    # gary's algorithm to find groups
    smallNumGroup = 0
    largeNumGroup = 0
    smallGroup = 0
    largeGroup = 0
    slots = ((190 - cur_time)/10)
    trains = 16 - train_count
    i = slots

    #checking first for loop condition  
    while(i * trains >= slots):
        i = i - 1

    smallGroup = i+1
    largeGroup = i

    for j in range(slots + 1):
        if (smallGroup * j + largeGroup * (slots - j)) == trains:
            smallNumGroup = j
            largeNumGroup = (slots - j)
            break

    sendTime = 0
    
    for group1 in range(smallNumGroup):
        sendTime = cur_time + (10*(smallGroup-1))
        if(L8Trains > 0):
            addTrain("A", train_count + 1, "L8", calculateTime(sendTime), 400, A_Passengers[cur_time/10], A_remaining)
            train_count += 1
            L8Trains -= 1
        else:
            addTrain("A", train_count + 1, "L4", calculateTime(sendTime), 200, A_Passengers[cur_time/10], A_remaining)
            train_count += 1
            L4Trains -= 1
        
    for group2 in range(largeNumGroup):
        sendTime = cur_time + (10*(largeGroup-1))
        if(L8Trains > 0):
            addTrain("A", train_count + 1, "L8", calculateTime(sendTime), 400, A_Passengers[cur_time/10], A_remaining)
            train_count += 1
            L8Trains -= 1
        else:
            addTrain("A", train_count + 1, "L4", calculateTime(sendTime), 200, A_Passengers[cur_time/10], A_remaining)
            train_count += 1
            L4Trains -= 1



    schedule = pd.DataFrame(TrainNum, TrainType, A_ArrivalTime, A_AvailCap, A_Boarding, B_ArrivalTime, \
            B_AvailCap, B_Boarding, C_ArrivalTime, C_AvailCap, C_Boarding, U_Arrival, U_AvailCap, U_Offloading)

    print("hello, its meeeee")
    schedule.head()'''

if __name__ == "__main__":
    main()