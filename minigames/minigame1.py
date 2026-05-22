import pygame

pygame.init()
pygame.mixer.init()


def minigame(nr):
    map_grid = {
        "X" : [],
        "Y" : []
    }
    for i in range (10):
        map_grid["X"].append(192*i)
    for i in range (6):
        map_grid["Y"].append(192*i)
    print(map_grid)

    sprites = {
        "player" :[pygame.image.load("minigames/img/player1.png"),pygame.image.load("minigames/img/player2.png")],
        "hunter": [pygame.image.load("minigames/img/hunter1.png"),pygame.image.load("minigames/img/hunter2.png")],
        "locust" : pygame.transform.scale(pygame.image.load("minigames/img/Locust.png"),(192,192)),
        "dead"  : pygame.image.load("minigames/img/player_dead.png"),
        "overlay" : pygame.image.load("minigames/img/overlay.png"),
        "message" : pygame.transform.scale(pygame.image.load("minigames/img/text_box.png"),(350,100)),
        "map" :
            {"road" : pygame.transform.scale(pygame.image.load("minigames/img/road.png"),(192,384)),
             "grass": pygame.transform.scale(pygame.image.load("minigames/img/grass.png"),(192,192)),
             "tree" : pygame.transform.scale(pygame.image.load("minigames/img/tree.png"),(192,192)),
             "blank": pygame.transform.scale(pygame.image.load("minigames/img/blank.png"),(192,192)),
             "side_walk": {"dark" : pygame.transform.scale(pygame.image.load("minigames/img/side_walk.png"),(192,192)),
                           "Up" : pygame.transform.scale(pygame.image.load("minigames/img/side_walkU.png"),(192,192)),
                           "Down": pygame.transform.scale(pygame.image.load("minigames/img/side_walkD.png"),(192,192)),
                           "LeftUp": pygame.transform.scale(pygame.image.load("minigames/img/side_walkLU.png"),(192,192)),
                           "RightUp": pygame.transform.scale(pygame.image.load("minigames/img/side_walkRU.png"),(192,192)),
                           "RightDown": pygame.transform.scale(pygame.image.load("minigames/img/side_walkRD.png"),(192,192)),
                           "LeftDown": pygame.transform.scale(pygame.image.load("minigames/img/side_walkLD.png"),(192,192))},
             "car" : pygame.transform.scale(pygame.image.load("minigames/img/car.png"),(576,192)),
              
        }
    }
    tree_hitbox = []
    sfx = {
        "ambience" : pygame.mixer.Sound("minigames/sfx/Ambience.ogg"),
        "step" : pygame.mixer.Sound("minigames/sfx/Step.ogg"),
    }

    # Glitch SFX - sterowanie głośnością zależnie od tego jak gracz "podchodzi" do góry.
    glitch_sound = pygame.mixer.Sound("minigames/sfx/glitch.mp3")
    glitch_sound.set_volume(0.0)
    glitch_channel = glitch_sound.play(loops=-1)
    glitch_playing = True
    if nr == 1:
        minigame_screens = {
            "screen1" : "t"*3+"g"*7 +"t"+ "g"*9+ "g"*2+"LUUR"+"g"*4 +"s"+"r"*9 + "s"+"b"*9  + "g"*10,
            "screen2" : "g"*4 + "t"*6 +"g"*5+"t"*5+"g"*7+"t"*3+"r"*10 +"b"*10+"g"*8+"t"*2
        }
        text = "It's been nearly a month \nsince she's gone"
        player_pos = [600,450]
    elif nr == 2:
        minigame_screens = {
            "screen1" : "t"*3+"g"*7 +"t"+ "g"*9+ "g"*2+"LUUR"+"g"*4 +"s"+"r"*9 + "s"+"b"*9  + "g"*10,
            "screen2" : "g"*4 + "t"*6 +"g"*5+"t"*5+"g"*7+"t"*3+"r"*10 +"b"*10+"g"*8+"t"*2,
            "screen3" : "t"*5 + "ggttt" + "t"*5 + "ggttt" + "t"*4 +"gggttt" + "r"*8 + "st" + "b"*8 + "st" + "t"*10,
            "screen4" : "t"*5+ "ggttt"+"t"*5+ "gtttt"+"t"*5+ "gtttt" +"t"*5+ "gtttt" + "t"*5+ "ggttt" + "t"*5 +"ggttt",
            "screen5" : "t"*14 + "gg" + "t"*7 + "g#gg" + "t"*6 + "g"*4 + "t"*7 + "g"*3 + "t"*8 + "gg" + "t"*8 + "gg" + "t"*3
        }
        player_pos = [700,450]
        
    car_stage = 0
    clock = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    player_sprite = 0
    timer = 0
    hunter_sprite = 0
    text_stage = 0
    
    text_display = ""
    font = pygame.font.SysFont("font/raster-forge-font/RasterForgeRegular-JpBgm.ttf", 40)
    is_moving = False
    player_speed = 40
    
    player_facing = ["D","W"]
    minigame_on = True
    minigame_screen = 1
    block = False
    dx = 0
    dy = 0
    sfx["ambience"].play(-1)

    while minigame_on:
        tree_hitbox.clear()
        x = 0
        y = 0
        if block and car_stage < 4 and nr == 1:
            car_stage +=1

        for i in range(len(map_grid["Y"])):
            for j in range(len(map_grid["X"])):
                i = 5-i
                j = 9-j
                x = map_grid["X"][j]
                y = map_grid["Y"][i]
                if minigame_screens[f"screen{minigame_screen}"][i*10+j] == "t":
                    tree_hitbox.append(sprites["map"]["tree"].get_rect(topleft=(x,y)))
                    
        if minigame_screen == 2 and nr == 1:
            tree_hitbox.append(sprites["hunter"][hunter_sprite].get_rect(topleft=(500,350)))
        dx = 0
        dy = 0
        is_moving = False
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                minigame_on = False
        if not block:
            if key[pygame.K_a]:
                dx = -player_speed
                is_moving = True
                if player_facing[0] == "D":
                    sprites["player"][0] = pygame.transform.flip(sprites["player"][0],True,False)
                    sprites["player"][1] = pygame.transform.flip(sprites["player"][1],True,False)
                    player_facing[0] = "A"
            if key[pygame.K_d]:
                dx = player_speed
                is_moving = True
                if player_facing[0] == "A":
                    sprites["player"][0] = pygame.transform.flip(sprites["player"][0],True,False)
                    sprites["player"][1] = pygame.transform.flip(sprites["player"][1],True,False)
                    player_facing[0] = "D"
            if key[pygame.K_w]:
                dy = -player_speed
                is_moving = True
                player_facing[1] = "W"
            if key[pygame.K_s]:
                dy = player_speed
                is_moving = True
                player_facing[1] = "S"

        #collision

        new_x = player_pos[0] + dx
        x_hitbox = sprites["player"][0].get_rect(topleft=[new_x, player_pos[1]])
        for tree in tree_hitbox:
            if x_hitbox.colliderect(tree):
                if dx > 0:
                    new_x = tree.left - x_hitbox.width
                else:
                    new_x = tree.right
                break
        new_y = player_pos[1] + dy
        y_hitbox = sprites["player"][0].get_rect(topleft=[new_x, new_y])
        for tree in tree_hitbox:
            if y_hitbox.colliderect(tree):
                if dy > 0:
                    new_y = tree.top - y_hitbox.height
                else:
                    new_y = tree.bottom
                break
        player_pos[0] = new_x
        player_pos[1] = new_y
        if minigame_screen == 1:
            if player_pos[0] < 0: player_pos[0] = 0
            if player_pos[0] > 1800:
                minigame_screen = 2
                player_pos[0] = 100
            player_pos[1] = max(0, min(960, player_pos[1]))
        elif minigame_screen == 2: 
            if player_pos[0] < 0:
                minigame_screen = 1
                player_pos[0] = 1800
            if player_pos[0] > 1800 and nr != 2: 
                player_pos[0] = 1800
            elif nr == 2 and player_pos[0] > 1800:
                minigame_screen = 3
                player_pos[0] = 100
            player_pos[1] = max(0, min(960, player_pos[1]))
        elif minigame_screen == 3: 
            if player_pos[0] < 0:
                minigame_screen = 2
                player_pos[0] = 1800
            if player_pos[0] > 1800: 
                player_pos[0] = 1800
            if player_pos[1] < 0:
                minigame_screen = 4
                player_pos[1] = 960
        elif minigame_screen == 4: 
            if player_pos[0] < 0:
                player_pos[0] = 0
            if player_pos[0] > 1800: 
                player_pos[0] = 1800
            if player_pos[1] > 960:
                minigame_screen = 3
                player_pos[1] = 30
            if player_pos[1] < 0:
                minigame_screen = 5
                player_pos[1] = 960
        elif minigame_screen == 5:
            if player_pos[0] < 0:
                player_pos[0] = 0
            if player_pos[0] > 1800: 
                player_pos[0] = 1800
            if player_pos[1] > 960:
                minigame_screen = 4
                player_pos[1] = 30
            if player_pos[1] < 900:
                player_speed = 20
            elif player_pos[1] < 800:
                player_speed = 10
            elif player_pos[1] < 650:
                player_speed = 5

            if glitch_playing and minigame_screen == 5:
                y = player_pos[1]
                t = (900 - y) / (900 - 500)
                t = max(0.0, min(1.0, t))

                glitch_sound.set_volume(t)
                if t >= 1.0:
                    minigame_on = False
            
        if is_moving:
            if timer % 2 == 0:  
                sfx["step"].play()
                player_sprite = 1 if player_sprite == 0 else 0
        if timer % 4 == 0:
            hunter_sprite = 1 if hunter_sprite == 0 else 0


        tile = minigame_screens[f"screen{minigame_screen}"]
        blits = {
            "g": sprites["map"]["grass"],
            "r": sprites["map"]["road"],
            "t": [sprites["map"]["grass"], sprites["map"]["tree"]],
            "b": sprites["map"]["blank"],
            "s": sprites["map"]["side_walk"]["dark"],
            "L": sprites["map"]["side_walk"]["LeftUp"],
            "l": sprites["map"]["side_walk"]["LeftDown"],
            "R": sprites["map"]["side_walk"]["RightUp"],
            "$": sprites["map"]["side_walk"]["RightDown"],
            "U": sprites["map"]["side_walk"]["Up"],
            "D": sprites["map"]["side_walk"]["Down"],
            "#": [sprites["map"]["grass"], sprites["locust"]]
        }
        for i in range(len(map_grid["Y"])):
            for j in range(len(map_grid["X"])):
                ii = 5 - i
                jj = 9 - j
                x = map_grid["X"][jj]
                y = map_grid["Y"][ii]
                type = tile[ii*10 + jj]
                layers = blits.get(type, None)
                if layers:
                    if isinstance(layers, list):
                        for layer in layers:
                            SCREEN.blit(layer, (x, y))
                    else:
                        SCREEN.blit(layers, (x, y))
                
        if minigame_screen == 2 and player_pos[0] > 1600 and nr == 1:
            block = True
        if minigame_screen == 2 and nr == 1:
            SCREEN.blit(sprites["hunter"][hunter_sprite],(500,350))
        
        

        if car_stage == 3:
            pygame.mixer.stop()
            pygame.mixer.Sound("minigames/sfx/car_crash.mp3").play()
            SCREEN.blit(sprites["dead"], player_pos)
        elif car_stage > 3:
            SCREEN.blit(sprites["dead"], player_pos)
            if timer%2 == 0:
                minigame_on = False
        else:
            SCREEN.blit(sprites["player"][player_sprite], player_pos)

        if car_stage > 0 :
            SCREEN.blit(sprites["map"]["car"],(2250 - car_stage*200,player_pos[1]))
        text_display = ""
        if nr == 1:
            for i in range(text_stage):
                text_display += text[i]
            if (abs(player_pos[0]+59-tree_hitbox[-1].centerx) < 220 and abs(player_pos[1]+59-tree_hitbox[-1].centery) < 220) and minigame_screen == 2:
                if text_stage == 0:
                    channel = pygame.mixer.Sound("minigames/sfx/message.mp3").play()
                if text_stage < len(text):
                    text_stage +=3
                    if text_stage > len(text):
                        text_stage = len(text)
                else:
                    channel.stop()
                SCREEN.blit(sprites["message"],(tree_hitbox[-1].left,tree_hitbox[-1].top-100))
                SCREEN.blit(pygame.font.Font.render(font,text_display,True,(0,0,0)),(tree_hitbox[-1].left+8, tree_hitbox[-1].top-100+8))
        SCREEN.blit(sprites["overlay"], (0, 0))
        pygame.display.update()
        if minigame_on == False:
            for i in range (500):
                SCREEN.fill((0,0,0))
                pygame.display.update()


        timer += 1
        dt = clock.tick(5)
    glitch_channel.stop()
    sfx["ambience"].stop()
    sfx["step"].stop()