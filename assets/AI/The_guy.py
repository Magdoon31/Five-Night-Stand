import sys, random
sys.path.insert(0, 'assets')
import lib.sfx_manager as sfx

# rooms: E - exit, DA - Dinning A, DB - Dinning B, LH - left hall, UH - upper hall,
# LoH - lower hall, A - Room A, B - Room B, C - Room C, BR - back room, BH - back hall, You - you
ALUsed = 0
AudioLureConnections = {"E" : ["BH","DB","UH"], "DB": ["E","UH","DA"], "DA":["DB","LH","A"], "LH": ["DA","A","C"], "C": ["LH"], "BR":["UH", "LoH", "BH"], "BH": ["E","BR"], "A": ["DA","LH"]
}

def move(room, AI,LockedDoor,nightmare = False, AudioLure = False):
    rnd = random.randint(1, 100)
    if AI > 80 and not nightmare and not AudioLure:
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
            if LockedDoor == "DA" and choice == "LH":
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
                if nightmare:
                    rnd = random.randint(1, 3)
                    if rnd == 1:
                        return "B"
                    else:
                        return "DB"
                if choice == "LoH" and not nightmare:
                    sfx.play("metal_door_bang")
                    return room
                else:
                    return choice
            else:
                return choice if not nightmare else "LoH"
        elif room == "LoH":
            return random.choice(["You", "UH" if not nightmare else "You", "BR"])
        elif room == "A":
            return "LH"
        elif room == "C":
            sfx.play("steps_left")
            return "LH"
        elif room == "B":
            return "UH"
        elif room == "BR":
            choice = random.choice(["LoH", "BH"])
            if choice == "LoH":
                sfx.play("steps_right")
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
    

def AudioLure(room, AI, AudioLureRoom, LockedDoor, Nightmare):
    global ALUsed
    rnd = random.randint(1, 100)

    if room not in AudioLureConnections[AudioLureRoom] or AudioLureRoom == room:
        ALUsed += 1
        return room
    elif rnd <= int(100 - (AI/5 * ALUsed)):
        ALUsed += 1
        if (((room == "DA" and AudioLureRoom == "LH") or (room == "LH" and AudioLureRoom == "DA")) and LockedDoor == "DA") or (((room == "BH" and AudioLureRoom == "E") or (room == "E" and AudioLureRoom == "BH")) and LockedDoor == "E"):
            sfx.play("metal_door_bang")
            return room
        return AudioLureRoom
    else:
        ALUsed += 1
        while True:
            roomToMove = move(room, 100, LockedDoor,Nightmare, AudioLure = True)
            if room == "BH" and AudioLureRoom == "BR" and LockedDoor == "E":
                sfx.play("metal_door_bang")
                return room
            elif room == "C" and AudioLureRoom == "LH":
                    return room
            elif Nightmare and room == "BH" and AudioLureRoom == "BR":
                            return room
            elif Nightmare and room == "DA" and LockedDoor == "DA":
                sfx.play("metal_door_bang")
                return room
            elif Nightmare and room == "E" and LockedDoor == "E":
                sfx.play("metal_door_bang")
                return room
            elif Nightmare and room == "UH" and LockedDoor == "UH":
                sfx.play("metal_door_bang")
                return room        
            if roomToMove == AudioLureRoom or (room == "LH" and roomToMove == "DA" and LockedDoor == "DA") or (room == "LoH" and roomToMove == "UH" and LockedDoor == "UH"):
                continue
            else:
                return roomToMove
def reset_audio_lures():
    global ALUsed
    ALUsed = 0
    