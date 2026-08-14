import pygame, random, math
import assets.AI.The_guy as The_guy
from lib import girl, music_manager
import lib.sfx_manager as sfx
from lib.camera_manager import camera_manager, door_manager
import lib.locust as locust
from lib.menu_manager import menu_GUI
from lib.music_manager import play_music, music_stop
from lib.settings_manager import image_render, settings_data_render, settings_data_save, settings_logic, settings_render
from minigames.minigame1 import minigame

pygame.init()
pygame.mixer.init()
pygame.font.init()

clock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

game_on = True
flashlight_tutorial_imgs = []
flash_frame = 0
monitor_imgs = []

width, height = SCREEN.get_size()

al_counter_on, show_timer_on = settings_data_render()

for i in range(1,204):  #flashlight video in tutorial
    img = pygame.image.load(f"assets/VIDEO/flashlight/image{i}.png").convert()
    img = pygame.transform.scale(img,(width*0.25,height*0.25)).convert()
    flashlight_tutorial_imgs.append(img)

CamBackground = []
for i in range(1, 47):
        img = pygame.image.load(f"assets/VIDEO/camera_BACK_frames/frame_{i:04d}.png").convert()
        CamBackground.append(img)
for i in range(1, 6):
        img = pygame.image.load(f"assets/IMAGE/camera/monitor{i}.png").convert_alpha()
        img = pygame.transform.scale(img, (width * 1.073, height))
        monitor_imgs.append(img)

radar = False
nightmare = False
dark_mode = False
short_night = False
inverted_controls = False
battery = False
nightmare_text_rect = pygame.Rect(0, 0, 0, 0)
radar_text_rect = pygame.Rect(0, 0, 0, 0)
dark_mode_text_rect = pygame.Rect(0, 0, 0, 0)
inverted_controls_text_rect = pygame.Rect(0, 0, 0, 0)
battery_text_rect = pygame.Rect(0, 0, 0, 0)
short_night_text_rect = pygame.Rect(0, 0, 0, 0)
the_guy_AI_value = 40
face_AI_value = 40
girl_AI_value = 40


while game_on:
    enemies = {"The_guy": {"room": "E", "AI": 40}, "Face" : {"room": "You", "AI":40, "alpha" : 0}, "locust" : {"room":"DB", "AI":0}, "girl" : {"room":"C", "AI":0, "pos":0}}
    enemies["The_guy"]["AI"] = the_guy_AI_value
    enemies["Face"]["AI"] = face_AI_value
    enemies["girl"]["AI"] = girl_AI_value
    animating = False
    anim_frame = 0
    anim_timer = 0
    anim_delay = 30
    hour = 0
    timer = 0
    display_time = "10:00 PM"
    last_hour_time = pygame.time.get_ticks()

    last7one = 0

    Win_img = pygame.image.load("assets/IMAGE/6AM.png").convert()
    Win_img = pygame.transform.scale(Win_img, (width,height)).convert()

    the_guy_move_timer = 0
    AttackTimer = 0
    Jumpscare = False

    music_manager.volume_update()
    sfx.volume_update()

    face_room_img = pygame.image.load("assets/IMAGE/Face_room.png").convert_alpha()
    face_jumpscare = pygame.image.load("assets/IMAGE/Face.png").convert_alpha()
    face_jumpscare = pygame.transform.scale(face_jumpscare,(width*0.7,height))
    running = True
    win = False
    reset_progress = False

    flashlight_img = pygame.image.load("assets/IMAGE/flashlight.png").convert_alpha()
    flashlight_img = pygame.transform.scale(flashlight_img, (width * 0.52, height * 0.92))
    flashlight_toogle = False


    SelectedCam = ""
    room_positions = {
        "A": (width*0.487, height*0.502),
        "BH": (width*0.729, height*0.624),
        "BR": (width*0.681, height*0.692),
        "E": (width*0.6795, height*0.432),
        "C": (width*0.383, height*0.82),
        "DA": (width*0.488, height*0.429),
        "DB": (width*0.519, height*0.43),
        "LH": (width*0.384, height*0.636)
    }
    door_positions = {
        "DA" : (width*0.358, height*0.456),
        "E" : (width*0.7075, height*0.456),
        "UH" : (width*0.623, height*0.651)
    }
    ScanTimer = 0
    ScanDuration = 0
    ScanDurationMax = 200
    AudioLureTimer = 0
    DoorTimer = 0
    AudioLure_img = pygame.image.load("assets/IMAGE/plan of the hotel/AudioLure.png")
    AudioLure_img = pygame.transform.scale(AudioLure_img,(width*0.045,height*0.05)).convert_alpha()
    LockedDoor = None
    audio_lure_button_rect = pygame.Rect(width*0.18, height*0.3, width*0.095, height*0.08)
    

    cameraMove = 15
    CamON = False
    CamX = width//-8
    
    CamBackground_frame = 0
    cam_room_cache = {}
    for room in ["You", "DA", "DB", "LH", "UH", "LoH", "A", "B", "C", "BR", "BH", "E"]:
        img = pygame.image.load(f"assets/IMAGE/plan of the hotel/Cameras{room}.png")
        cam_room_cache[room] = pygame.transform.scale(img, (width*0.76, height)).convert_alpha()
    OriginalCamPlan = cam_room_cache["You"]
    CamPlan = OriginalCamPlan

    room_img = pygame.image.load("assets/IMAGE/Room.png")
    room_img = pygame.transform.scale(room_img, (width*1.26, height)).convert()
    accurate_room_img = room_img
    the_guy_room = pygame.image.load("assets/IMAGE/Room_THE_GUY.png")
    the_guy_room = pygame.transform.scale(the_guy_room, (width*1.26, height)).convert()
    The_guy_jumpscare = pygame.image.load("assets/IMAGE/THE_GUY.png")
    The_guy_jumpscare = pygame.transform.scale(The_guy_jumpscare, (width, height)).convert_alpha()
    Blood = pygame.image.load("assets/IMAGE/Blood.png")
    Blood = pygame.transform.scale(Blood, (width, height)).convert() 
    locust_camera = pygame.image.load("assets/IMAGE/locust_cameras.png")
    locust_camera = pygame.transform.scale(locust_camera,(height,height)).convert_alpha()
    room_locust = pygame.transform.scale(pygame.image.load("assets/IMAGE/locust_room.png"),(width*0.2,height*0.65)).convert_alpha()
    girl_room_left = pygame.image.load("assets/IMAGE/girl_left.png")
    girl_room_left = pygame.transform.scale(girl_room_left,(width*0.05,height*0.1))
    girl_room_right = pygame.image.load("assets/IMAGE/girl_right.png")
    girl_room_right = pygame.transform.scale(girl_room_right,(width*0.05,height*0.1))
    sfx_img = pygame.image.load("assets/IMAGE/sfx_icon.png")
    sfx_img = pygame.transform.scale(sfx_img, (height*0.1,height*0.1))
    girl_kill_timer = 0
    face_offset = 0

    font_small = pygame.font.Font("assets/FONTS/witchwoode/Witchwoode-Regular.otf", 26)
    font = pygame.font.Font("assets/FONTS/witchwoode/Witchwoode-Regular.otf", 52)
    font_title = pygame.font.Font("assets/FONTS/witchwoode/Witchwoode-Regular.otf", 92)
    fancy_font = pygame.font.Font("assets/FONTS/moglandemo.regular.ttf", 52)
    fancy_font_title = pygame.font.Font("assets/FONTS/moglandemo.regular.ttf", 72)
    timer_font = pygame.font.Font("assets/FONTS/Roboto-Light.ttf", 52)
    timer_font_small = pygame.font.Font("assets/FONTS/Roboto-Light.ttf", 32)
    menu = True

    image_render(SCREEN,width,height)

    try:
        with open("lib/text/progres/game.txt", "r+") as progress:
            progress_data = progress.read().splitlines()
            print(progress_data)
        try:
            night = int(progress_data[1])
            extras_unlocked = progress_data[3]
            nightmare_beaten = progress_data[5]
            deaf_mode_beaten = progress_data[7]
            deaf_unlocked = progress_data[9]
        except IndexError or ValueError:
            with open("lib/text/progres/game.txt", "w+") as progress:
                progress.write("Night\n1\n")
                progress.write("Extras\nFalse\n")
                progress.write("Nightmare\nFalse\n")
                progress.write("deaf_mode_beaten:\nFalse\n")
                progress.write("deaf_unlocked:\nFalse")
                night = 1
                extras_unlocked = "False"
                nightmare_beaten = "False"
                deaf_mode_beaten = "False"
                deaf_unlocked = "False"
        if night not in (1,2,3,4,5) or extras_unlocked not in ("True","False") or nightmare_beaten not in ("True","False") or deaf_mode_beaten not in ("True","False") or deaf_unlocked not in ("True","False"):
            with open("lib/text/progres/game.txt", "w+") as progress:
                progress.write("Night\n1\n")
                progress.write("Extras\nFalse\n")
                progress.write("Nightmare\nFalse\n")
                progress.write("deaf_mode_beaten:\nFalse\n")
                progress.write("deaf_unlocked:\nFalse")
    except FileNotFoundError:
        with open("lib/text/progres/game.txt", "w+") as progress:
            progress.write("Night\n1\n")
            progress.write("Extras\nFalse\n")
            progress.write("Nightmare\nFalse\n")
            progress.write("deaf_mode_beaten:\nFalse\n")
            progress.write("deaf_unlocked:\nFalse")
    with open("lib/text/progres/game.txt", "r+") as progress:
        progress_data = progress.read().splitlines()
    night = int(progress_data[1])
    extras_unlocked = progress_data[3]
    nightmare_beaten = progress_data[5]
    deaf_mode_beaten = progress_data[7]
    deaf_unlocked = progress_data[9]

    
    The_guy.reset_audio_lures()

    
    arrow_up = pygame.image.load("assets/IMAGE/arrow_up.png").convert_alpha()
    arrow_up = pygame.transform.scale(arrow_up, (width*0.04,width*0.04))
    arrow_down = pygame.image.load("assets/IMAGE/arrow_down.png").convert_alpha()
    arrow_down = pygame.transform.scale(arrow_down, (width*0.04,width*0.04))
    The_guy_AI = pygame.image.load("assets/IMAGE/The_guy_AI.jpg").convert()
    The_guy_AI = pygame.transform.scale(The_guy_AI, (width*0.13,width*0.13))
    the_guy_arrow_up_rect = pygame.Rect(width//5.5+The_guy_AI.get_width()*1.05, height//2.1 - arrow_up.get_height()*1.2, arrow_up.get_width(), arrow_up.get_height())
    the_guy_arrow_down_rect = pygame.Rect(width//5.5+The_guy_AI.get_width()*1.05, height//2.1 + arrow_down.get_height()*0.2, arrow_down.get_width(), arrow_down.get_height())
    face_AI = pygame.image.load("assets/IMAGE/Face_AI.png").convert()
    face_AI = pygame.transform.scale(face_AI, (width*0.13,width*0.13))
    face_arrow_up_rect = pygame.Rect(((width//5.5)*2.25)+face_AI.get_width()*1.05, height//2.1 - arrow_up.get_height()*1.2, arrow_up.get_width(), arrow_up.get_height())
    face_arrow_down_rect = pygame.Rect(((width//5.5)*2.25)+face_AI.get_width()*1.05, height//2.1 + arrow_down.get_height()*0.2, arrow_down.get_width(), arrow_down.get_height())
    girl_AI = pygame.image.load("assets/IMAGE/girl_AI.png").convert()
    girl_AI = pygame.transform.scale(girl_AI, (width*0.13,width*0.13))
    girl_arrow_up_rect = pygame.Rect(((width//5.5)*3.5)+girl_AI.get_width()*1.05, height//2.1 - arrow_up.get_height()*1.2, arrow_up.get_width(), arrow_up.get_height())
    girl_arrow_down_rect = pygame.Rect(((width//5.5)*3.5)+girl_AI.get_width()*1.05, height//2.1 + arrow_down.get_height()*0.2, arrow_down.get_width(), arrow_down.get_height())
    start_text = pygame.font.Font.render(font_title, "Start", True, (255,255,255))
    start_rect = start_text.get_rect(topleft=(width//2 - 200,height//2 + 320))
    block_img = pygame.image.load("assets/IMAGE/block.png")
    block_img = pygame.transform.scale(block_img,(width*0.27-width*0.18,height*0.49 - height*0.41))
    battery_img = [
        pygame.transform.scale(pygame.image.load("assets/IMAGE/battery/battery_none.png"),(width*0.045,height*0.15)),
        pygame.transform.scale(pygame.image.load("assets/IMAGE/battery/battery_low.png"),(width*0.045,height*0.15)),
        pygame.transform.scale(pygame.image.load("assets/IMAGE/battery/battery_low_mid.png"),(width*0.045,height*0.15)),
        pygame.transform.scale(pygame.image.load("assets/IMAGE/battery/battery_mid.png"),(width*0.045,height*0.15)),
        pygame.transform.scale(pygame.image.load("assets/IMAGE/battery/battery_high_mid.png"),(width*0.045,height*0.15)),
        pygame.transform.scale(pygame.image.load("assets/IMAGE/battery/battery_full.png"),(width*0.045,height*0.15)),
    ]
    battery_amount = 100

    reset_text = pygame.font.Font.render(fancy_font,"Reset",True,(255,255,255))
    reset_text_rect = reset_text.get_rect(topleft=(width-reset_text.get_width()*1.2,height-reset_text.get_height()*1.2))

    running_left_audio_sfx_rect = pygame.Rect(width//2-sfx_img.get_width()*1.2,height-sfx_img.get_height()*1.2,sfx_img.get_width(),sfx_img.get_height())
    running_right_audio_sfx_rect = pygame.Rect(width//2+sfx_img.get_width()*0.2,height-sfx_img.get_height()*1.2,sfx_img.get_width(),sfx_img.get_height())
    close_steps_audio_sfx_rect = pygame.Rect(width//2-sfx_img.get_width()//2,height-sfx_img.get_height()*1.2,sfx_img.get_width(),sfx_img.get_height())

    girl_rect = (0,0,0,0)
    girl_disappear_timer = 0
    girl_disappearing = False
   
    extra = False
    custom_night = False
    settings = False
    play = True
    progress_star = pygame.image.load("assets/IMAGE/progress_star.png").convert_alpha()
    progress_star = pygame.transform.scale(progress_star, (width*0.05,width*0.05)).convert_alpha()
    
   
    tutorial_step = 0
    tutorial_texts = [
    "Welcome to Five Night Stand! You wake up in an abandoned hotel.\nYour goal is to survive until 6 AM while avoiding the enemies.",
    "Move the view with A and D.\nCheck the cameras with S and use the flashlight with Q.\nIt can scare some enemies away, but it's not a sollution to every problem.",
    "On the cameras, click on a room (diamond) to select it,\nthen use the Audio Lure to lure The Guy there.\nEach use makes it less reliable.\nThe lure isn't very loud, so use it close to him.",
    "You can lock one door at a time by clicking it on the camera map\n and use the Scan button to reveal where The Guy is.\nbut be aware, it has a cooldown",
    "Sometimes, while watching the cameras, you may hear a quiet \"psst.\"\nIf you do, look around.\nYou might find her somewhere by the side of the room.\nClick her before she leaves.\nIf you ignore her... things may get worse.",
    "You found something you weren't supposed to.\n\nIt was part of 20/15 mode. No one really knew what it was supposed to be.\nIt would appear to the left of the Exit, then rapidly pace back and forth.\nWatching.\nOr at least, that's what it looked like.",
    "It gets closer.\nThen farther.\nThen closer again.\n\nIf it gets close to your door, use the Audio Lure.\n",
    "If it pushes the door, use the flashlight on the side you heard it from.\n\nAnd i think that's all.\n\n...probably.\n"
]
    tutorial_font = pygame.font.Font("assets/FONTS/Kinnora.otf", 46)



    stars = 0
    if night > 5:
        night = 5
    if extras_unlocked == "True":
        stars +=1
    if nightmare_beaten == "True":
        stars +=1
    if deaf_mode_beaten == "True":
        stars +=1


    if night == 1:
        enemies["The_guy"]["AI"] = 10
        enemies["Face"]["AI"] = 0
        enemies["girl"]["AI"] = 0
    elif night == 2:
        enemies["The_guy"]["AI"] = 30
        enemies["Face"]["AI"] = 15
        enemies["girl"]["AI"] = 0
    elif night == 3:
        enemies["The_guy"]["AI"] = 40
        enemies["Face"]["AI"] = 50
        enemies["girl"]["AI"] = 0
    elif night == 4:
        enemies["The_guy"]["AI"] = 50
        enemies["Face"]["AI"] = 60
        enemies["girl"]["AI"] = 40
    elif night == 5 and extras_unlocked == "False":
        enemies["The_guy"]["AI"] = 70
        enemies["Face"]["AI"] = 80
        enemies["girl"]["AI"] = 70



        
    # Menu loop

    


    while menu:

        mouse_pos = pygame.mouse.get_pos()
        play_music("menu")

# Menu Display

        SCREEN.blit(CamBackground[CamBackground_frame], (0, 0))
        CamBackground_frame = (CamBackground_frame + 1) % len(CamBackground)
       
        if tutorial_step == 0:
            for i in range(stars):
                SCREEN.blit(progress_star,(0 + i*width*0.05, height*0.9))

            # Menu navigation    
            play_rect, custom_rect, extra_rect, settings_rect = menu_GUI(fancy_font_title, SCREEN, width, height, mouse_pos, play, custom_night, extras_unlocked, extra, settings)

            if extra:
            # Nightmare btn
                pygame.draw.rect(SCREEN, (255,255,255),(width//2 - 450,height//2-200,30,30), 0 if nightmare else 2)
                nightmare_text = pygame.font.Font.render(fancy_font, "Nightmare", True, (255,255,255))
                nightmare_text_rect = pygame.Rect(width//2 - 450,height//2 - 215,nightmare_text.get_width() + 50,nightmare_text.get_height())
                SCREEN.blit(nightmare_text, (width//2 - 400,height//2 - 215))

            # radar btn
                if not nightmare:
                    pygame.draw.rect(SCREEN, (255,255,255),(width//2 - 450, height//2,30,30), 0 if radar else 2)
                    radar_text = pygame.font.Font.render(fancy_font, "Radar", True, (255,255,255))
                    radar_text_rect = pygame.Rect(width//2 - 450, height//2-15,radar_text.get_width() + 50,radar_text.get_height())
                    SCREEN.blit(radar_text, (width//2 - 400, height//2 - 15))

            # dark_mode btn
                pygame.draw.rect(SCREEN, (255,255,255),(width//2 - 450, height//2+200,30,30), 0 if dark_mode else 2)
                dark_mode_text = pygame.font.Font.render(fancy_font, "Dark Mode", True, (255,255,255))
                dark_mode_text_rect = pygame.Rect(width//2 - 450, height//2 + 200,dark_mode_text.get_width() + 50,dark_mode_text.get_height())
                SCREEN.blit(dark_mode_text, (width//2 - 400, height//2 + 185))

            # inverted_controls btn
                pygame.draw.rect(SCREEN, (255,255,255),(width//2, height//2 - 200,30,30), 0 if inverted_controls else 2)
                inverted_controls_text = pygame.font.Font.render(fancy_font, "Inverted controls", True, (255,255,255))
                inverted_controls_text_rect = pygame.Rect(width//2, height//2 - 200,inverted_controls_text.get_width() + 50,inverted_controls_text.get_height())
                SCREEN.blit(inverted_controls_text, (width//2 + 50 , height//2 - 215))

            # Short_night btn
                pygame.draw.rect(SCREEN, (255,255,255),(width//2, height//2,30,30), 0 if short_night else 2)
                short_night_text = pygame.font.Font.render(fancy_font, "Short Night", True, (255,255,255))
                short_night_text_rect = pygame.Rect(width//2, height//2-15,short_night_text.get_width() + 50,short_night_text.get_height())
                SCREEN.blit(short_night_text, (width//2 + 50, height//2 - 15))

            # Battery btn
                pygame.draw.rect(SCREEN, (255,255,255),(width//2, height//2+200,30,30), 0 if battery else 2)
                battery_text = pygame.font.Font.render(fancy_font, "Battery", True, (255,255,255))
                battery_text_rect = pygame.Rect(width//2, height//2 + 200,battery_text.get_width() + 50,battery_text.get_height())
                SCREEN.blit(battery_text, (width//2 + 50, height//2 + 185))

                

            elif play:

                SCREEN.blit(pygame.font.Font.render(font,f"Night {night}",True,(255,255,255)),(width//2 - 100,height//1.45))
                if not nightmare and not radar and not dark_mode and not inverted_controls and not short_night and not battery:
                    SCREEN.blit(start_text, (width//2 - 120,height//1.3))
                    start_btn = pygame.draw.rect(SCREEN, (255,255,255), (width//2 - 170,height//1.3,start_rect.width+90, start_rect.height+10), 3)
                else:
                    extra_error_text = pygame.font.Font.render(font_small, "Turn off Extras to play normal nights", True, (100,100,100))
                    SCREEN.blit(extra_error_text, (width//2-230, height//1.3))


                tutorial_text = pygame.font.Font.render(fancy_font, "Tutorial", True, (255,90,90) if deaf_unlocked == "True" else (255,255,255))
                tutorial_btn_rect = pygame.Rect((width-tutorial_text.get_width()*1.3,height-tutorial_text.get_height()*1.15,tutorial_text.get_width()*1.2,tutorial_text.get_height()))
                pygame.draw.rect(SCREEN,(255,90,90) if deaf_unlocked == "True" else (255,255,255), tutorial_btn_rect, 3)
                SCREEN.blit(tutorial_text,(width-tutorial_text.get_width()*1.2,height-tutorial_text.get_height()*1.1))


            elif custom_night:
                if enemies['The_guy']['AI'] == 20 and enemies['Face']['AI'] == 15 and enemies['girl']['AI'] == 0:
                    color = (255,20,20)
                else:
                    color = (255,255,255)
                SCREEN.blit(The_guy_AI, (width//5.5, height//2.1 - The_guy_AI.get_height()//2))
                the_guy_AI_text = pygame.font.Font.render(font, f"{enemies['The_guy']['AI']}", True, color)
                SCREEN.blit(the_guy_AI_text, (width//5.5 + The_guy_AI.get_width()//2-the_guy_AI_text.get_width()//2, height//2.1 + The_guy_AI.get_height()//1.7))

                SCREEN.blit(face_AI, ((width//5.5)*2.25, height//2.1 - face_AI.get_height()//2))
                face_AI_text = pygame.font.Font.render(font, f"{enemies['Face']['AI']}", True, color)
                SCREEN.blit(face_AI_text, ((width//5.5)*2.25 + face_AI.get_width()//2-face_AI_text.get_width()//2, height//2.1 + face_AI.get_height()//1.7))

                SCREEN.blit(girl_AI, ((width//5.5)*3.5, height//2.1  - girl_AI.get_height()//2))
                girl_AI_text = pygame.font.Font.render(font, f"{enemies['girl']['AI']}", True, color)
                if enemies['girl']['AI'] != 0:
                    SCREEN.blit(girl_AI_text, ((width//5.5)*3.5 + girl_AI.get_width()//2-girl_AI_text.get_width()//2, height//2.1 + girl_AI.get_height()//1.7))

                SCREEN.blit(start_text, (width//2 - 120,height//1.2))
                start_btn = pygame.draw.rect(SCREEN, (255,255,255), (width//2 - 170,height//1.2,start_rect.width+90, start_rect.height+10), 3)

                if not nightmare:
                    # The Guy arrows
                    SCREEN.blit(arrow_up, (width//5.5+The_guy_AI.get_width()*1.05, height//2.1 - arrow_up.get_height()*1.2))
                    SCREEN.blit(arrow_down, (width//5.5+The_guy_AI.get_width()*1.05, height//2.1 + arrow_down.get_height()*0.2))
                    # Face arrows
                    SCREEN.blit(arrow_up, ((width//5.5)*2.25+face_AI.get_width()*1.05, height//2.1 - arrow_up.get_height()*1.2))
                    SCREEN.blit(arrow_down, ((width//5.5)*2.25+face_AI.get_width()*1.05, height//2.1 + arrow_down.get_height()*0.2))
                    # girl arrows
                    SCREEN.blit(arrow_up, ((width//5.5)*3.5+girl_AI.get_width()*1.05, height//2.1 - arrow_up.get_height()*1.2))
                    SCREEN.blit(arrow_down, ((width//5.5)*3.5+girl_AI.get_width()*1.05, height//2.1 + arrow_down.get_height()*0.2))

                    
                    SCREEN.blit(reset_text,(width-reset_text.get_width()*1.2,height-reset_text.get_height()*1.2))
                    if reset_text_rect.collidepoint(mouse_pos):
                        pygame.draw.rect(SCREEN,(255,255,255),(width-reset_text.get_width()*1.2, height-reset_text.get_height()*0.3, reset_text_rect.width, 3), 0)
            elif settings:
                settings_render(SCREEN, width, height, fancy_font)
                


        elif tutorial_step == 1:
            SCREEN.blit(pygame.font.Font.render(tutorial_font,tutorial_texts[0],True,(255,255,255)),(width*0.1,height*0.3))
        elif tutorial_step == 2:
            SCREEN.blit(pygame.font.Font.render(tutorial_font,tutorial_texts[1],True,(255,255,255)),(width*0.1,height*0.3))
            SCREEN.blit(flashlight_tutorial_imgs[int(flash_frame)], (width*0.55,height*0.55))
            flash_frame += 1/3
            if flash_frame >= 200:
                flash_frame = 0
        elif tutorial_step == 3:
            flash_frame = 0
            SCREEN.blit(pygame.font.Font.render(tutorial_font, tutorial_texts[2], True, (255,255,255)), (width*0.05, height*0.19))

            SCREEN.blit(pygame.transform.scale(CamPlan, (int(width*0.57), int(height*0.75))), (width*0.26, height*0.28))

            pygame.draw.circle(SCREEN, (255,255,255), (int(width*0.68), int(height*0.56)), height*0.04, 3)

            pygame.draw.line(SCREEN, (255,40,40), (int(width*0.69), int(height*0.56)), (int(width*0.72), int(height*0.55)), 3)
            pygame.draw.line(SCREEN, (255,40,40), (int(width*0.69), int(height*0.56)), (int(width*0.694), int(height*0.545)), 3)
            pygame.draw.line(SCREEN, (255,40,40), (int(width*0.69), int(height*0.56)), (int(width*0.7), int(height*0.57)), 3)

            pygame.draw.line(SCREEN, (255,40,40), (int(width*0.31), int(height*0.51)), (int(width*0.27), int(height*0.53)), 3)
            pygame.draw.line(SCREEN, (255,40,40), (int(width*0.31), int(height*0.51)), (int(width*0.30), int(height*0.53)), 3)
            pygame.draw.line(SCREEN, (255,40,40), (int(width*0.31), int(height*0.51)), (int(width*0.29), int(height*0.50)), 3)
        elif tutorial_step == 4:
            SCREEN.blit(pygame.font.Font.render(tutorial_font,tutorial_texts[3],True,(255,255,255)),(width*0.05,height*0.28))
            SCREEN.blit(pygame.transform.scale(CamPlan,(int(width*0.57),int(height*0.75))),(width*0.26,height*0.28))

            pygame.draw.circle(SCREEN,(255,255,255),(int(width*0.71),int(height*0.59)),40,3)

            pygame.draw.line(SCREEN,(255,40,40),(int(width*0.72),int(height*0.59)),(int(width*0.75),int(height*0.57)),3)
            pygame.draw.line(SCREEN,(255,40,40),(int(width*0.72),int(height*0.59)),(int(width*0.72),int(height*0.57)),3)
            pygame.draw.line(SCREEN,(255,40,40),(int(width*0.72),int(height*0.59)),(int(width*0.73),int(height*0.605)),3)

            pygame.draw.line(SCREEN,(255,40,40),(int(width*0.31),int(height*0.58)),(int(width*0.27),int(height*0.60)),3)
            pygame.draw.line(SCREEN,(255,40,40),(int(width*0.31),int(height*0.58)),(int(width*0.303),int(height*0.60)),3)
            pygame.draw.line(SCREEN,(255,40,40),(int(width*0.31),int(height*0.58)),(int(width*0.295),int(height*0.57)),3)
        elif tutorial_step == 5:
            SCREEN.blit(pygame.font.Font.render(tutorial_font,tutorial_texts[4],True,(255,255,255)),(width*0.1,height*0.3))
        elif tutorial_step == 6:
            music_stop()
            SCREEN.fill((0,0,0))
            SCREEN.blit(pygame.font.Font.render(tutorial_font,tutorial_texts[5],True,(250,180,180)),((width*0.1,height*0.3)))
        
            SCREEN.blit(sfx_img,(width//2-sfx_img.get_width()*1.2,height-sfx_img.get_height()*1.2))
            SCREEN.blit(sfx_img,(width//2+sfx_img.get_width()*0.2,height-sfx_img.get_height()*1.2))
        elif tutorial_step == 7:
            music_stop()
            SCREEN.fill((0,0,0))
            SCREEN.blit(pygame.font.Font.render(tutorial_font,tutorial_texts[6],True,(250,180,180)),(width*0.1,height*0.3))

            SCREEN.blit(sfx_img,(width//2-sfx_img.get_width()//2,height-sfx_img.get_height()*1.2))
        elif tutorial_step == 8:
            music_stop()
            SCREEN.fill((0,0,0))
            SCREEN.blit(pygame.font.Font.render(tutorial_font,tutorial_texts[7],True,(250,180,180)),(width*0.1,height*0.3))
        

# Menu Logic

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                running = False
                game_on = False
            if settings:
                reset_progress, al_counter_on, show_timer_on = settings_logic(mouse_pos, event)
                if reset_progress:
                    menu = False
                    running = False
                    game_on = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(mouse_pos):
                    sfx.play("click")
                    play, custom_night, extra, settings = True, False, False, False
                elif custom_rect.collidepoint(mouse_pos) and extras_unlocked == "True":
                    sfx.play("click")
                    play, custom_night, extra, settings = False, True, False, False
                elif extra_rect.collidepoint(mouse_pos) and extras_unlocked == "True":
                    sfx.play("click")
                    play, custom_night, extra, settings = False, False, True, False
                elif settings_rect.collidepoint(mouse_pos):
                    sfx.play("click")
                    play, custom_night, extra, settings = False, False, False, True

                if tutorial_step > 0:
                    if not running_left_audio_sfx_rect.collidepoint(mouse_pos) and not running_right_audio_sfx_rect.collidepoint(mouse_pos) and not close_steps_audio_sfx_rect.collidepoint(mouse_pos):
                        tutorial_step += 1
                        if 9> tutorial_step >= 6 and deaf_unlocked == "True":
                            sfx.play("secret_text")
                    if tutorial_step == 6:
                        rnd = random.randint(1,2)
                        if running_left_audio_sfx_rect.collidepoint(mouse_pos):
                            if rnd == 1:
                                sfx.play("fast_run_left")
                            else:
                                sfx.play("deep_footsteps_left")
                        elif running_right_audio_sfx_rect.collidepoint(mouse_pos):
                            if rnd == 1:
                                sfx.play("fast_run_right")
                            else:
                                sfx.play("deep_footsteps_right")
                    if tutorial_step == 7:
                        rnd = random.randint(1,3)
                        if close_steps_audio_sfx_rect.collidepoint(mouse_pos):
                            if rnd == 1:
                                sfx.play("small_footsteps")
                            else:
                                sfx.play(f"small_footsteps{rnd}")


                elif extra:
                    if nightmare_text_rect.collidepoint(mouse_pos):
                        sfx.play("click")
                        nightmare = not nightmare
                        radar = False
                        if nightmare:
                            enemies["The_guy"]["AI"] = 100
                            enemies["Face"]["AI"] = 100
                            enemies["girl"]["AI"] = 100
                    if radar_text_rect.collidepoint(mouse_pos):
                        sfx.play("click")
                        radar = not radar
                    if dark_mode_text_rect.collidepoint(mouse_pos):
                        sfx.play("click")
                        dark_mode = not dark_mode
                    if inverted_controls_text_rect.collidepoint(mouse_pos):
                        sfx.play("click")
                        inverted_controls = not inverted_controls
                    if short_night_text_rect.collidepoint(mouse_pos):
                        sfx.play("click")
                        short_night = not short_night
                    if battery_text_rect.collidepoint(mouse_pos):
                        sfx.play("click")
                        battery = not battery
                elif play:
                    if start_btn.collidepoint(mouse_pos) and not nightmare and not radar and not dark_mode:
                        menu = False
                        running = True
                        game_on = True
                    if tutorial_btn_rect.collidepoint(mouse_pos):
                        tutorial_step = 1
                elif custom_night:
                    if not nightmare:
                        if the_guy_arrow_up_rect.collidepoint(mouse_pos):
                            sfx.play("click")
                            enemies["The_guy"]["AI"] += 5
                            if enemies["The_guy"]["AI"] > 100:
                                enemies["The_guy"]["AI"] = 100
                        elif the_guy_arrow_down_rect.collidepoint(mouse_pos):
                            sfx.play("click")
                            enemies["The_guy"]["AI"] -= 5
                            if enemies["The_guy"]["AI"] < 0:
                                enemies["The_guy"]["AI"] = 0
                        elif face_arrow_up_rect.collidepoint(mouse_pos):
                            sfx.play("click")
                            enemies["Face"]["AI"] += 5
                            if enemies["Face"]["AI"] > 100:
                                enemies["Face"]["AI"] = 100
                        elif face_arrow_down_rect.collidepoint(mouse_pos):
                            sfx.play("click")
                            enemies["Face"]["AI"] -= 5
                            if enemies["Face"]["AI"] < 0:
                                enemies["Face"]["AI"] = 0
                        elif girl_arrow_up_rect.collidepoint(mouse_pos):
                            sfx.play("click")
                            enemies["girl"]["AI"] += 5
                            if enemies["girl"]["AI"] > 100:
                                enemies["girl"]["AI"] = 100
                        elif girl_arrow_down_rect.collidepoint(mouse_pos):
                            sfx.play("click")
                            enemies["girl"]["AI"] -= 5
                            if enemies["girl"]["AI"] < 0:
                                enemies["girl"]["AI"] = 0
                        elif reset_text_rect.collidepoint(mouse_pos):
                            sfx.play("click")
                            enemies["The_guy"]["AI"] = 0
                            enemies["Face"]["AI"] = 0
                            enemies["girl"]["AI"] = 0
                    if start_btn.collidepoint(mouse_pos):
                        menu = False
                        running = True
                        game_on = True


                if (tutorial_step > 5 and deaf_unlocked == "False") or tutorial_step > 8:
                    tutorial_step = 0
                    menu_music_active = False
            

        pygame.display.update()
        dt = clock.tick(30) 
        if dt > 100:
            print("Lag spike:", dt, "ms")


    if enemies["The_guy"]["AI"] == 0:
        enemies["The_guy"]["room"] = None

    if enemies["The_guy"]["AI"] == 20 and enemies["Face"]["AI"] == 15 and enemies["girl"]["AI"] == 0:
        nightmare = False
        radar = False
        dark_mode = False
        battery = False
        CamPlan = pygame.image.load("assets/IMAGE/plan of the hotel/CamerasLocust.png").convert_alpha()
        CamPlan = pygame.transform.scale(CamPlan, (width*0.76,height)).convert_alpha()
        hour = 2
        the_guy_move_timer = -300
        enemies["The_guy"]["room"] = None
        enemies["The_guy"]["AI"] = 0
        enemies["Face"]["AI"] = 0
        enemies["girl"]["AI"] = 0
        enemies["locust"]["AI"] = 1
        
    
    display_night = ""
    if night in (1,2,3,4,5) and play:
        display_night = f"NIGHT {night}"
    elif extras_unlocked == "True" and not nightmare and enemies["locust"]["AI"] == 0:
        display_night = "CUSTOM NIGHT"
    elif nightmare:
        display_night = "NIGHT 6"
    elif enemies["locust"]["AI"] == 1:
        display_night = "########"
    else:
        display_night = "?"
    music_stop()
    if running:
        for i in range(1,300):
            if i == 1:
                play_music("night_start")
            SCREEN.fill((0,0,0))
            night_text_game_start = pygame.font.Font.render(font, display_night, True, (255,255,255) if not enemies["locust"]["AI"] == 1 else (210,20,20))
            SCREEN.blit(night_text_game_start, (width//2 - night_text_game_start.get_width()//2,height//2-night_text_game_start.get_height()//2))
            pygame.display.update()
            clock.tick(60)
    
    if play and extras_unlocked == "True":
        enemies["girl"]["AI"] = 70
        enemies["Face"]["AI"] = 80
        enemies["The_guy"]["AI"] = 70
    the_guy_AI_value = enemies["The_guy"]["AI"]
    face_AI_value = enemies["Face"]["AI"]
    girl_AI_value = enemies["girl"]["AI"]

    print(the_guy_AI_value,face_AI_value,girl_AI_value)
    
    #Game loop

    music_stop()
    if game_on:
        play_music("game")  
    last_hour_time = 0

    while running:

        flashlight_toogle = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_on = False
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_s and not animating and not inverted_controls) or (event.key == pygame.K_w and not animating):
                    sfx.play("camera_pull_up")
                    animating = True
                    anim_frame = 0
                    anim_timer = 0
                    turning_on = not CamON

    # Scan button & Audio Lure button

            if event.type == pygame.MOUSEBUTTONDOWN and CamON:
                mouse_pos = pygame.mouse.get_pos()
                if enemies["locust"]["AI"] == 0:
                    if audio_lure_button_rect.collidepoint(mouse_pos) and AudioLureTimer == 0 and SelectedCam not in ("", None):
                        AudioLureTimer = 240
                        sfx.play("audio_lure")
                        roomToMove = The_guy.AudioLure(enemies["The_guy"]['room'], enemies["The_guy"]['AI'], SelectedCam, LockedDoor, nightmare)
                        enemies["The_guy"]["room"] = roomToMove
                    if width*0.18 <= mouse_pos[0] <= width*0.27 and height*0.41 <= mouse_pos[1] <= height*0.49 and not radar:
                        if ScanTimer == 0:
                            sfx.play("scan")
                            ScanDuration = ScanDurationMax
                            ScanTimer = 900
                        else:
                            sfx.play("error")

                    if AudioLureTimer == 0:
                        SelectedCam = camera_manager(width, height, room_positions, mouse_pos, SelectedCam)
                # Door locking
                    if DoorTimer == 0:
                        LockedDoor, DoorTimer = door_manager(door_positions, mouse_pos, LockedDoor, DoorTimer)

                else:
                    if audio_lure_button_rect.collidepoint(mouse_pos):
                        sfx.play("audio_lure")
                        if enemies["locust"]["room"] in ("LH","LoH"):
                            enemies["locust"]["room"] = "DB"
                            locust.attack = 0
                            the_guy_move_timer = 0
                        else:
                            Jumpscare = True
                    if width*0.18 <= mouse_pos[0] <= width*0.27 and height*0.41 <= mouse_pos[1] <= height*0.49:
                        sfx.play("error")  
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if enemies["girl"]["pos"] != 0:
                    if girl_rect.collidepoint(event.pos):
                        enemies["girl"]["room"] = "C"
                        girl_disappearing = True
                        girl_disappear_timer = 30
                        sfx.play("girl_vanish")
    # Event end

        if girl_disappearing:
            girl_disappear_timer -= 1
            if girl_disappear_timer <= 0:
                girl_disappearing = False
                enemies["girl"]["pos"] = 0

        if enemies["locust"]["AI"] == 0:
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
                         
        key = pygame.key.get_pressed()

    # Flashlight
        if ((key[pygame.K_q] and not CamON and not inverted_controls) or (key[pygame.K_e] and not CamON)) and battery_amount > 0:
            flashlight_toogle = True
            if battery:
                battery_amount -= 0.051 if not dark_mode else 0.015
            

    # Enemy movement
        if enemies["locust"]["AI"] == 0:
            the_guy_move_timer += 1
            if the_guy_move_timer >= 300:
                the_guy_move_timer = 0
                current_room = enemies["The_guy"]["room"]
                new_room = The_guy.move(current_room, the_guy_AI_value, LockedDoor, nightmare)
                enemies["The_guy"]["room"] = new_room
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
        else:
            the_guy_move_timer += 1
            if hour < 6 :
                if the_guy_move_timer >= 130  :
                    the_guy_move_timer = 0
                    enemies["locust"]["room"] = locust.move(enemies["locust"]["room"],CamON)
                    if locust.attack >= 3:
                        Jumpscare = True
            elif the_guy_move_timer >= 80:
                the_guy_move_timer = 0
                enemies["locust"]["room"] = locust.move(enemies["locust"]["room"],CamON)
                if locust.attack >= 3:
                    Jumpscare = True


    # Time and hour system

        current_time = timer
        if (current_time - last_hour_time) // 60 >= 40:
            hour += 1
            last_hour_time = timer
        if hour in (0,1,2):
            display_time = f"{10+hour}:00 PM"
        else:
            display_time = f"{hour-2}:00 AM"
        if hour >= 8:
            win = True
            running = False
            hour = 0
        if hour == 7 and (current_time - last_hour_time) // 60 == 32 and last7one == 0:
            last7one += 1
            sfx.play("last_7_sec")
            
    # Camera movement
        if not CamON and not animating:
            if inverted_controls:
                if key[pygame.K_d]:
                    CamX += cameraMove
                    if CamX > 0:
                        CamX = 0
                    if CamX < -500:
                        CamX = -500
                if key[pygame.K_a]:
                    CamX -= cameraMove
                    if CamX < -500:
                        CamX = -500
                    if CamX > 0:
                        CamX = 0
            else:
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
                if enemies["locust"]["room"] == "breath" and enemies["locust"]["AI"] == 1:
                    enemies["locust"]["room"] = "DB"
                    locust.attack = 0
                    the_guy_move_timer = 0
                if enemies["locust"]["room"] in("doorL","doorR"):
                    Jumpscare = True
            else:
                SCREEN.blit(room_img, (CamX, 0))
                SCREEN.blit(monitor_imgs[4 - anim_frame], (-40, 0))
                if enemies["locust"]["room"] == "camera_static" and enemies["locust"]["AI"] == 1:
                    enemies["locust"]["room"] = "DB"
                    locust.attack = 0
                    the_guy_move_timer = 0
        elif CamON:             
#Camera screen render
            SCREEN.blit(CamBackground[CamBackground_frame], (0, 0))
            CamBackground_frame = (CamBackground_frame + 1) % len(CamBackground)
            if LockedDoor in door_positions:
                pos = door_positions[LockedDoor]
                pygame.draw.rect(SCREEN, (255,255,255), (pos[0],pos[1],width*0.03,height*0.016))
            SCREEN.blit(CamPlan, (width*0.12, height*0.05))
            if SelectedCam in room_positions:
                pos = (room_positions[SelectedCam][0]-width*0.022,room_positions[SelectedCam][1]-height*0.0269)
                if AudioLureTimer > 0 and AudioLureTimer % 10 < 5:
                    SCREEN.blit(AudioLure_img, pos)
                pos = room_positions[SelectedCam]
                pygame.draw.circle(SCREEN,(100,100,100), pos, width*0.005)
            if ScanTimer > 900:
                SCREEN.blit(block_img,(width*0.18,height*0.415))

            for i in range(6):
                if ScanTimer > (i * 150):
                    color = (100, 100, 100)
                else:
                    color = (255, 255, 255)
                pygame.draw.rect(SCREEN, color, (width * 0.175 + i*width*0.019, height * 0.51,width*0.01,width*0.01))


            TIME = pygame.font.Font.render(timer_font, display_time, True, (255, 255, 255))
            SCREEN.blit(TIME, (width*0.05, height*0.06))
            if show_timer_on:

                total_seconds = timer / 60
                minutes = int(total_seconds // 60)
                seconds = int(total_seconds % 60)
                milliseconds = int((total_seconds % 1) * 100)

                mini_timer = timer_font_small.render(f"{minutes:01d}:{seconds:02d}:{milliseconds:02d}", True, (255, 255, 255))
                SCREEN.blit(mini_timer,(width*0.05, height*0.11))

            if al_counter_on:
                al_count_text = pygame.font.Font.render(timer_font_small, f"{max(100 - (enemies['The_guy']["AI"]/5 * The_guy.ALUsed),0)}%", True, (180,180,180))
                SCREEN.blit(al_count_text,(width*0.05, height*(0.14 if show_timer_on else 0.11)))
            if enemies["locust"]["room"] == "camera_static" and enemies["locust"]["AI"] == 1:
                SCREEN.blit(locust_camera,(410,-10))
            pygame.display.update()
#Room screen render
        else:                   
            SCREEN.blit(room_img, (CamX, 0))

            if enemies["Face"]["alpha"] < 30:
                face_offset = random.randint(width//-4,width//4)
            if enemies["Face"]["alpha"] > 30:
                face_room_img.set_alpha(enemies["Face"]["alpha"])
                SCREEN.blit(face_room_img,(CamX+width//2+face_offset,height*0.2))
            if enemies["girl"]["pos"] != 0:
                if enemies["girl"]["pos"] % 2 == 0:
                    girl_rect = girl_room_left.get_rect(topleft=(CamX,enemies["girl"]["pos"]*2))        
                    if girl_disappearing:
                        if girl_disappear_timer % 4 < 2:
                            SCREEN.blit(girl_room_left, girl_rect)
                    else:
                        SCREEN.blit(girl_room_left,girl_rect)                
                else:
                    girl_rect = girl_room_right.get_rect(topleft=(CamX+width*1.26 - girl_room_right.get_width(),enemies["girl"]["pos"]*2))
                    if girl_disappearing:
                        if girl_disappear_timer % 6 < 3:
                            SCREEN.blit(girl_room_right, girl_rect)
                    else:
                        SCREEN.blit(girl_room_right,girl_rect)
            if battery:
                battery_stage = 0 if battery_amount <= 0 else min(math.floor(battery_amount / 20) + 1, 5)
                SCREEN.blit(battery_img[battery_stage],(width - battery_img[battery_stage].get_width()*1.2, height - battery_img[battery_stage].get_height()*1.1))
                
            if flashlight_toogle:
                SCREEN.blit(flashlight_img,(width//2-flashlight_img.get_width()//2,height//2-flashlight_img.get_height()//2))
            if enemies["Face"]["alpha"] >= 255:
                Jumpscare = True
            if enemies["locust"]["room"] == "breath" and enemies["locust"]["AI"] == 1:
                SCREEN.blit(room_locust,(890+CamX,120))


        sfx.flashlight(flashlight_toogle)

        pygame.display.update()

        if flashlight_toogle and enemies["locust"]["AI"] == 1:
            if enemies["locust"]["room"] == "breath":
                Jumpscare = True
            elif enemies["locust"]["room"] == "doorL" and CamX > -200:
                enemies["locust"]["room"] = "DB"
                locust.attack = 0
                the_guy_move_timer = 0
            elif enemies["locust"]["room"] == "doorR" and CamX < -300:
                enemies["locust"]["room"] = "DB"
                locust.attack = 0
                the_guy_move_timer = 0     

    # Jumpscare

        if Jumpscare and not animating:
            SCREEN.blit(accurate_room_img, (CamX, 0))
            if enemies["Face"]["alpha"] >= 255:
                SCREEN.blit(pygame.transform.scale(pygame.image.load("assets/IMAGE/RoomDark.png"),(width*1.26,height)),(CamX,0))
                SCREEN.blit(face_jumpscare,(300,0))
            elif enemies["locust"]["AI"] == 1:
                SCREEN.blit((locust_camera),(410,-10))
            else:
                SCREEN.blit(The_guy_jumpscare, (0, 0))
            Jumpscare = False
            sfx.stop()
            music_stop()
            sfx.play("jumpscare")
            pygame.display.update()
            pygame.time.wait(1100)
            sfx.stop()
            music_stop()
            SCREEN.blit(Blood, (0, 0))
            pygame.display.update()
            pygame.time.wait(3800)
            win = False
            running = False
            menu = True

        if not short_night:
            dt = clock.tick(60) 
        else:
            dt = clock.tick(120) 
        if dt > 100:
            print("Lag spike:", dt, "ms")

        # SFX
        sfx.random_ambience_sfx(CamON)
        timer += 1
        ScanTimer -= 1
        AudioLureTimer -=1
        DoorTimer -=1
        if AudioLureTimer < 0:
            AudioLureTimer = 0
        if ScanTimer < 0:
            ScanTimer = 0
        if DoorTimer < 0:
            DoorTimer = 0
    #Face
        if not flashlight_toogle:
            enemies["Face"]["alpha"] += enemies["Face"]["AI"]/250
            if nightmare and enemies["Face"]["alpha"] < 20:
                enemies["Face"]["alpha"] = 20
        else:
            enemies["Face"]["alpha"] -= 0.85 if dark_mode else 4
        if enemies["Face"]["alpha"] < 0:
            enemies["Face"]["alpha"] = 0
    #Girl
        girl_kill_timer -= 1
        if girl_kill_timer < 0:
            girl_kill_timer = 0
        if enemies["girl"]["room"] == "C" and timer % 12 == 0 and CamON and ScanTimer <= 800:
            enemies["girl"]["room"], enemies["girl"]["pos"] = girl.girl_try_movement(girl_AI_value,height)
            if enemies["girl"]["room"] == "You":
                girl_kill_timer = 150 if not nightmare else 120
        elif enemies["girl"]["room"] == "You" and timer % 30 == 0 and girl_kill_timer == 0:
            ScanTimer, power_down = girl.girl_try_sabotage(girl_AI_value, nightmare, ScanTimer)
            if ScanTimer > 900:
                enemies["girl"]["room"] = "C"
                enemies["girl"]["pos"] = 0
            if power_down:
                LockedDoor = None
                DoorTimer = 60
                sfx.play("metal_door_close")
                the_guy_move_timer = 0

        
    if win:
        SCREEN.blit(Win_img, (0, 0))
        music_stop()
        sfx.stop()
        music_stop()
        win = False
        play_music("win")
        pygame.display.update()
        pygame.time.wait(7000)
        with open("lib/text/progres/game.txt", "w") as progress:
            if night != 5:
                progress.write(f"Night\n{night+1}\n")
            else:
                progress.write(f"Night\n{night}\n")
            if night == 5 and extras_unlocked == "False":
                progress.write("Extras\nTrue\n")
            else:
                progress.write(f"Extras\n{extras_unlocked}\n")
            if extras_unlocked == "True" and nightmare == True and nightmare_beaten == "False":
                progress.write("Nightmare\nTrue\n")
            else:
                progress.write(f"Nightmare\n{nightmare_beaten}\n")
            if enemies["locust"]["AI"] == 1:
                progress.write(f"deaf_mode_beaten:\nTrue\n")
            else:
                progress.write(f"deaf_mode_beaten:\n{deaf_mode_beaten}\n")
            progress.write(f"2015_unlocked\n{deaf_unlocked}")
        if night == 2:
            minigame(1)
        elif night == 4:
            minigame(2)
        elif night == 5 and play:
            minigame(3)
        elif nightmare:
            minigame(4)
    elif not reset_progress:
        with open("lib/text/progres/game.txt", "w") as progress:
            progress.write(f"Night\n{night}\n")
            progress.write(f"Extras\n{extras_unlocked}\n")
            progress.write(f"Nightmare\n{nightmare_beaten}\n")
            progress.write(f"deaf_mode_beaten:\n{deaf_mode_beaten}\n")
            if enemies["locust"]["AI"] == 1 or deaf_unlocked == "True":
                progress.write(f"deaf_unlocked:\nTrue")
                if enemies["locust"]["AI"] == 1:
                    the_guy_AI_value = 20
                    face_AI_value = 15
                    girl_AI_value = 0
            else:
                progress.write(f"deaf_unlocked:\nFalse")
        
        menu = True
    
    if game_on:
        SCREEN.fill((0,0,0))
        pygame.display.update()
        running = True
print(reset_progress)
if not reset_progress:
    settings_data_save()
pygame.quit()