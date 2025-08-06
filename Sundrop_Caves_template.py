from random import randint

player = {}
game_map = []
fog = []
day=0

MAP_WIDTH = 0
MAP_HEIGHT = 0

TURNS_PER_DAY = 20
WIN_GP = 500

minerals = ['copper', 'silver', 'gold']
mineral_names = {'C': 'copper', 'S': 'silver', 'G': 'gold'}
pickaxe_price = [50, 150]

prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT
def load_map(filename, map_struct):
    map_file = open(filename, 'r')
    global MAP_WIDTH
    global MAP_HEIGHT
    
    map_struct.clear()
    
    # TODO: Add your map loading code here
    with open(filename,'r')as map_file:
        for line in map_file:
            line=line.strip()
            if line:
                map_struct.append(list(line))
    MAP_WIDTH = len(map_struct[0])
    MAP_HEIGHT = len(map_struct)

    map_file.close()

# This function clears the fog of war at the 3x3 square around the player
def clear_fog(fog, player):
    x,y=player['x'],player['y']
    for i in range(max(0,y-1),min(MAP_HEIGHT,y+2)):
        for j in range(max(0,x-1),min(MAP_WIDTH,x+2)):
            fog[i][j]=False
    return

def initialize_game(game_map, fog, player,name):
    # initialize map
    load_map("lvl 1.txt", game_map)

    # TODO: initialize fog
    for _ in range(MAP_HEIGHT):
        fog.append([True]*MAP_WIDTH)
    # TODO: initialize player
    #   You will probably add other entries into the player dictionary
    player.clear()
    player['name']=name
    player['x'] = 0
    player['y'] = 0
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['GP'] = 67
    player['day'] = 1
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY
    player['pickaxe'] = 1
    player['capacity']=10

    clear_fog(fog, player)
    
# This function draws the entire map, covered by the fof
def draw_map(game_map, fog, player):
    for y in range(MAP_HEIGHT):
        row=""
        for x in range(MAP_WIDTH):
            if x==player['x'] and y == player['y']:
                row += "M"
            elif fog[y][x]:
                row+="#"
            else:
                row+=game_map[y][x]
        print(row)     
    return

# This function draws the 3x3 viewport
def draw_view(game_map, fog, player):
    px=player['x']
    py=player['y']
    
    print("+---+")
    for y in range(py - 1, py + 2):
        line = "|"
        for x in range(px - 1, px + 2):
            if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
                if x == px and y == py:
                    line += "M"
                elif not fog[y][x]:
                    line += game_map[y][x]
                else:
                    line += "?"
            else:
                line += " "
        line += "|"
        print(line)
    print("+---+")
    return

# This function shows the information for the player
def show_information(player):
    print("-----Player Information-----")
    ore_type={1:"copper",2:"silver",3:"gold"}
    current_ore=ore_type.get(player['pickaxe'],'unknow')
    print("Name: {:}".format(player['name']))
    print("Pickaxe level: {:} ({:}) ".format(player['pickaxe'],current_ore))
    print("----------------------------")
    total_load=player['copper']+player['silver']+player['gold']
    print("Load: {:}/{:} ".format(total_load,player['capacity']))
    print("----------------------------")
    print("GP: {:}".format(player['GP']))
    print("Steps taken: {:}".format(player['steps']))
    print("----------------------------")
    return

# This function saves the game
def save_game(game_map, fog, player):
    with open("savefile.txt",'w') as f:
    # save map  
        for row in game_map:
            print("".join(row),file=f)
        print("",file=f) #blank line
    # save fog
        for row in fog:
            line=""
            for cell in row:
                line+="1" if cell else"0"
            print(line,file=f)
    # save player
    load_amt=player.get('copper',0)+player.get('silver',0)+player.get('gold',0)
    print(player['name'],player['x'],player['y'],player['GP'],
          player['steps'],load_amt,player['capacity'],sep=",",file=f)
    return
        
# This function loads the game
def load_game(game_map, fog, player):
    # load map
    # load fog
    # load player
    return

def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
#    print("(H)igh scores")
    print("(Q)uit")
    print("------------------")

def show_town_menu():
    print()
    # TODO: Show Day
    print("DAY {:}".format(player['day']))
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")
            

#--------------------------- MAIN GAME ---------------------------
game_state = 'main'
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 1000 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")

# TODO: The game!
def sell_ore(player):
    total_earned=0

    for mineral in ['copper','silver','gold']:
        amount=player.get(mineral,0)
        if amount>0:
            low,high=prices[mineral]
            price_per_unit=randint(low,high)
            earned=amount*price_per_unit
            total_earned+=earned
            player[mineral]=0
    player['GP']+=total_earned
    print("GP: {:}".format(player['GP']))
while True:
    show_main_menu()
    day+=1
    choice1=input("Youe choice? ").strip().lower()
    if choice1=="n":
        name=input("Greetings,miner!What is your Name?")
        print("Pleased to meet you,{:}. Welcome to Sundrop Town!".format(name))
        initialize_game(game_map,fog,player,name)
        while True:
            show_town_menu()
            choice2=input("Your choice? ").strip().lower()
            if choice2=="b":
                while True:
                    print("------------------------Shop Menu------------------------")
                    pickaxe_lvl=player['pickaxe']
                    if pickaxe_lvl==1:
                        print("(P)ickaxe upgrade to Level 2 to mine silver ore for 50GP")
                    elif pickaxe_lvl==2:
                        print("(P)ickaxe upgrade to Level 3 to mine gold ore for 150GP")
                    elif pickaxe_lvl>=3:
                        print("(P)ickaxe is at max level.")
                    
                    cap=player.get("capacity",10)
                    upgrade_cost=cap*2
                    print("(B)ackpack upgrade to carry {:} items for {:} GP".format(cap+2,upgrade_cost))
                    print("(L)eave shop")
                    print("---------------------------------------------------------")
                    sell_ore(player)
                    choice3=input("Your choice? ").strip().lower()
                    if choice3=='p':
                        if pickaxe_lvl==1 and player['GP']>=50:
                            player['GP']-=50
                            player['pickaxe']=2
                            print("Congratulations!You can now mine silver!")
                        elif player.get('pickaxe',1)==2 and player['GP']>=150:
                            player['GP']-=150
                            player['pickaxe']=3
                            print("Congratulations!You can now mine gold!")
                        else:
                            print("Not enough GP")
                    elif choice3=="b":
                        if player['GP']>=upgrade_cost:
                            player['GP']-=upgrade_cost
                            player['capacity']=cap+2
                            print("Congratulations! You can now carry {:} items!".format(cap+2))
                        else:
                            print("Not enough GP.")
                    elif choice3=="l":
                        break
                    else:
                        print("Invalid choice")
            elif choice2=='i':
                show_information(player)
            elif choice2=='v':
                save_game(game_map, fog, player)
                print("Game saved.")
            elif choice2=='q':
                break
    elif choice1=="l":
        load_game(game_map,fog,player)
        print("Game loaded successfully!")
        while True:
            show_town_menu()
            choice2 = input("Your choice? ").strip().lower()
            if choice2=="b":
                while True:
                    print("------------------------Shop Menu------------------------")
                    pickaxe_lvl=player['pickaxe']
                    if pickaxe_lvl==1:
                        print("(P)ickaxe upgrade to Level 2 to mine silver ore for 50GP")
                    elif pickaxe_lvl==2:
                        print("(P)ickaxe upgrade to Level 3 to mine gold ore for 150GP")
                    elif pickaxe_lvl>=3:
                        print("(P)ickaxe is at max level.")
                    
                    cap=player.get("capacity",10)
                    upgrade_cost=cap*2
                    print("(B)ackpack upgrade to carry {:} items for {:} GP".format(cap+2,upgrade_cost))
                    print("(L)eave shop")
                    print("---------------------------------------------------------")
                    sell_ore(player)
                    choice3=input("Your choice? ").strip().lower()
                    if choice3=='p':
                        if pickaxe_lvl==1 and player['GP']>=50:
                            player['GP']-=50
                            player['pickaxe']=2
                            print("Congratulations!You can now mine silver!")
                        elif player.get('pickaxe',1)==2 and player['GP']>=150:
                            player['GP']-=150
                            player['pickaxe']=3
                            print("Congratulations!You can now mine gold!")
                        else:
                            print("Not enough GP")
                    elif choice3=="b":
                        if player['GP']>=upgrade_cost:
                            player['GP']-=upgrade_cost
                            player['capacity']=cap+2
                            print("Congratulations! You can now carry {:} items!".format(cap+2))
                        else:
                            print("Not enough GP.")
                    elif choice3=="l":
                        break
                    else:
                        print("Invalid choice")
            elif choice2=='i':
                show_information(player)
            elif choice2=='v':
                save_game(game_map, fog, player)
                print("Game saved.")
            elif choice2=='q':
                break
    elif choice1=="q":
        break
    else:
        print("Invalid input. Please enter N, L ,Q only")
