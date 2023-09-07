# PitStop
The goal of the game is to end the game with your cars as far up the 
grid order as possible by choosing the optimal time to pitstop. The goal isn't to
win the race, it's to do the best you can with the cars you've been given

## Drivers
Each driver has 4 traits
- Pace: How far they move down the track each lap
- Inconsistency: The varience of a drivers pace lap to lap
    (*A driver with a pace of 20 and inconsistency of 4 could gain 1-5 seconds on a car with 15 paceand 0 inconsistency*)
- Overtaking and Defending: Used to determine the sucess of an overtake attempt
    by or against them

## Strategy
If a driver would get to a position ahead of the car in front of them, they need to
attempt an overtake. Depending on the Overtaking and Defending skills of the 
drivers involved, this could be a challenge. A failed overtake will force the car behind
slow their pace to match the distance of the driver ahead. So if you have a faster car, 
make sure you don't waste time behind defensive slow ones. Open air is best.

Each car must pit once per race. The car's pace doesn't change, so the decision comes down
to whether you end up behind an opponent after the slow down, or can you hold up an 
opponent who would be faster than you!
