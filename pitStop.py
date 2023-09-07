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
    target = car_list[index]
    for i in range(index, 9):
        opp = car_list[index + 1]
        if(target.position <= opp.position):
            swap(car_list, index, index + i)
            print(f"pit swapping {target} and {opp}")
            index += 1


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
            car = car_list[i]
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
        seed = random.randint(0,1000000)
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
    player_car1 = Car(p1Name, random.randint(15, 20), random.randint(1, 4), random.randint(1, 10), random.randint(1, 10), None)
    player_car2 = Car(p2Name, random.randint(15, 20), random.randint(1, 4), random.randint(1, 10), random.randint(1, 10), None)

    computer_cars = [
        Car(NAMES[i], random.randint(15, 20), random.randint(1, 4), random.randint(1, 10), random.randint(1, 10), random.randint(1, LAPCOUNT))
        for i in range(0, 8)
    ]

    all_cars = [player_car1, player_car2] + computer_cars
    all_cars.sort(key=lambda x: x.pace + random.randint(-x.inconsistency, x.inconsistency), reverse=True)

    print_driver_info(all_cars)

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
                player1_pit_decision = input(f"Would {player_car1.name} like to take a pit stop this lap? (y/n): ")
                if player1_pit_decision.lower() == 'y':
                    player_car1.pitPlan = LAP
                    print(f"{player_car1.name} pits.")

        if(not player_car2.pitstop_done):
            if(LAP == LAPCOUNT):
                player_car2.pitPlan = LAP
                print(f"{player_car2.name} pits.")
            else:
                player2_pit_decision = input(f"Would {player_car2.name} like to take a pit stop this lap? (y/n): ")
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
            pitstop_status = '✅' if car.pitstop_done else '❌'
            posChange = ""
            if(car.prevPos > i):
                for j in range(car.prevPos - i):
                    posChange = posChange + "⬆"
            elif(car.prevPos < i):
                for j in range(i - car.prevPos):
                    posChange = posChange + "⬇"
            print(f"{i + 1}. {posChange} {car.name} +{abs(car.position - all_cars[0].position)}s - Pitstop: {pitstop_status}")
        print("\n")
    player1_end = all_cars.index(player_car1) + 1
    player2_end = all_cars.index(player_car2) + 1
    print("**   FINAL RESULTS   **")
    for i, car in enumerate(all_cars):
            posChange = ""
            if(car.originalPos > i):
                posChange = posChange + "⬆"
            elif(car.originalPos < i):
                posChange = posChange + "⬇"
            print(f"{i + 1}. {posChange}({car.originalPos + 1}->{i + 1}){car.name} +{abs(car.position - all_cars[0].position)}s")

if __name__ == '__main__':
    main()
