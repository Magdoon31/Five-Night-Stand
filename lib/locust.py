import pygame,random

attack = 0
locust_sfx = []
locust_channel = pygame.mixer.Channel(3)
locust_sfx.append(pygame.mixer.Sound("assets/SOUND/locust/breath.mp3")) #0
locust_sfx.append(pygame.mixer.Sound("assets/SOUND/locust/camera_static.mp3")) #1
locust_sfx.append(pygame.mixer.Sound("assets/SOUND/locust/small_footsteps.mp3")) #2
locust_sfx.append(pygame.mixer.Sound("assets/SOUND/locust/deepfootstepsleft.mp3")) #3
locust_sfx.append(pygame.mixer.Sound("assets/SOUND/locust/deepfootstepsright.mp3")) #4
locust_sfx.append(pygame.mixer.Sound("assets/SOUND/locust/doorcreak_left.mp3")) #5
locust_sfx.append(pygame.mixer.Sound("assets/SOUND/locust/doorcreak_right.mp3"))#6
locust_sfx.append(pygame.mixer.Sound("assets/SOUND/locust/fastrunleft.mp3"))#7
locust_sfx.append(pygame.mixer.Sound("assets/SOUND/locust/fastrunright.mp3"))#8
locust_sfx.append(pygame.mixer.Sound("assets/SOUND/locust/small_footsteps2.mp3"))#9
locust_sfx.append(pygame.mixer.Sound("assets/SOUND/locust/small_footsteps3.mp3"))#10

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
            locust_channel.play(locust_sfx[3 if rndsfx == 1 else 7])
            return "DA"
        else:
            locust_channel.play(locust_sfx[4 if rndsfx == 1 else 8])
            return "UH"
    elif room == "DA":
        rnd = random.randint(1,3)
        rndsfx = random.randint(1,2)
        if rnd == 1:
            locust_channel.play(locust_sfx[2 if rndsfx == 1 else 9])
            return "LH"
        elif rnd == 2:
            locust_channel.play(locust_sfx[5])
            return "doorL"
        else:
            if random.random() < 0.2:
                locust_channel.play(locust_sfx[2])
            else:
                locust_channel.play(locust_sfx[4 if rndsfx == 1 else 8])
            return "DB"
    elif room == "LH":
        attack +=1
        return "LH"
    elif room == "UH":
        rndsfx = random.randint(1,2)
        rnd = random.randint(1,3)
        if rnd == 1:
            locust_channel.play(locust_sfx[9 if rndsfx == 1 else 10])
            return "LoH"
        elif rnd == 2:
            locust_channel.play(locust_sfx[6])
            return "doorR"
        else:
            if random.random() < 0.2:
                locust_channel.play(locust_sfx[10])
            else:
                locust_channel.play(locust_sfx[3 if rndsfx == 1 else 7])
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


    