import pygame, random
import assets.AI.The_guy as The_guy
import assets.SOUND.SFXManager as sfx

pygame.init()
pygame.mixer.init()
pygame.font.init()

clock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)



# Enemies difficulty [AI]

enemies = {"The_guy": {"room": "E", "AI": 40}, "Face" : {"room": "You", "AI":40, "alpha" : 0}}



animating = False
anim_frame = 0
anim_timer = 0
anim_delay = 30
hour = 0
display_time = "10:00 PM"
last_hour_time = pygame.time.get_ticks()
last7 = pygame.mixer.Sound("assets/SOUND/last 7 sec.mp3")
last7one = 0

Win_img = pygame.image.load("assets/IMAGE/6AM.png").convert()
Win_img = pygame.transform.scale(Win_img, (1920,1080)).convert()
Win_sfx = pygame.mixer.Sound("assets/SOUND/6AM.mp3")

EnemyMoveTimer = 0
AttackTimer = 0
Jumpscare = False
jumpscareSFX = pygame.mixer.Sound("assets/SOUND/Jumpscare.mp3")




face_room_img = pygame.image.load("assets/IMAGE/Face_room.png").convert_alpha()
face_jumpscare = pygame.image.load("assets/IMAGE/Face.png").convert_alpha()
face_jumpscare = pygame.transform.scale(face_jumpscare,(1320,1080))
running = True
win = False


flashlight_img = pygame.image.load("assets/IMAGE/flashlight.png").convert_alpha()
flashlight_img = pygame.transform.scale(flashlight_img, (1000,1000))
flashlight_toogle = False


SelectedCam = ""
room_positions = {
    "A": (955, 538),
    "BH": (1420, 668),
    "BR": (1328, 742),
    "E": (1325, 460),
    "C": (755, 880),
    "DA": (957, 458),
    "DB": (1017, 460),
    "LH": (757, 680)
}
door_positions = {
    "DA" : (706,485),
    "E" : (1377,486),
    "UH" : (1215,696)
}
ScanTimer = 0
ScanDuration = 0
ScanDurationMax = 200
AudioLureTimer = 0
DoorTimer = 0
AudioLure_img = pygame.image.load("assets/IMAGE/plan of the hotel/AudioLure.png").convert_alpha()
AudioLure_img = pygame.transform.scale(AudioLure_img,(88,54))
AudioLure_sfx = pygame.mixer.Sound("assets/SOUND/AudioLure.mp3")
LockedDoor = None
audio_lure_button_rect = pygame.Rect(364, 323, 180, 88)

cameraMove = 15
CamON = False
CamX = -250
CamBackground = []
for i in range(1, 47):  # np. 6 sekund * 30 fps
    img = pygame.image.load(f"assets/VIDEO/camera_BACK_frames/frame_{i:04d}.png").convert()
    CamBackground.append(img)
CamBackground_frame = 0
cam_room_cache = {}
for room in ["You", "DA", "DB", "LH", "UH", "LoH", "A", "B", "C", "BR", "BH", "E"]:
    img = pygame.image.load(f"assets/IMAGE/plan of the hotel/Cameras{room}.png")
    cam_room_cache[room] = pygame.transform.scale(img, (1460,1080)).convert_alpha()
OriginalCamPlan = cam_room_cache["You"]
CamPlan = OriginalCamPlan

room_img = pygame.image.load("assets/IMAGE/Room.png").convert()
room_img = pygame.transform.scale(room_img, (2420,1080)).convert()
accurate_room_img = room_img
the_guy_room = pygame.image.load("assets/IMAGE/Room_THE_GUY.png").convert()
the_guy_room = pygame.transform.scale(the_guy_room, (2420,1080)).convert()
The_guy_jumpscare = pygame.image.load("assets/IMAGE/THE_GUY.png").convert_alpha()
The_guy_jumpscare = pygame.transform.scale(The_guy_jumpscare, (1920,1080)).convert_alpha()
Blood = pygame.image.load("assets/IMAGE/Blood.png").convert()
Blood = pygame.transform.scale(Blood, (1920,1080)).convert() 


font = pygame.font.Font("assets/FONTS/witchwoode/Witchwoode-Regular.otf", 52)
monitor_imgs = []
for i in range(1, 6):
    img = pygame.image.load(f"assets/IMAGE/camera/monitor{i}.png").convert_alpha()
    img = pygame.transform.scale(img, (2060,1080))
    monitor_imgs.append(img)
menu = True

# Menu loop

menuMusic = pygame.mixer.Sound("assets/MUSIC/menu1.mp3")
menuMusic.play(-1)  
start_img = pygame.image.load("assets/IMAGE/Start.png").convert_alpha()
start_img = pygame.transform.scale(start_img, (320,120))
The_guy_AI = pygame.image.load("assets/IMAGE/The_guy_AI.jpg").convert()
The_guy_AI = pygame.transform.scale(The_guy_AI, (400,400))
arrow_up = pygame.image.load("assets/IMAGE/arrow-up.png").convert_alpha()
arrow_down = pygame.image.load("assets/IMAGE/arrow-down.png").convert_alpha()
face_AI = pygame.image.load("assets/IMAGE/Face_AI.png").convert()
face_AI = pygame.transform.scale(face_AI, (400,400))
click = pygame.mixer.Sound("assets/SOUND/click.mp3")
extra = False
extra_img = pygame.image.load("assets/IMAGE/extras.png").convert_alpha()
extra_img = pygame.transform.scale(extra_img, (220,80)).convert_alpha()
back_img = pygame.image.load("assets/IMAGE/back.png").convert_alpha()
back_img = pygame.transform.scale(back_img, (220,80)).convert_alpha()
nightmare_img = pygame.image.load("assets/IMAGE/text/nightmare.png").convert_alpha()
nightmare_img = pygame.transform.scale(nightmare_img, (250,82)).convert_alpha()
radar_img = pygame.image.load("assets/IMAGE/text/radar.png").convert_alpha()
radar_img = pygame.transform.scale(radar_img, (230,70)).convert_alpha()
dark_img = pygame.image.load("assets/IMAGE/text/Dark.png").convert_alpha()
dark_img = pygame.transform.scale(dark_img, (270,74)).convert_alpha()
radar = False
nightmare = False
dark_mode = False
tutorial_step = 0
tutorial_btn = pygame.image.load("assets/IMAGE/tutorial.png").convert_alpha()
tutorial_btn = pygame.transform.scale(tutorial_btn, (280,70)).convert_alpha()
tutorial_texts = ["Welcome to Five Night Stand! In this game, you wake up in an abondend hotel.\nYour goal is to survive until 6 AM while avoiding enemies.\n    (disclamer: this game doesn't have 5 nights, it's just a name...)",
                  "You can move the view left and right by pressing A and D\nYou can check the cameras by pressing S.\nAlso you can use the flashlight by pressing Q,\nit can scare the enemies away, but not allways.",
                  "On the camera view you can click on the rooms(diamonds)\nto select them and then use the audio lure to lure The guy to that room.\nFirst Audio lure works 100 percent of the time, but after each use,\nthe number goes down. Also, lure isn't that loud, so use it closely to the guy",
                  "You can lock one door at a time by clicking on the door on the camera view.\nAnd... the Scan button... it's self explanatory, it scans the whole place",
                  "Hope you enjoy the game! If you have any questions\nsuggestions or found a bug, contact me on discord: magdoon"]
tutorial_font = pygame.font.Font("assets/FONTS/Kinnora.otf", 46)


while menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu = False
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if not extra and tutorial_step == 0:
                if 800 <= mouse_pos[0] <= 1120 and 800 <= mouse_pos[1] <= 920:
                    menu = False
                if 300 <= mouse_pos[0] <= 520 and 100 <= mouse_pos[1] <= 180:
                    extra = True
                if 730 <= mouse_pos[0] <= 850 and 250 <= mouse_pos[1] <= 450:
                    click.play()
                    enemies["The_guy"]["AI"] += 5
                    if enemies["The_guy"]["AI"] > 100:
                        enemies["The_guy"]["AI"] = 100
                if 730 <= mouse_pos[0] <= 850 and 465 <= mouse_pos[1] <= 650:
                    click.play()
                    enemies["The_guy"]["AI"] -= 5
                    if enemies["The_guy"]["AI"] < 0:
                        enemies["The_guy"]["AI"] = 0
                if 1530 <= mouse_pos[0] <= 1650 and 250 <= mouse_pos[1] <= 450:
                    click.play()
                    enemies["Face"]["AI"] += 5
                    if enemies["Face"]["AI"] > 100:
                        enemies["Face"]["AI"] = 100
                if 1530 <= mouse_pos[0] <= 1650 and 465 <= mouse_pos[1] <= 650:
                    click.play()
                    enemies["Face"]["AI"] -= 5
                    if enemies["Face"]["AI"] < 0:
                        enemies["Face"]["AI"] = 0
                if 1300 <= mouse_pos[0] <= 1580 and 100 <= mouse_pos[1] <= 180:
                    tutorial_step += 1
            elif tutorial_step > 0 and tutorial_step < 5:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    tutorial_step += 1
            elif tutorial_step == 5:
                tutorial_step = 0
            else:
                if 300 <= mouse_pos[0] <= 520 and 100 <= mouse_pos[1] <= 180:
                    extra = False
                if 600 <= mouse_pos[0] <= 890 and 385 <= mouse_pos[1] <= 440:
                    click.play()
                    nightmare = not nightmare
                if 600 <= mouse_pos[0] <= 890 and 550 <= mouse_pos[1] <= 605:
                    click.play()
                    radar = not radar
                if 600 <= mouse_pos[0] <= 890 and 700 <= mouse_pos[1] <= 750:
                    click.play()
                    dark_mode = not dark_mode
    SCREEN.blit(CamBackground[CamBackground_frame], (0, 0))
    CamBackground_frame = (CamBackground_frame + 1) % len(CamBackground)
    if not extra and tutorial_step == 0:
        SCREEN.blit(extra_img,(300,100))
        SCREEN.blit(start_img,(800,800))
        SCREEN.blit(tutorial_btn,(1300,100))
        SCREEN.blit(The_guy_AI,(300,250))
        SCREEN.blit(face_AI,(1100,250))
        SCREEN.blit(arrow_up,(710,250))
        SCREEN.blit(arrow_down,(710,450))
        SCREEN.blit(arrow_up,(1510,250))
        SCREEN.blit(arrow_down,(1510,450))
        SCREEN.blit(pygame.font.Font.render(font,str(enemies["The_guy"]["AI"]),True,(255,255,255)),(480,704))
        SCREEN.blit(pygame.font.Font.render(font,str(enemies["Face"]["AI"]),True,(255,255,255)),(1280,704))
    elif tutorial_step == 1:
        SCREEN.blit(pygame.font.Font.render(tutorial_font,tutorial_texts[0],True,(255,255,255)),(100,300))
    elif tutorial_step == 2:
        SCREEN.blit(pygame.font.Font.render(tutorial_font,tutorial_texts[1],True,(255,255,255)),(100,300))
        SCREEN.blit(pygame.transform.scale(room_img,(605,270)),(1000,600))
    elif tutorial_step == 3:
        SCREEN.blit(pygame.font.Font.render(tutorial_font,tutorial_texts[2],True,(255,255,255)),(100,200))
        SCREEN.blit(pygame.transform.scale(CamPlan,(1095,810)),(500,300))
        pygame.draw.circle(SCREEN,(255,255,255),(500+807,300+310), 40,3)
        pygame.draw.line(SCREEN,(255,40,40),(500+807+12,300+310-4),(500+807+75,300+310-20),3)
        pygame.draw.line(SCREEN,(255,40,40),(500+807+12,300+310-4),(500+807+20,300+310-20),3)
        pygame.draw.line(SCREEN,(255,40,40),(500+807+12,300+310-4),(500+807+26,300+310+10),3)
        pygame.draw.line(SCREEN,(255,40,40),(590,550),(590-70,550+20),3)
        pygame.draw.line(SCREEN,(255,40,40),(590,550),(590-20,550+20),3)
        pygame.draw.line(SCREEN,(255,40,40),(590,550),(590-27,550-10),3)
    elif tutorial_step == 4:
        SCREEN.blit(pygame.font.Font.render(tutorial_font,tutorial_texts[3],True,(255,255,255)),(100,300))
        SCREEN.blit(pygame.transform.scale(CamPlan,(1095,810)),(500,300))
        pygame.draw.circle(SCREEN,(255,255,255),(560+805,330+304), 40,3)
        pygame.draw.line(SCREEN,(255,40,40),(570+807+12,330+310-4),(570+807+75,330+310-20),3)
        pygame.draw.line(SCREEN,(255,40,40),(570+807+12,330+310-4),(570+807+20,330+310-20),3)
        pygame.draw.line(SCREEN,(255,40,40),(570+807+12,330+310-4),(570+807+26,330+310+10),3)
        pygame.draw.line(SCREEN,(255,40,40),(590,630),(590-70,630+20),3)
        pygame.draw.line(SCREEN,(255,40,40),(590,630),(590-20,630+20),3)
        pygame.draw.line(SCREEN,(255,40,40),(590,630),(590-27,630-10),3)
    elif tutorial_step == 5:
        SCREEN.blit(pygame.font.Font.render(tutorial_font,tutorial_texts[4],True,(255,255,255)),(100,300))
    else:
        SCREEN.blit(back_img,(300,100))
        pygame.draw.rect(SCREEN, (255,255,255),(600,400,30,30), 0 if nightmare else 2)
        SCREEN.blit(nightmare_img,(640,380))
        pygame.draw.rect(SCREEN, (255,255,255),(600,550,30,30), 0 if radar else 2)
        SCREEN.blit(radar_img,(640,536))
        pygame.draw.rect(SCREEN, (255,255,255),(600,700,30,30), 0 if dark_mode else 2)
        SCREEN.blit(dark_img,(640,686))
    pygame.display.update()
    dt = clock.tick(30) 
    if dt > 100:
        print("Lag spike:", dt, "ms")

pygame.mixer.stop()
gameMusic = pygame.mixer.Sound("assets/MUSIC/Game1.mp3")
gameMusic.play(-1)  
#Game loop

while running:
    flashlight_toogle = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and not animating:
                sfx.CameraPullUp()
                animating = True
                anim_frame = 0
                anim_timer = 0
                turning_on = not CamON

# Scan button & Audio Lure button

        if event.type == pygame.MOUSEBUTTONDOWN and CamON:
            mouse_pos = pygame.mouse.get_pos()
            # if 364 <= mouse_pos[0] <= 544 and 323 <= mouse_pos[0] <= 411 and AudioLureTimer == 0:

            if audio_lure_button_rect.collidepoint(mouse_pos) and AudioLureTimer == 0 and SelectedCam != "":
                AudioLureTimer = 200
                AudioLure_sfx.play()
                roomToMove = The_guy.AudioLure(enemies["The_guy"]['room'], enemies["The_guy"]['AI'], SelectedCam, LockedDoor)
                enemies["The_guy"]["room"] = roomToMove
            if 365 <= mouse_pos[0] <= 545 and 443 <= mouse_pos[1] <= 531 and ScanTimer == 0 and not radar:
                pygame.mixer.Sound("assets/SOUND/scan.mp3").play()
                ScanDuration = ScanDurationMax
                ScanTimer = 900
            if AudioLureTimer == 0:
                if 735 <= mouse_pos[0] <= 775 and 850 <= mouse_pos[1] <= 910 and SelectedCam != "C":
                    SelectedCam = "C"
                if 737 <= mouse_pos[0] <= 777 and 650 <= mouse_pos[1] <= 710 and SelectedCam != "LH":
                    SelectedCam = "LH"
                if 1400 <= mouse_pos[0] <= 1440 and 640 <= mouse_pos[1] <= 700 and SelectedCam != "BH":
                    SelectedCam = "BH"
                if 1310 <= mouse_pos[0] <= 1350 and 710 <= mouse_pos[1] <= 770 and SelectedCam != "BR":
                    SelectedCam = "BR"
                if 1305 <= mouse_pos[0] <= 1345 and 430 <= mouse_pos[1] <= 490 and SelectedCam != "E":
                    SelectedCam = "E"
                if 995 <= mouse_pos[0] <= 1035 and 430 <= mouse_pos[1] <= 490 and SelectedCam != "DB":
                    SelectedCam = "DB"
                if 937 <= mouse_pos[0] <= 977 and 428 <= mouse_pos[1] <= 488 and SelectedCam != "DA":
                    SelectedCam = "DA"
                if 935 <= mouse_pos[0] <= 975 and 505 <= mouse_pos[1] <= 565 and SelectedCam != "A":
                    SelectedCam = "A"
# Door locking
            if DoorTimer == 0:
                if door_positions["DA"][0] <= mouse_pos[0] <= door_positions["DA"][0]+60 and door_positions["DA"][1] <= mouse_pos[1] <= door_positions["DA"][1]+22:
                    if LockedDoor == "DA":
                        LockedDoor = None
                    else:
                        LockedDoor = "DA"
                elif door_positions["E"][0] <= mouse_pos[0] <= door_positions["E"][0]+60 and door_positions["E"][1] <= mouse_pos[1] <= door_positions["E"][1]+22:
                    if LockedDoor == "E":
                        LockedDoor = None
                    else:
                        LockedDoor = "E"
                elif door_positions["UH"][0] <= mouse_pos[0] <= door_positions["UH"][0]+60 and door_positions["UH"][1] <= mouse_pos[1] <= door_positions["UH"][1]+22:
                    if LockedDoor == "UH":
                        LockedDoor = None
                    else:
                        LockedDoor = "UH"
                else:
                    continue
                sfx.MetalDoor("close")
                DoorTimer = 200
    if ScanDuration > 0 and not radar:
        if ScanDuration % 60 < 30:
            CamPlan = cam_room_cache.get(enemies["The_guy"]['room'], OriginalCamPlan)
        else:
            CamPlan = OriginalCamPlan
        ScanDuration -= 1
    
    if ScanDuration == 0 and not radar:
        CamPlan = OriginalCamPlan

    if radar:
        if pygame.time.get_ticks() % 1000 < 500:
            CamPlan = cam_room_cache.get(enemies["The_guy"]['room'], OriginalCamPlan)
        else:
            CamPlan = OriginalCamPlan
    
        
              
# Exit button         
                    
    key = pygame.key.get_pressed()
    # if key[pygame.K_ESCAPE]:
    #     win = False
    #     running = False
# Flashlight
    if key[pygame.K_q] and not CamON:
        flashlight_toogle = True
        

# Enemy movement
    EnemyMoveTimer += 1
    if EnemyMoveTimer >= 300:
        EnemyMoveTimer = 0
        for enemy in enemies:
            current_room = enemies[enemy]["room"]
            AI = enemies[enemy]["AI"]
            new_room = The_guy.move(current_room, AI, LockedDoor, nightmare)
            enemies[enemy]["room"] = new_room
    if enemies["The_guy"]["room"] == "You" and AttackTimer < 600:
        AttackTimer += 1
    if AttackTimer >= 600:
        if CamON:
            animating = True
            anim_frame = 0
            anim_timer = 0
            turning_on = not CamON
            Jumpscare = True
            CamON = False
        if flashlight_toogle:
            Jumpscare = True
            flashlight_toogle = False
    if enemies["The_guy"]["room"] == "You" and CamON:
        room_img = the_guy_room
    if enemies["The_guy"]["room"] != "You" and room_img == the_guy_room:
        room_img = accurate_room_img


# Time and hour system

    current_time = pygame.time.get_ticks()
    if (current_time - last_hour_time) // 1000 >= 45:
        hour += 1
        last_hour_time = current_time
    if hour in (0,1,2):
        display_time = f"{10+hour}:00 PM"
    else:
        display_time = f"{hour-2}:00 AM"
    if hour >= 8:
        win = True
        running = False
    if hour == 7 and (current_time - last_hour_time) // 1000 == 37 and last7one == 0:
        last7.play()
        last7one += 1

# Camera movement
    if not CamON and not animating:
        if key[pygame.K_a]:
            CamX += cameraMove
            if CamX > 0:
                CamX = 0
            if CamX < -500:
                CamX = -500
        if key[pygame.K_d]:
            CamX -= cameraMove
            if CamX < -500:
                CamX = -500
            if CamX > 0:
                CamX = 0
    if animating:
        anim_timer += clock.get_time()
        if anim_timer >= anim_delay:
            anim_frame += 1
            anim_timer = 0
        if anim_frame >= 5:
            animating = False
            anim_frame = 4 
            CamON = turning_on
    if animating:
        if turning_on:
            SCREEN.blit(monitor_imgs[anim_frame], (-40, 0))
        else:
            SCREEN.blit(room_img, (CamX, 0))
            SCREEN.blit(monitor_imgs[4 - anim_frame], (-40, 0))
    elif CamON:             #Camera screen render
    
        SCREEN.blit(CamBackground[CamBackground_frame], (0, 0))
        CamBackground_frame = (CamBackground_frame + 1) % len(CamBackground)

# Audio Lure
        if LockedDoor in door_positions:
            pos = door_positions[LockedDoor]
            pygame.draw.rect(SCREEN, (255,255,255), (pos[0],pos[1],59,22))
        SCREEN.blit(CamPlan, (250, 50))
        if SelectedCam in room_positions:
            pos = (room_positions[SelectedCam][0]-44,room_positions[SelectedCam][1]-29)
            if AudioLureTimer > 0 and AudioLureTimer % 10 < 5:
                SCREEN.blit(AudioLure_img, pos)
            pos = room_positions[SelectedCam]
            pygame.draw.circle(SCREEN,(100,100,100), pos, 10)

        if ScanTimer > 0:
                for i in range((ScanTimer//150) + 1):
                    pygame.draw.rect(SCREEN, (100, 100, 100), (355 + i*36 + i/3, 543, 18, 18))
        TIME = pygame.font.Font.render(font, display_time, True, (255, 255, 255))
        SCREEN.blit(TIME, (80, 75))
        pygame.display.update()
    else:                   #Room screen render
        SCREEN.blit(room_img, (CamX, 0))
        if enemies["Face"]["alpha"] > 30:
            face_room_img.set_alpha(enemies["Face"]["alpha"])
            SCREEN.blit(face_room_img,(CamX+1300,200))
        if flashlight_toogle:
            SCREEN.blit(flashlight_img,(460,40))
        if enemies["Face"]["alpha"] >= 255:
            Jumpscare = True
    sfx.flashlight(flashlight_toogle)
        
    pygame.display.update()

# Jumpscare

    if Jumpscare and not animating:
        SCREEN.blit(accurate_room_img, (CamX, 0))
        if enemies["Face"]["alpha"] >= 255:
            SCREEN.blit(pygame.transform.scale(pygame.image.load("assets/IMAGE/RoomDark.png"),(2420,1080)),(CamX,0))
            SCREEN.blit(face_jumpscare,(300,0))
        else:
            SCREEN.blit(The_guy_jumpscare, (0, 0))
        pygame.mixer.stop()
        jumpscareSFX.play()
        pygame.display.update()
        pygame.time.wait(2300)
        pygame.mixer.stop()
        SCREEN.blit(Blood, (0, 0))
        pygame.display.update()
        pygame.time.wait(2000)
        win = False
        running = False

# SFX
    dt = clock.tick(60) 
    if dt > 100:
        print("Lag spike:", dt, "ms")
    sfx.SFX(CamON, dt)

    ScanTimer -= 1
    AudioLureTimer -=1
    DoorTimer -=1
    if AudioLureTimer < 0:
        AudioLureTimer = 0
    if ScanTimer < 0:
        ScanTimer = 0
    if DoorTimer < 0:
        DoorTimer = 0
    if not flashlight_toogle:
        enemies["Face"]["alpha"] += enemies["Face"]["AI"]/250
        if nightmare and enemies["Face"]["alpha"] < 20:
            enemies["Face"]["alpha"] = 20
            
    else:
        enemies["Face"]["alpha"] -= 0.75 if dark_mode else 4
    if enemies["Face"]["alpha"] < 0:
        enemies["Face"]["alpha"] = 0
    
if win:
    SCREEN.blit(Win_img, (0, 0))
    pygame.mixer.stop()
    Win_sfx.play()
    pygame.display.update()
    pygame.time.wait(7000)
pygame.quit()