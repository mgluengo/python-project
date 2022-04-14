#ESCAPE: AN ADVENTURE IN THE MIDDLE-EARTH

#Warning: to run this code, you need termcolor package
#To install this package with conda, run: conda install -c omnia termcolor

#SECTION 1: DEFINITIONS

# define items in THE SHIRE

bilbo_house = {
    "name": "House Bilbo",
    "type": "furniture",
}

road_a = {
    "name": "road a",
    "type": "door",
}

map_a = {
    "name": "map a",
    "type": "key",
    "target": road_a,   
}

sam_house = {
    "name": "House Sam",
    "type": "furniture",
}

the_shire = {
    "name": "THE SHIRE",
    "type": "room",
}

# define items in GONDOR

road_b = {
    "name": "road b",
    "type": "door",
}

rivendell = {
    "name": "Rivendell",
    "type": "furniture",
}

map_b = {
    "name": "map b",
    "type": "key",
    "target": road_b,
}


road_c = {
    "name": "road c",
    "type": "door",
}

gondor = {
    "name": "GONDOR",
    "type": "room",
}

# this is not an area - definition of road d before defining map d

road_d = {
    "name": "road d",
    "type": "door",
}

# define items in ROHAN

map_c = {
    "name": "map c",
    "type": "key",
    "target": road_c,
}

map_d = {
    "name": "map d",
    "type": "key",
    "target": road_d,
}

moria = {
    "name": "Moria",
    "type": "furniture",
}

helm = {
    "name": "Helms Deep",
    "type": "furniture",
}

road_b = {
    "name": "road b",
    "type": "door",
}

rohan = {
    "name": "ROHAN",
    "type": "room",
}

# define items in MORDOR

eye_tower = {
    "name": "Eye Tower",
    "type": "furniture",
}

road_c = {
    "name": "road c",
    "type": "door",
}

road_d = {
    "name": "road d",
    "type": "door",
}

mordor = {
    "name": "MORDOR",
    "type": "room",
}


# define outside

outside = {
  "name": "MOUNT DOOM"
}


# define all rooms(areas) and doors(roads)

all_rooms = [the_shire, gondor, rohan, mordor, outside]  # check if it must be changed to all_areas

all_doors = [road_a, road_b, road_c, road_d]



# define which places/areas are related

object_relations = {
    "THE SHIRE": [bilbo_house, sam_house, road_a],
    "GONDOR": [rivendell, road_a, road_b, road_c],
    "ROHAN": [moria, helm, road_b],
    "MORDOR": [eye_tower, road_c, road_d],
    "MOUNT DOOM": [road_d],
    "House Sam": [map_a],
    "Rivendell": [map_b],
    "Moria": [map_c],
    "Helms Deep": [map_d],
    "road a": [the_shire, gondor],
    "road b": [gondor, rohan],
    "road c": [gondor, mordor],
    "road d": [mordor, outside]
}

# SECTION 2 - DEFINE STATE AT GAME START

# define game state. Do not directly change this dict. 
# Instead, when a new game starts, make a copy of this
# dict and use the copy to store gameplay state. This 
# way you can replay the game multiple times.

INIT_GAME_STATE = {
    "current_room": the_shire,
    "keys_collected": [],
    "target_room": outside
}


#SECTION 3 - FUNCTIONS TO PLAY THE GAME

def linebreak():
    """
    Print a line break
    """
    print("\n\n")

def start_game(): 
    """
    Start the game
    """
    from termcolor import colored
    print('***********\n')
    print(colored("\nESCAPE: AN ADVENTURE IN THE MIDDLE-EARTH\n", "blue", attrs=["bold"]))
    print('***********\n')
    print("""
        Hurry up, hobbit!

        The Ring has awoken.
        A threat grows in the land of Mordor where the shadows loom.

        Find all maps to reach Mount Doom and destroy the Ring once and for all.
        The fate of the free world is now in your hands!

        Your journey starts in The Shire.

        You step out of Bilbo's house...

        There's no going back.

    """)
    print('***********\n')
    play_room(game_state["current_room"])   

def play_room(room):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either 
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        from termcolor import colored
        print('***********\n')
        print(colored("\nYou destroyed the Ring and saved the free world!\n", "blue", attrs=["bold"]))
        print("""
            Farewell for now, hobbit...
            but remember: for every adventure that ends
            a new one begins.
            """)
        print('***********\n')
    else:
        print("\nYOU ARE IN " + room["name"])
        items = [i["name"] for i in object_relations[room["name"]]]
        print("You see from here: " + "  //  ".join(items))
        examine_item(input("\nWhere do we go next? ").strip())

def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if(not current_room == room):
            return room

def examine_item(item_name):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been 
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """

    current_room = game_state["current_room"]
    next_room = ""
    output = None

    from termcolor import colored
    
    for item in object_relations[current_room["name"]]:
        if(item["name"] == item_name):
            output = "\nYou examine " + item_name + ": "
            if(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                if(have_key):
                    output += colored("\nLook! You can enter the area with a map you have.", "cyan")
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += colored("\nYou shall not pass! First find the map to enter this area.", "red")
            else:
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += colored("\nMy Precious! You find " + item_found["name"] + ".", "green")
                else:
                    output += colored("\nThere isn't anything interesting in this place.", "red")
            print(output)
            break

    if(output is None):
        print("\n\nFeeling lost? The place you requested is not in the current area.")
    
    if(next_room and input("\nShall we explore the next area?\nEnter 'yes' or 'no': ").strip() == 'yes'):
        print(colored("\nThe journey continues!", "green"))
        play_room(next_room)
    else:
        play_room(current_room)


#SECTION 4 - INITIATE GAME

game_state = INIT_GAME_STATE.copy()
start_game()