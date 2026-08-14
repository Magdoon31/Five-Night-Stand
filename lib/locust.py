import pygame,random
from lib import sfx_manager as sfx
attack = 0


def move(room,CamON):
    global attack
    if room in ("DA","DB","UH"):
        attack = 0
    if random.random() < 0.1 and room not in ("breath","camera_static","doorL","doorR","LH","LoH"):
        return "breath" if CamON else "camera_static"
    if room == "You":
        return "DB"
    elif room == "DB":
        attack = 0
        rndsfx = random.randint(1,2)
        if random.random()>0.5:
            if random.random() < 0.2:
                sfx.play("small_footsteps")
            else:
                sfx.play("deep_footsteps_left" if rndsfx == 1 else "fast_run_left")
            return "DA"
        else:
            if random.random() < 0.2:
                sfx.play("small_footsteps2")
            else:
                sfx.play("deep_footsteps_right" if rndsfx == 1 else "fast_run_right")
            return "UH"
    elif room == "DA":
        rnd = random.randint(1,3)
        rndsfx = random.randint(1,2)
        if rnd == 1:
            sfx.play("small_footsteps" if rndsfx == 1 else "small_footsteps2")
            return "LH"
        elif rnd == 2:
            sfx.play("door_creak_left")
            return "doorL"
        else: 
            sfx.play("deep_footsteps_right" if rndsfx == 1 else "fast_run_right")
            return "DB"
    elif room == "LH":
        attack +=1
        return "LH"
    elif room == "UH":
        rndsfx = random.randint(1,2)
        rnd = random.randint(1,3)
        if rnd == 1:
            sfx.play("small_footsteps2" if rndsfx == 1 else "small_footsteps3")
            return "LoH"
        elif rnd == 2:
            sfx.play("door_creak_right")
            return "doorR"
        else:
            sfx.play("deep_footsteps_left" if rndsfx == 1 else "fast_run_left")
            return "DB"
    elif room == "LoH":
        attack +=1
        return "LoH"
    elif room == "doorL":
        attack +=1
        return "doorL"
    elif room == "doorR":
        attack +=1
        return "doorR"
    elif room == "breath":
        attack +=1
        return "breath"
    elif room == "camera_static":
        attack +=1
        return "camera_static"


    