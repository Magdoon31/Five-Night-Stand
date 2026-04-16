import sys, random
sys.path.insert(0, 'assets')
import SOUND.SFXManager as sfx

# rooms: E - exit, DA - Dinning A, DB - Dinning B, LH - left hall, UH - upper hall,
# LoH - lower hall, A - Room A, B - Room B, C - Room C, BR - back room, BH - back hall You - you
ALUsed = 0
AudioLureConnections = {"E" : ["BH","DB","UH"], "DB": ["E","UH","DA"], "DA":["DB","LH","A"], "LH": ["DA","A","C"], "C": ["LH"], "BR":["UH", "LoH", "BH"], "BH": ["E","BR"], "A": ["DA","LH"]
}

def move(room, AI,LockedDoor,nightmare = False):
    rnd = random.randint(1, 100)
    if AI > 80 and not nightmare:
        AI = 80
    if rnd <= AI:
        if room == "E":
            choice = random.choice(["DB", "BH"])
            if LockedDoor == "E" and choice == "BH":
                return room if not nightmare else "DB"
            else:
                return choice
        elif room == "DA":
            choice = random.choice(["DB", "LH"])
            if LockedDoor == "DA":
                if choice == "LH" :
                    return "DB" if nightmare else room
            else:
                return choice
        elif room == "DB":
            return random.choice(["DA", "UH", "E"])
        elif room == "LH":
            return random.choice(["You", "C", "A" if not nightmare else "You"])
        elif room == "UH":
            choice = random.choice(["LoH", "DB", "B"])
            if LockedDoor == "UH":
                if choice == "LoH" and not nightmare:
                    sfx.MetalDoor("bang")
                    return room
                if nightmare:
                    return "DB"
            else:
                return choice if not nightmare else "LoH"
        elif room == "LoH":
            return random.choice(["You", "UH" if not nightmare else "You", "BR"])
        elif room == "A":
            return "LH"
        elif room == "C":
            sfx.Steps("left")
            return "LH"
        elif room == "B":
            return "UH"
        elif room == "BR":
            choice = random.choice(["LoH", "BH"])
            if choice == "LoH":
                sfx.Steps("right")
            return choice
        elif room == "BH":
            if not nightmare:
                return random.choice(["E", "BR"])
            else:
                return "BR"
        else:
            return room
    else:
        return room
    if room == None:
        return "DB"

def AudioLure(room, AI, AudioLureRoom, LockedDoor):
    global ALUsed
    rnd = random.randint(1, 100)
    if AudioLureConnections[AudioLureRoom].count(room) != 1:
        ALUsed += 1
        return room
    if AudioLureRoom == room:
        roomToMove = move(room, AI, LockedDoor)
        ALUsed += 1
        return roomToMove
    if rnd <= int(100 - (AI/5 * ALUsed)):
        ALUsed += 1
        return AudioLureRoom
    else:
        while True:
            roomToMove = move(room, AI, LockedDoor)
            if roomToMove == AudioLureRoom:
                continue
            else:
                ALUsed += 1
                return roomToMove

    