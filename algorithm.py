from this import d
import pandas as pd

output_file = pd.read_csv("~/desktop/mchacks9/output_format.csv")
passenger_arrivals = pd.read_csv("~/desktop/mchacks9/testing/rail_data.csv")

A_arrivals = passenger_arrivals['A'].tolist()
B_arrivals = passenger_arrivals['B'].tolist()
C_arrivals = passenger_arrivals['C'].tolist()

A_overflow = 0
B_overflow = 0
C_overflow = 0

A_total = sum(A_arrivals)
B_total = sum(B_arrivals)
C_total = sum(C_arrivals)

A_remaining = A_total
B_remaining = B_total
C_remaining = C_total

L4Trains = 4
L8Trains = 12

train_count = 0

def calculateTime(current_time):
    time = ""

    hours = 7 + (current_time//60)
    minutes = (current_time % 60)

    string_minutes = ""

    if (minutes < 10):
        string_minutes = "0" + str(minutes)
    else:
        string_minutes = str(minutes)

    time += str(hours) + ":" + string_minutes

    return time

def arrivalsAtTime(cur_time, station):
    
    if(station == "A"):
        if(cur_time == 0):
            return A_arrivals[0]
        elif(str(cur_time)[-1] == "0"):
            return A_arrivals[(cur_time - 1)//10]
        else:
            return A_arrivals[cur_time//10]
        
    elif(station == "B"):
        if(cur_time == 0):
            return B_arrivals[0]
        elif(str(cur_time)[-1] == "0"):
            return B_arrivals[(cur_time - 1)//10]
        else:
            return B_arrivals[cur_time//10]

    elif(station == "C"):
        if(cur_time == 0):
            return C_arrivals[0]
        elif(str(cur_time)[-1] == "0"):
            return C_arrivals[(cur_time - 1)//10]
        else:
            return C_arrivals[cur_time//10]

def clearStation(cur_time, station):
    if(station == "A"):
        if(cur_time == 0):
            A_arrivals[0] = 0
        elif(str(cur_time)[-1] == "0"):
            A_arrivals[(cur_time - 1)//10] = 0
        else:
            A_arrivals[cur_time//10] = 0
        
    elif(station == "B"):
        if(cur_time == 0):
            B_arrivals[0] = 0
        elif(str(cur_time)[-1] == "0"):
            B_arrivals[(cur_time - 1)//10] = 0
        else:
            B_arrivals[cur_time//10] = 0

    elif(station == "C"):
        if(cur_time == 0):
            C_arrivals[0] = 0
        elif(str(cur_time)[-1] == "0"):
            C_arrivals[(cur_time - 1)//10] = 0
        else:
            C_arrivals[cur_time//10] = 0

def updateOverflow(cur_time, station):
    global A_overflow, B_overflow, C_overflow

    if(station == "A"):
        A_overflow += arrivalsAtTime(cur_time, "A")
        clearStation(cur_time, "A")

    elif (station == "B"):
        B_overflow += arrivalsAtTime(cur_time, "B")
        clearStation(cur_time, "B")

    elif (station == "C"):
        C_overflow += arrivalsAtTime(cur_time, "C")
        clearStation(cur_time, "C")

def addTrain(cur_time, train_type, skips):
        global L4Trains, L8Trains
        global A_remaining, B_remaining, C_remaining
        global A_overflow, B_overflow, C_overflow
        global output_file
        global train_count

        passengers_at_station = 0

        if(train_type == "L4"):
            L4Trains -= 1
            a_avail_cap = 200
        else:
            L8Trains -= 1
            a_avail_cap = 400

        a_arrival = cur_time
        a_boarding = 0

        b_arrival = 0
        b_avail_cap = a_avail_cap
        b_boarding = 0

        c_arrival = 0
        c_avail_cap = b_avail_cap
        c_boarding = 0

        u_arrival = 0
        u_avail_cap = c_avail_cap
        u_boarding = 0

        # at station A
        if "A" not in skips:
            cur_time += 3
            b_arrival = a_arrival + 8 + 3

            passengers_at_station = arrivalsAtTime(cur_time, "A") + A_overflow

            # if available cap is less than equal to passengers wanting a ride
            if(a_avail_cap <= passengers_at_station):
                a_boarding = a_avail_cap
                A_overflow = passengers_at_station - a_boarding

            # if available cap is greater than passengers wanting a ride
            else:
                a_boarding = passengers_at_station
                A_overflow = 0

            # updating number of people waiting
            A_remaining -= a_boarding
        else:
            A_overflow += arrivalsAtTime(cur_time, "A")
            b_arrival = a_arrival + 8
        #
        clearStation(cur_time, "A")
        updateOverflow(cur_time, "B")
        updateOverflow(cur_time, "C")
        #
        b_avail_cap = a_avail_cap - a_boarding
        cur_time += 8

        # at station B
        if "B" not in skips and b_avail_cap != 0:
            cur_time += 3
            c_arrival = b_arrival + 9 + 3

            passengers_at_station = arrivalsAtTime(cur_time, "B") + B_overflow

            # if available cap is less than equal to passengers wanting a ride
            if(b_avail_cap <= passengers_at_station):
                b_boarding = b_avail_cap
                B_overflow = passengers_at_station - b_boarding

            # if available cap is greater than passengers wanting a ride
            else:
                b_boarding = passengers_at_station
                B_overflow = 0

            # updating number of people waiting
            B_remaining -= b_boarding
        else:
            B_overflow += arrivalsAtTime(cur_time, "B")
            c_arrival = b_arrival + 9
        #
        clearStation(cur_time, "B")
        updateOverflow(cur_time, "C")
        #
        c_avail_cap = b_avail_cap - b_boarding
        cur_time += 9

        # at station C
        if c_avail_cap != 0:
            cur_time += 3
            u_arrival = c_arrival + 11 + 3

            passengers_at_station = arrivalsAtTime(cur_time, "C") + C_overflow

            # if available cap is less than equal to passengers wanting a ride
            if(c_avail_cap <= passengers_at_station):
                c_boarding = c_avail_cap
                C_overflow = passengers_at_station - c_boarding

            # if available cap is greater than passengers wanting a ride
            else:
                c_boarding = passengers_at_station
                C_overflow = 0

            # updating the number of people waiting
            C_remaining -= c_boarding
        else:
            C_overflow += arrivalsAtTime(cur_time, "C")
            u_arrival = c_arrival + 11
        #
        clearStation(cur_time, "C")
        #
        u_avail_cap = c_avail_cap - c_boarding
        cur_time += 11

        u_offboarding = a_boarding + b_boarding + c_boarding

        tempDF = pd.DataFrame([[train_count + 1, train_type, calculateTime(a_arrival), a_avail_cap, a_boarding, calculateTime(b_arrival), b_avail_cap, b_boarding, calculateTime(c_arrival), c_avail_cap, c_boarding, calculateTime(u_arrival), u_avail_cap, u_offboarding]])
       
        print('\n'.join(tempDF.to_string(index = False).split('\n')[1:]))


        tempDF.columns = ['TrainNum', 'TrainType', 'A_ArrivalTime', 'A_AvailCap', 'A_Boarding', 'B_ArrivalTime', 'B_AvailCap', 'B_Boarding', 'C_ArrivalTime', 'C_AvailCap', 'C_Boarding', 'U_Arrival', 'U_AvailCap', 'U_Offloading']
        output_file = output_file.append(tempDF, ignore_index=True)

        train_count += 1

def main():

    global A_overflow, B_overflow, C_overflow
    global A_total, B_total, C_total
    global L4Trains, L8Trains
    global train_count
    
    overflow = 0
    cur_time = 0

    #################
    ##### start #####
    #################

    # send a train straight to C
    addTrain(cur_time, "L4", ["A", "B"])

    # send a train to A immediately after C leaves
    addTrain(cur_time, "L8", [])

    #####################
    ##### rush hour #####
    #####################

    while(A_remaining > A_total/3 and B_remaining > B_total/3):
        
        # if the current time ends with minute 8
        if(str(cur_time)[-1] == "8"):

            if(cur_time == 58):
                hi = 5

            A_pickup = arrivalsAtTime(cur_time + 3, "A")
            B_pickup = arrivalsAtTime(cur_time + 3 + 11 + 3, "B")
            C_pickup = arrivalsAtTime(cur_time + 3 + 11 + 3 + 12 + 3, "C")
            
            # calculate potential overflow
            overflow = (A_overflow + B_overflow + C_overflow + A_pickup + B_pickup + C_pickup) - 400

            # send a "standard" train
            addTrain(cur_time, "L8", [])

            if(overflow >= 100):
                # print("overflow at " + calculateTime(cur_time) + " is " + str(overflow))

                # if there are still L4 trains left
                if(L4Trains > 0):
                    addTrain(cur_time + 9, "L4", ["A", "B"])

                # else, send an L8 train
                else:
                    addTrain(cur_time + 9, "L8", ["A", "B"])

        # incrementing time
        cur_time += 2

    #####################################
    ##### final third of bell curve #####
    #####################################

    cur_time -= 2

    # gary's algorithm to find groups
    num_small_groups = 0
    num_large_groups = 0
    small_group_size = 0
    large_group_size = 0
    slots_left = ((190 - cur_time)//10) - 1
    trains_left = 16 - train_count
    
    i = slots_left

    # checking first for loop condition  
    while(i * trains_left >= slots_left):
        i -= 1

    small_group_size = i
    large_group_size = i + 1
    match_found = False

    for j in range(slots_left + 1):

        temp_small_size = slots_left - j

        if(match_found):
            break

        if(small_group_size * (temp_small_size) <= slots_left):

            for temp_large_size in range(slots_left + 1):
                right_count = (temp_small_size + temp_large_size == trains_left)
                right_size = ((small_group_size * temp_small_size + large_group_size * temp_large_size) == slots_left)

                if(right_count and right_size):
                    num_small_groups = temp_small_size
                    num_large_groups = temp_large_size

                    match_found = True

    send_time = 0

    for group1 in range(1, num_small_groups + 1):
        send_time = cur_time + ((10 * (small_group_size)) * group1)

        # if there are L8 trains left (to use up all the L8 trains first)
        if(L8Trains > 0):
            addTrain(send_time, "L8", [])

        else:
            addTrain(send_time, "L4", [])

    print(send_time)
        
    for group2 in range(1, num_large_groups + 1):
        send_time = cur_time + ((10 * (large_group_size)) * group2)

        if(L8Trains > 0):
            addTrain(send_time, "L8", [])

        else:
            addTrain(send_time, "L4", [])

    # print(output_file)

if __name__ == "__main__":
    main()