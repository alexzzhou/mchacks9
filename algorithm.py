from trains.py import GlobalVar

def scheduling_algo():
    L4Trains = 4
    L8Trains = 12
    
    CURRENT_T = 0
    glovar = GlobalVar()
    passenger_schedule = pd.read_csv(sys.argv[2]).to_numpy().tolist()

    A_remaining = glovar.PEOPLEA
    B_remaining = glovar.PEOPLEB
    C_remaining = glovar.PEOPLEC

    scheduling_trains = []
    overflow = 0

    ##### start
    send_train(scheduling_trains, "L4", [A,B])
    send_train(scheduling_trains, "L4", [])

    ##### rush hour
    while(A_remaining > glovar.PEOPLEA/3 and B_remaining > glovar.PEOPLEB/3 and C_remaining > glovar.PEOPLEC/3):
        
        # if the current time ends with minute 8
        if(str(CURRENT_T)[-1] == "8"):
            
            # calculate potential overflow
            overflow = 400 - passenger_schedule[0][CURRENT_T] + overflow

            if(overflow >= 100):
                if(L4Trains > 0):
                    send_train(scheduling_trains, "L4", )
