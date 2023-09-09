import random

LAP = 0


NAMES = ["Verstappen", "Hamilton", "Leclerc", "Alonso", "Norris", "Perez", "Sainz", "Russell"]

class Car:
    def __init__(self, name, pace, inconsistency, overtaking, defending, pitPlan):
        self.name = name
        self.pace = pace
        self.inconsistency = inconsistency
        self.overtaking = overtaking
        self.defending = defending
        self.position = 0
        self.pitstop_done = False
        self.pitPlan = pitPlan
        self.checked = False
        self.prevPos = 0
        self.originalPos = 0

def swap(array, indA, indB):
    hold = array[indA]
    array[indA] = array[indB]
    array[indB] = hold


def print_driver_info(car_list):
    print("\nDriver Information:")
    for i, car in enumerate(car_list):
        print(f"{car.name}")
        print(f"  - Pace: {car.pace}")
        print(f"  - Inconsistency: {car.inconsistency}")
        print(f"  - Overtaking: {car.overtaking}")
        print(f"  - Defending: {car.defending}\n")
        #print(f"  - Pit Plan: {car.pitPlan if car.pitPlan is not None else 'N/A'}\n")



def attempt_overtake(attacker, defender):
    #print(f"{attacker.name} is attempting to overtake {defender.name}")
    attack_value = random.randint(0, attacker.overtaking)
    defend_value = random.randint(0, defender.defending)
    # if attack_value > defend_value:
    #     print('overtake successful')
    # else:
    #     print('overtake failed')
    return attack_value > defend_value

def return_from_pit(car_list, index):
    if index < 0 or index >= len(car_list):  # Check for out-of-bounds index
        #print(f"Index {index} out of bounds.")
        return

    target = car_list[index]

    # Using min to ensure the loop doesn't go out of bounds
    for i in range(index + 1, min(len(car_list), 9)):
        opp = car_list[i]
        if target.position <= opp.position and i < 10:
            try:
                swap(car_list, index, i)  # Changed from index + i to i
            except Exception as e:  # It's good to know what kind of exception occurred
                print(f"issue with pit rejoin between {target.name} and {opp.name}: {e}")
            index += 1  # Update the index



def expectedPosition(car_list):
    scores = []
    # Populate the scores list
    for car in car_list:
        scores.append({
            "name": car.name, 
            "score": (car.pace * 2 - car.inconsistency + car.overtaking + car.defending)
        })

    # Sort the list of dictionaries by the 'score' key in descending order
    sorted_scores = sorted(scores, key=lambda x: x['score'], reverse=True)

    # Print the sorted list
    print("Expected Final Positions \n Try to match or do better than this\n")
    for i, car_score in enumerate(sorted_scores, 1):
        print(f"{i}. {car_score['name']}")
    print("\n")




def lap(car_list, pitstop_time):
    for car in car_list:
        car.checked = False
    global LAP  # Specify that you're using the global LAP variable
    
    for i in range(len(car_list)):

        # for j, car in enumerate(car_list):
        #     pitstop_status = '✅' if car.pitstop_done else '❌'
        #     print(f"{j + 1}. {car.name} - Position: {car.position} - Pitstop: {pitstop_status}")
        
        car = car_list[i]
        while(car.checked):
            i += 1
            if(i < len(car_list)):
                car = car_list[i]
            else:
                break
        #print(f"Looking at {car.name}\n")
        car.position += car.pace - random.randint(0, car.inconsistency)
        if (car.pitPlan == LAP): # If taking a pitstopn
            
            car.position -= pitstop_time
            return_from_pit(car_list, i)
            car.pitstop_done = True
            car.checked = True
        else:
            
            while True:
                if(i > 0):
                    overtakeTarget = car_list[i - 1]
                    if(car.position > overtakeTarget.position): 
                        if(overtakeTarget.pitPlan != LAP):
                            #You are overtaking the car ahead and they are not pitting
                            if(attempt_overtake(car, overtakeTarget)):
                                # Overtake success
                                swap(car_list, i, i - 1)
                                i -= 1
                            else:
                                car.position = overtakeTarget.position
                                car.checked = True
                                break
                        else: 
                            swap(car_list, i, i - 1)
                            i -= 1
                    else: 

                        car.checked = True
                        break
                        
                else: 
                    car.checked = True
                    break
                    


def main():

    seed = input("Do you want to use a seed? (either n or enter seed): ")
    if seed == "n":
        seed = random.randint(0,10000)
        print(f"seed randomly set to {seed}")
    random.seed(seed)

    p1Name = input("Name of your first driver: ")
    p2Name = input("Name of your second driver: ")
    if p1Name == "":
        p1Name = "Driver 1"
    if p2Name == "":
        p2Name = "Driver 2"

    global LAP
    global NAMES
    LAPCOUNT = random.randint(10, 15)
    LAP = 1
    player_car1 = Car(p1Name, random.randint(1, 7), random.randint(1, 5), random.randint(1, 5), random.randint(1, 5), None)
    player_car2 = Car(p2Name, random.randint(1, 7), random.randint(1, 5), random.randint(1, 5), random.randint(1, 5), None)

    computer_cars = [
        Car(NAMES[i], random.randint(1, 7), random.randint(1, 5), random.randint(1, 5), random.randint(1, 5), random.randint(1, LAPCOUNT))
        for i in range(0, 8)
    ]

    all_cars = [player_car1, player_car2] + computer_cars
    all_cars.sort(key=lambda x: x.pace - random.randint(0, x.inconsistency), reverse=True)

    print_driver_info(all_cars)
    expectedPosition(all_cars)

    player1_start = all_cars.index(player_car1) + 1
    player2_start = all_cars.index(player_car2) + 1

    pitstop_time = random.randint(5, 10)

    print(f"The race is {LAPCOUNT} laps long")
    print(f"Pitstop time penalty is {pitstop_time}s")

    print("Initial car order:")
    for i, car in enumerate(all_cars):
        print(f"{i + 1}. {car.name}")
        car.originalPos = i
    print("")

    for current_lap in range(1, LAPCOUNT + 1):
        print(f"Lap {current_lap}")
        if(not player_car1.pitstop_done):
            #print(f"{LAP} {LAPCOUNT}")
            if(LAP == LAPCOUNT):
                player_car1.pitPlan = LAP
                print(f"{player_car1.name} pits.")
            else :
                player1_pit_decision = input(f"Would {player_car1.name} like to take a pit stop this lap? -{pitstop_time}s (y/n): ")
                if player1_pit_decision.lower() == 'y':
                    player_car1.pitPlan = LAP
                    print(f"{player_car1.name} pits.")

        if(not player_car2.pitstop_done):
            if(LAP == LAPCOUNT):
                player_car2.pitPlan = LAP
                print(f"{player_car2.name} pits.")
            else:
                player2_pit_decision = input(f"Would {player_car2.name} like to take a pit stop this lap? -{pitstop_time}s (y/n): ")
                if player2_pit_decision.lower() == 'y':
                    player_car2.pitPlan = LAP
                    print(f"{player_car2.name} pits.")

        if(player_car1.pitstop_done and player_car2.pitstop_done):
            input("do next lap")

        for i, car in enumerate(all_cars):
            car.prevPos = i
        lap(all_cars, pitstop_time)
        LAP += 1

        #all_cars.sort(key=lambda x: x.position, reverse=True)

        for i, car in enumerate(all_cars):
            pitstop_status = '(y)' if car.pitstop_done else '(n)'
            posChange = ""
            if(car.prevPos > i):
                for j in range(car.prevPos - i):
                    posChange = posChange + "+"
            elif(car.prevPos < i):
                for j in range(i - car.prevPos):
                    posChange = posChange + "-"
            print(f"{i + 1}. {posChange} {car.name} +{abs(car.position - all_cars[0].position)}s - Pitstop: {pitstop_status}     ({car.pace}, {car.inconsistency}, {car.overtaking}, {car.defending})")
        print("\n")
    
    print("**   FINAL RESULTS   **")
    for i, car in enumerate(all_cars):
            posChange = ""
            if(car.originalPos > i):
                posChange = posChange + "+"
            elif(car.originalPos < i):
                posChange = posChange + "-"
            print(f"{i + 1}. {posChange}({car.originalPos + 1}->{i + 1}) {car.name} +{abs(car.position - all_cars[0].position)}s")

if __name__ == '__main__':
    while True:
        main()
        play = input("Run again (y) or close (n)")
        if(play == 'n'):
            break
