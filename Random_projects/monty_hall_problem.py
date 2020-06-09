import random

def setGame():
    prise = random.randint(1,3)
    choise = random.randint(1,3)
    return (prise, choise)

def gameNoChange(game_tuple):
    prise = game_tuple[0]
    choise = game_tuple[1]
    if prise == choise:
        return True
    else:
        return False

def gameChange(game_tuple):
    prise = game_tuple[0]
    old_choise = game_tuple[1]
    while True:
        open_door = random.randint(1,3)
        if open_door != old_choise and open_door != prise:
            break
    new_choise  = tuple(set([1,2,3]) - set([old_choise, open_door]))
#    print(new_choise[0], old_choise, open_door)
    if prise == new_choise[0]:
        return True
    else:
        return False

wins_no_change = 0
loose_no_change = 0

wins_with_change = 0
loose_with_change = 0

num_tests = 1000_000_000
for _ in range(num_tests):
    # no change     
    game_example_no_change = gameNoChange(setGame())
    if game_example_no_change:
        wins_no_change += 1
    else:
        loose_no_change += 1
    
    # with change
    game_example_with_change = gameChange(setGame())
    if game_example_with_change:
        wins_with_change += 1
    else:
        loose_with_change += 1

fraction_no_change = wins_no_change/(loose_no_change+wins_no_change)
fraction_with_change = wins_with_change/(loose_with_change+wins_with_change)
print('wins(no change): ', wins_no_change, "\nloose(no change): ", loose_no_change, "\nPropability: ", fraction_no_change)
print("\n--------\n")
print('wins(change): ', wins_with_change, "\nloose(change): ", loose_with_change, "\nPropability: ", fraction_with_change)