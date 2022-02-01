import pandas as pd

# ------------------------------------- global variables ------------------------------------- #

output_file = pd.read_csv("output_format.csv", index_col=False)
passenger_arrivals = pd.read_csv("testing/rail_data.csv")

# creating lists of passengers' arrival times from the input csv
A_arrivals = passenger_arrivals['A'].tolist()
B_arrivals = passenger_arrivals['B'].tolist()
C_arrivals = passenger_arrivals['C'].tolist()

# a list tracking overflow passengers at station C
C_overflow = [0] * len(C_arrivals)

# indices denoting the last point at which a train picked up passengers
A_last_stop = 0
B_last_stop = 0
C_last_stop = 0

# the total number of passengers to be picked up at each station
A_total = sum(A_arrivals)
B_total = sum(B_arrivals)
C_total = sum(C_arrivals)

# the total number of passengers waiting to be picked up
A_remaining = A_total
B_remaining = B_total
C_remaining = C_total

# the number of given L4 and L8 trains
L4Trains = 4
L8Trains = 12

# the number of trains sent
train_count = 0

# ---------------------------------------- functions ---------------------------------------- #

def calculateTime(current_time):
    """
    (int) -> str
    
    Converts the integer representing the number of minutes since 7:00 AM
    to a string
    """

    time = ""

    hours = 7 + (current_time//60)
    minutes = (current_time % 60)

    string_minutes = ""

    # if the number of minutes is less than 10, adds a 0 before its
    # value in its string representation
    if (minutes < 10):
        string_minutes = "0" + str(minutes)
    else:
        string_minutes = str(minutes)

    time += str(hours) + ":" + string_minutes

    return time

def sum(list, start, stop):
    """
    (list, int, int) -> None
    
    Sums the number of passengers in the input list from index "start"
    (inclusive) to "stop" (exclusive)
    """
    sum = 0

    for i in range(start, stop):
        sum += list[i]

    return sum
 
def calculatePassengers(cur_time, station):
    """
    (int, str) -> int
    
    Calculates the number of passengers collected by a train leaving the
    input "station" at "cur_time"
    """
    global A_last_stop, B_last_stop, C_last_stop
    global C_arrivals

    start = 0   # inclusive
    stop = 0    # exclusive

    # if it is not 7:00 AM but the current time's minutes ends with 0
    if(cur_time != 0 and str(cur_time)[-1] == "0"):
        # the train cannot pick up people arriving at 7:10, for example,
        # if that train leaves the station at that same time
        stop = (cur_time - 1)//10
    else:
        stop = cur_time//10

    # if the "stop" index would cause an index out of bounds error
    if(stop >= len(C_arrivals)):
        stop = len(C_arrivals) - 1
        
    if(station == "A"):
        start = A_last_stop 
        A_last_stop = stop + 1  # incrememnting the index for next train

        return sum(A_arrivals, start, stop + 1)

    elif(station == "B"):
        start = B_last_stop
        B_last_stop = stop + 1  # incrememnting the index for next train

        return sum(B_arrivals, start, stop + 1)

    elif(station == "C"):
        start = C_last_stop
        C_last_stop = stop + 1  # incrememnting the index for next train

        return sum(C_arrivals, start, stop + 1)

def calculateOverflowPassengers(cur_time):
    """
    (int) -> int
    
    Similar to calculate Passengers, but specifically for overflow trains
    (trains sent to clean up overflow); calculates the number of passengers
    collected by a train leaving station C at "cur_time"
    """
    global A_last_stop, B_last_stop, C_last_stop
    global C_overflow

    start = 0   # inclusive
    stop = 0    # exclusive 

    # if it is not 7:00 AM but the current time's minutes ends with 0
    if(cur_time != 0 and str(cur_time)[-1] == "0"):
        # the train cannot pick up people arriving at 7:10, for example,
        # if that train leaves the station at that same time
        stop = (cur_time - 1)//10 + 1
    else:
        stop = cur_time//10 + 1
        
    start = stop - 1
    passengers = sum(C_overflow, start, stop + 1)

    # removes overflow passengers from the list of station C's arrivals
    # since this function is called to pick them up
    C_arrivals[start + 1] -= passengers

    return passengers

def addTrain(cur_time, train_type, skips):
    """
    (int, str, list) -> None

    Adds a train to the output dataframe
    """
    global L4Trains, L8Trains
    global A_remaining, B_remaining, C_remaining
    global C_overflow
    global output_file
    global train_count

    passengers_at_station = 0

    if(train_type == "L4"):
        L4Trains -= 1
        a_avail_cap = 200
    else:
        L8Trains -= 1
        a_avail_cap = 400

    #variables for the column values of the output dataframe
    #### station A
    a_arrival = cur_time
    a_boarding = 0
    ### station B
    b_arrival = 0
    b_avail_cap = a_avail_cap
    b_boarding = 0
    ### station C
    c_arrival = 0
    c_avail_cap = b_avail_cap
    c_boarding = 0
    ### union
    u_arrival = 0
    u_avail_cap = c_avail_cap
    u_offboarding = 0

    # --------------- simulating the train's movements --------------- #

    # ------ at station A ------ #
    if "A" not in skips:
        # the train will stay at the station for 3 minutes
        cur_time += 3
        b_arrival = a_arrival + 8 + 3

        passengers_at_station = calculatePassengers(cur_time, "A")

        # if the available capacity is less than or equal to the number of passengers
        if(a_avail_cap <= passengers_at_station):
            a_boarding = a_avail_cap

            # adds overflow to the subsequent time slot
            A_arrivals[A_last_stop] += passengers_at_station - a_boarding

        # if the available cap is greater than the number of passengers
        else:
            a_boarding = passengers_at_station

        # updating number of people waiting
        A_remaining -= a_boarding

    # if station A is being skipped
    else:
        A_arrivals[A_last_stop] += passengers_at_station - a_boarding
        b_arrival = a_arrival + 8

    b_avail_cap = a_avail_cap - a_boarding
    cur_time += 8   # the time it takes to get to station B

    # ------ at station B ------ #
    if "B" not in skips and b_avail_cap != 0:
        # the train will stay at the station for 3 minutes
        cur_time += 3
        c_arrival = b_arrival + 9 + 3

        passengers_at_station = calculatePassengers(cur_time, "B")

        # if the available capacity is less than or equal to the number of passengers
        if(b_avail_cap <= passengers_at_station):
            b_boarding = b_avail_cap
                
            # adds overflow to the subsequent time slot
            B_arrivals[B_last_stop] += passengers_at_station - b_boarding

        # if the available cap is greater than the number of passengers
        else:
            b_boarding = passengers_at_station

        # updating number of people waiting
        B_remaining -= b_boarding

    # if station B is being skipped
    else:
        c_arrival = b_arrival + 9
        
    c_avail_cap = b_avail_cap - b_boarding
    cur_time += 9   # the time it takes to get to station C 

    # ------ at station C ------ #
    if c_avail_cap != 0:
        # the train will stay at the station for 3 minutes
        cur_time += 3
        u_arrival = c_arrival + 11 + 3

        passengers_at_station = calculatePassengers(cur_time, "C")

        # if the available capacity is less than or equal to the number of passengers
        if(c_avail_cap <= passengers_at_station):
            c_boarding = c_avail_cap
                
            # adds overflow to the subsequent time slot
            C_arrivals[C_last_stop] += passengers_at_station - c_boarding
            C_overflow[C_last_stop - 1] += passengers_at_station - c_boarding

        # if the available cap is greater than the number of passengers
        else:
            c_boarding = passengers_at_station

        C_remaining -= c_boarding

    # if station C is being skipped
    else:
        u_arrival = c_arrival + 11

    u_avail_cap = c_avail_cap - c_boarding
    cur_time += 11  # the time it takes to get to union
    u_offboarding = a_boarding + b_boarding + c_boarding

    # adding the train's data to a dataframe, then appending the row to the output
    tempDF = pd.DataFrame([[train_count + 1, train_type, calculateTime(a_arrival), a_avail_cap, a_boarding, calculateTime(b_arrival), b_avail_cap, b_boarding, calculateTime(c_arrival), c_avail_cap, c_boarding, calculateTime(u_arrival), u_avail_cap, u_offboarding]])
    
    # for testing purposes, uncomment the line below to print each row as it's added
    # print('\n'.join(tempDF.to_string(index = False).split('\n')[1:]))
    
    # appending the train's data to the output dataframe
    tempDF.columns = ['TrainNum', 'TrainType', 'A_ArrivalTime', 'A_AvailCap', 'A_Boarding', 'B_ArrivalTime', 'B_AvailCap', 'B_Boarding', 'C_ArrivalTime', 'C_AvailCap', 'C_Boarding', 'U_Arrival', 'U_AvailCap', 'U_Offloading']
    output_file = output_file.append(tempDF, ignore_index=True)

    train_count += 1

def addOverflowTrain(cur_time, train_type):
    """
    (int, str) -> None

    Similar to addTrain, but specifically for overflow trains
    (trains sent to clean up overflow at station); adds a train
    to the output dataframe
    """
    global L4Trains, L8Trains
    global A_remaining, B_remaining, C_remaining
    global C_overflow
    global output_file
    global train_count

    passengers_at_station = 0

    if(train_type == "L4"):
        L4Trains -= 1
        a_avail_cap = 200
    else:
        L8Trains -= 1
        a_avail_cap = 400

    #variables for the column values of the output dataframe
    #### station A
    a_arrival = cur_time
    a_boarding = 0
    ### station B
    b_arrival = 0
    b_avail_cap = a_avail_cap
    b_boarding = 0
    ### station C
    c_arrival = 0
    c_avail_cap = b_avail_cap
    c_boarding = 0
    ### union
    u_arrival = 0
    u_avail_cap = c_avail_cap
    u_offboarding = 0

    # --------------- simulating the train's movements --------------- #

    # ------ at station A ------ #
    b_arrival = a_arrival + 8
    cur_time += 8

    # ------ at station B ------ #
    c_arrival = b_arrival + 9
    cur_time += 9

    # ------ at station C ------ #
    cur_time += 3
    u_arrival = c_arrival + 11 + 3
    passengers_at_station = calculateOverflowPassengers(cur_time)

    # if the available capacity is less than or equal to the number of passengers
    if(c_avail_cap <= passengers_at_station):
        c_boarding = c_avail_cap
            
        # overflow goes to the next time slot
        C_arrivals[C_last_stop] += passengers_at_station - c_boarding

    # if the available cap is greater than the number of passengers
    else:
        c_boarding = passengers_at_station

        # updating the number of people waiting
        C_remaining -= c_boarding

    u_avail_cap = c_avail_cap - c_boarding
    cur_time += 11
    u_offboarding = a_boarding + b_boarding + c_boarding

    # adding the train's data to a dataframe, then appending the row to the output
    tempDF = pd.DataFrame([[train_count + 1, train_type, calculateTime(a_arrival), a_avail_cap, a_boarding, calculateTime(b_arrival), b_avail_cap, b_boarding, calculateTime(c_arrival), c_avail_cap, c_boarding, calculateTime(u_arrival), u_avail_cap, u_offboarding]])
    
    # for testing purposes, uncomment the line below to print each row as it's added
    # print('\n'.join(tempDF.to_string(index = False).split('\n')[1:]))
    
    # appending the train's data to the output dataframe
    tempDF.columns = ['TrainNum', 'TrainType', 'A_ArrivalTime', 'A_AvailCap', 'A_Boarding', 'B_ArrivalTime', 'B_AvailCap', 'B_Boarding', 'C_ArrivalTime', 'C_AvailCap', 'C_Boarding', 'U_Arrival', 'U_AvailCap', 'U_Offloading']
    output_file = output_file.append(tempDF, ignore_index=True)

    train_count += 1
 
def main():
    global C_overflow
    global A_total, B_total, C_total
    global L4Trains, L8Trains
    global train_count
    global A_last_stop, B_last_stop, C_last_stop
    
    overflow = 0
    cur_time = 0

    # ---------------------- initial train sends ---------------------- #

    # send a train straight to C
    addTrain(cur_time, "L4", ["A", "B"])

    # send a train to A immediately after C leaves
    addTrain(cur_time, "L8", [])

    # --------------------------- rush hour --------------------------- #

    while(A_remaining > A_total/3 and B_remaining > B_total/3):
        
        # if the current time ends with minute 8
        if(str(cur_time)[-1] == "8"):

            A_pickup = calculatePassengers(cur_time + 3, "A")
            B_pickup = calculatePassengers(cur_time + 3 + 11 + 3, "B")
            C_pickup = calculatePassengers(cur_time + 3 + 11 + 3 + 12 + 3, "C")

            # resetting these variables since the function calls above are
            # calculating future overflow rather than actually picking up passengers
            A_last_stop -= 1
            B_last_stop -= 1
            C_last_stop -= 1

            # calculate potential overflow
            overflow = (A_pickup + B_pickup + C_pickup) - 400

            # send a "standard" train
            addTrain(cur_time, "L8", [])

            if(overflow >= 100):
                # print("overflow at " + calculateTime(cur_time) + " is " + str(overflow))

                # if there are still L4 trains left
                if(L4Trains > 0):
                    addOverflowTrain(cur_time + 9, "L4")

                # else, send an L8 train
                else:
                    addOverflowTrain(cur_time + 9, "L8")

        # incrementing time
        cur_time += 2

    # ------------------------ rush hour ends ------------------------ #
    # idea: split up the remaining time slots (10 minute intervals) and 
    # disperse the remaining trains so that 1) L8 trains are sent first 
    # and 2) the first trains cover the minimum about of time slots

    cur_time -= 2

    num_small_groups = 0
    num_large_groups = 0
    small_group_size = 0
    large_group_size = 0
    slots_left = ((190 - cur_time)//10) - 1 
    trains_left = 16 - train_count
    
    i = slots_left

    while(i * trains_left >= slots_left):
        i -= 1

    small_group_size = i
    large_group_size = i + 1
    match_found = False

    for j in range(slots_left + 1):

        if(match_found):
            break

        temp_small_size = slots_left - j

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

        # trying to use up all the L8 trains first
        if(L8Trains > 0):
            addTrain(send_time, "L8", [])

        else:
            addTrain(send_time, "L4", [])

    cur_time = send_time
        
    for group2 in range(1, num_large_groups + 1):
        send_time = cur_time + ((10 * (large_group_size)) * group2)

        if(L8Trains > 0):
            addTrain(send_time, "L8", [])

        else:
            addTrain(send_time, "L4", [])

    # uncomment the line below to view the resulting dataframe (but with index column)
    # print(output_file)

    # uncomment the line below to convert the dataframe to a csv
    output_file.to_csv('train_schedule.csv', index=False)

if __name__ == "__main__":
    main()