import pygame
import heapq

pygame.init()
pygame.mixer.init()

locust_screen, locust_pos, locust_path, locust_path_index = None, None, None, None


def get_tile(screen, x, y, minigame_screens):
    if x < 0 or x >= 10 or y < 0 or y >= 6:
        return None

    return minigame_screens[f"screen{screen}"][y * 10 + x]


def is_walkable(screen, x, y, minigame_screens):
    tile = get_tile(screen, x, y, minigame_screens)
    if tile is None:
        return False
    return tile not in ("t", "T", "w", ".", "W", "P", "p")


def find_path(screen, start, target, minigame_screens):
    queue = []
    heapq.heappush(queue, (0, start))
    came_from = {}
    cost = {start: 0}

    while queue:
        _, current = heapq.heappop(queue)
        if current == target:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        x, y = current

        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx = x + dx
            ny = y + dy

            if not is_walkable(screen, nx, ny, minigame_screens):
                continue

            new_cost = cost[current] + 1
            neighbour = (nx, ny)

            if neighbour not in cost or new_cost < cost[neighbour]:
                cost[neighbour] = new_cost

                target_x, target_y = target
                priority = new_cost + abs(nx - target_x) + abs(ny - target_y)

                heapq.heappush(queue, (priority, neighbour))
                came_from[neighbour] = current

    return []

def locust_screen_transition():
    global locust_screen, locust_pos, locust_path, locust_path_index

    tile = (
        int((locust_pos[0] + 64) // 192),
        int((locust_pos[1] + 128) // 192)
    )

    if locust_screen == 5 and tile == (5, 1):
        locust_screen = 4
        locust_pos = [
            3 * 192 + 96 - 64,
            4 * 192 + 96 - 128
        ]

    elif locust_screen == 4 and tile in ((4, 0), (5, 0)):
        locust_screen = 3
        locust_pos = [
            tile[0] * 192 + 96 - 64,
            5 * 192 + 96 - 128
        ]

    elif locust_screen == 3 and tile[0] == 9 and tile[1] in (1, 2, 3, 4):
        locust_screen = 2
        locust_pos = [
            0 * 192 + 96 - 64,
            tile[1] * 192 + 96 - 128
        ]

    elif locust_screen == 2 and tile[0] == 9 and tile[1] in (3, 4):
        locust_screen = 1
        locust_pos = [
            0 * 192 + 96 - 64,
            tile[1] * 192 + 96 - 128
        ]



def minigame(nr):
    global locust_screen, locust_pos, locust_path, locust_path_index
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
        "door" : pygame.transform.scale(pygame.image.load("minigames/img/door_ending.png"),(600,600)),
        "player" :[pygame.image.load("minigames/img/player1.png"),pygame.image.load("minigames/img/player2.png")],
        "hunter": [pygame.image.load("minigames/img/hunter1.png"),pygame.image.load("minigames/img/hunter2.png")],
        "locust_front" : pygame.transform.scale(pygame.image.load("minigames/img/locust_front.png"),(192//1.5,384//1.5)),
        "locust_back" : pygame.transform.scale(pygame.image.load("minigames/img/locust_back.png"),(192//1.5,384//1.5)),
        "locust_right" : pygame.transform.scale(pygame.image.load("minigames/img/locust_right.png"),(192//1.5,384//1.5)),
        "locust_left" : pygame.transform.scale(pygame.image.load("minigames/img/locust_left.png"),(192//1.5,384//1.5)),
        "dead"  : pygame.image.load("minigames/img/player_dead.png"),
        "overlay" : pygame.image.load("minigames/img/overlay.png"),
        
        "message" : pygame.transform.scale(pygame.image.load("minigames/img/text_box.png"),(350,100)),
        "map" :
            {"road" : pygame.transform.scale(pygame.image.load("minigames/img/road.png"),(192,384)),
             "grass": pygame.transform.scale(pygame.image.load("minigames/img/grass.png"),(192,192)),
             "tree" : pygame.transform.scale(pygame.image.load("minigames/img/tree.png"),(192,192)),
             "blank": pygame.transform.scale(pygame.image.load("minigames/img/blank.png"),(192,192)),
             "wall_bottom" : pygame.image.load("minigames/img/wall_bottom.png"),
             "wall" : pygame.image.load("minigames/img/wall.png"),
             "door" : pygame.transform.scale(pygame.image.load("minigames/img/door.png"),(250,320)),
             "planks_bottom": pygame.image.load("minigames/img/planks_bottom.png"),
             "planks_right": pygame.image.load("minigames/img/planks_right.png"),
             "table" : pygame.image.load("minigames/img/table.png"),
             "puddle": pygame.image.load("minigames/img/puddle.png"),
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
        "house": pygame.mixer.Sound("minigames/sfx/house_ambience.mp3"),
        "house_chase": pygame.mixer.Sound("minigames/sfx/house_intense.mp3"),
        "ending" : pygame.mixer.Sound("minigames/sfx/ending_music.mp3").set_volume(0.75)
    }
    # Glitch SFX - sterowanie głośnością zależnie od tego jak gracz "podchodzi" do góry.
    glitch_sound = pygame.mixer.Sound("minigames/sfx/glitch.mp3")
    glitch_sound.set_volume(0.0)
    glitch_playing = False
    if nr == 2:
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
    elif nr==3:
        minigame_screens = {
            "screen1" : "wWWWWwwwww" + "wsssswwwww"+"WssssWWWWw"+"sssssOsssw"+"sssssssssw"+"wwwwPPwwww",
            "screen2" : "WWWWWWWWWw" + "sssssssOsw" + "sTsTsTsssW" + "ssssssssss" + "ssOsssssss" + "wwwwPPwwww",
            "screen3" : "wWWWWWWWWW" + "wsssssTsOs" + "wssTssssss" + "wsssssssss" + "wsssssssss" + "wwwwsswwww",
            "screen4" : "...wssw..." + "...wssp..." + "...wssw..." + "...wsOw..." + "...sssp..." + "...wwww...",
            "screen5" : ".WWWWW...." + ".wssss...." + ".wsssWWw.." + ".wsssOsw.." + ".wsOsssw.." + ".wwwwwww..",

        }
        player_pos = [700,600]
        
    car_stage = 0
    clock = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    player_sprite = 0
    timer = 0
    hunter_sprite = 0
    text_stage = 0
    
    text_display = ""
    font = pygame.font.SysFont("font/raster-forge-font/RasterForgeRegular-JpBgm.ttf", 40)
    font_big = pygame.font.Font("minigames/font/Roboto-Light.ttf", 60)
    is_moving = False
    player_speed = 40
    
    player_facing = ["D","W"]
    minigame_on = True
    minigame_screen = 1
    chase = False
    chase_start = False

    locust_screen = 5
    locust_pos = [250, 840]
    locust_speed = 40
    width, height = SCREEN.get_size()

    locust_direction = "front"
    locust_path = []
    locust_path_index = 0

    end_text = [
    "6:00 AM.\nYou made it! You really made it...\nAt least you made it trough the night.",
    "But there are some things off, aren't there?",
    "The hotel has been empty for years.\nNo guests. No staff. Nothing that should still be moving inside.",
    "Yet you remember waking up here.\nYou remember the rooms, the layout, the doors.\nBut you don't remember arriving.",
    "You remember a forest too.\nTrees. Rain. A road.\nThen headlights...",
    "There's so many things you don't understand\nAnd just because you fit in, doesn't mean you're in the right place.",
    "But you remember that girl.\nYou remember seeing her in the hotel.\nSometimes you're not sure if she was ever there.",
    "Maybe she was lost in the forest.\nMaybe she found the hotel, maybe she never left it.",
    "You keep trying to remember what happened.\nBut every time you get close,\nsomething else comes back instead.",
    "Maybe the hotel was real.\nOr maybe it was only a place your mind made for you.\nMaybe there isn't much difference anymore.",
    "But the difference yet remains.\nThe door should have never been opened."
]
    end_text_index = 0

    end_text_state = "fade_in"
    door = False
    door_timer = 0
    door_alpha = 0
    end_text_alpha = 255

    end_text_fade_speed = 6
    end_text_hold_timer = 120
    lines = end_text[end_text_index].split("\n")
    line_height = font_big.get_height()
    total_height = len(lines) * line_height
    start_y = height // 2 - total_height // 2

    screen_escape_tiles = {
        5 : (5,1),
        4 : (5,0),
        3 : (9,3),
        2 : (9,3)
    }

    block = False
    dx = 0
    dy = 0
    if nr in (1,2):
        sfx["ambience"].play(-1)
    elif nr == 3:
        sfx["house"].play(-1)
    elif nr == 4:
        sfx["ending"].play(-1)

    while minigame_on:
        tree_hitbox.clear()
        x = 0
        y = 0
        if block and car_stage < 4 and nr == 1:
            car_stage +=1
        if nr < 4:
            for i in range(len(map_grid["Y"])):
                for j in range(len(map_grid["X"])):
                    i = 5-i
                    j = 9-j
                    x = map_grid["X"][j]
                    y = map_grid["Y"][i]
                    if minigame_screens[f"screen{minigame_screen}"][i*10+j] in ("t","w",".","W","P","p","T") :
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
        if not block or nr < 4:
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
        if nr < 4:

            player_tile = (int((player_pos[0]+50) // 192), int((player_pos[1]+50) // 192))
            print("PLAYER:", player_tile, get_tile(minigame_screen, *player_tile, minigame_screens))

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
        if nr in (1,2):
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
        elif nr == 3:
            if minigame_screen == 1:
                if player_pos[0] < 0 and not chase:
                    minigame_screen = 2
                    player_pos[0] = 1800
                if player_pos[1] > 960:
                    player_pos[1] = 920
            if minigame_screen == 2:
                if player_pos[0] > 1800:
                    minigame_screen = 1
                    player_pos[0] = 0
                if player_pos[1] > 960:
                    player_pos[1] = 920
                if player_pos[0] < 0 and not chase:
                    minigame_screen = 3
                    player_pos[0] = 1800
            if minigame_screen == 3:
                if player_pos[0] > 1800:
                    minigame_screen = 2
                    player_pos[0] = 0
                if player_pos[1] > 960 and not chase:
                    minigame_screen = 4
                    player_pos[1] = 0
            if minigame_screen == 4:
                if player_pos[1] < 0:
                    minigame_screen = 3
                    player_pos[1] = 960
                if player_pos[0] < 600 and not chase:
                    minigame_screen = 5
                    player_pos[0] = 900
                    player_pos[1] = 220
            if minigame_screen == 5:
                if player_pos[0] < 830 and not chase:
                    chase_start = True
                if player_pos[0] > 950 and player_pos[1] < 300:
                    minigame_screen = 4
                    player_pos[0] = 600
                    player_pos[1] = 790


        

        
        if chase_start:
            chase = True
            chase_start = False
            pygame.mixer.stop()
            sfx["house_chase"].play(-1)
            locust_screen = 5
            locust_pos = [450, 650]
            locust_path = []
            locust_path_index = 0

    # Chase
        if chase:
            locust_screen_transition()
            locust_tile = (int((locust_pos[0] + 64) // 192), int((locust_pos[1] + 128) // 192))
            print("LOCUST:", locust_tile, get_tile(locust_screen, *locust_tile, minigame_screens), "LOCUST PATH:", locust_path)

        # Nowa ścieżka, kiedy Locust nie ma żadnej albo dotarł do końca poprzedniej
            if timer % 5 == 0 or not locust_path or locust_path_index >= len(locust_path):
                if locust_screen == minigame_screen:
                    locust_path = find_path(locust_screen, locust_tile, player_tile, minigame_screens)
                else:
                    locust_path = find_path(locust_screen, locust_tile, screen_escape_tiles[locust_screen], minigame_screens)
                if locust_path and locust_path[0] == locust_tile:
                    locust_path_index = 1
                else:
                    locust_path_index = 0

            if locust_path and locust_path_index < len(locust_path):
                target_tile = locust_path[locust_path_index]
                target_x = target_tile[0] * 192 + 96
                target_y = target_tile[1] * 192 + 96
                dx = target_x - (locust_pos[0] + 64)
                dy = target_y - (locust_pos[1] + 128)
                distance = (dx ** 2 + dy ** 2) ** 0.5

                if distance < locust_speed:
                    locust_path_index += 1

                else:
                    dx /= distance
                    dy /= distance
                    locust_pos[0] += dx * locust_speed
                    locust_pos[1] += dy * locust_speed

                    # Kierunek Locusta
                    if abs(dx) > abs(dy):
                        if dx > 0:
                            locust_direction = "right"
                        else:
                            locust_direction = "left"
                    else:
                        if dy > 0:
                            locust_direction = "front"
                        else:
                            locust_direction = "back"


            # Kolizja z graczem
            locust_rect = sprites[f"locust_{locust_direction}"].get_rect(
                topleft=locust_pos
            )
            player_rect = sprites["player"][player_sprite].get_rect(
                topleft=player_pos
            )
            if locust_rect.colliderect(player_rect):
                minigame_on = False
        if nr < 4:
            if glitch_playing and minigame_screen == 5 and nr == 2:
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
                "#": [sprites["map"]["grass"], sprites["locust_front"]],
                "w": sprites["map"]["wall"],
                "W": sprites["map"]["wall_bottom"],
                ".": None,
                "P": [sprites["map"]["side_walk"]["dark"], sprites["map"]["planks_bottom"]],
                "p": [sprites["map"]["side_walk"]["dark"], sprites["map"]["planks_right"]],
                "T": [sprites["map"]["side_walk"]["dark"], sprites["map"]["table"]],
                "O": [sprites["map"]["side_walk"]["dark"], sprites["map"]["puddle"]]
            }
        SCREEN.fill((0,0,0))
        if nr < 4:
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
        if minigame_screen == 1 and nr == 3:
            SCREEN.blit(sprites["map"]["door"], (1250,260))
        
        

        if car_stage == 3:
            pygame.mixer.stop()
            pygame.mixer.Sound("minigames/sfx/car_crash.mp3").play()
            SCREEN.blit(sprites["dead"], player_pos)
        elif car_stage > 3:
            SCREEN.blit(sprites["dead"], player_pos)
            if timer%2 == 0:
                minigame_on = False
        else:
            if chase and locust_screen == minigame_screen:
                SCREEN.blit(sprites[f"locust_{locust_direction}"], locust_pos)
            if nr < 4:
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
        if nr < 4:
            SCREEN.blit(sprites["overlay"], (0, 0))
        if timer % 5 in (0,3) and chase:
            SCREEN.fill((0,0,0))
        

        if nr == 4:
            if end_text_state == "fade_in":
                end_text_alpha -= end_text_fade_speed
                if end_text_alpha <= 0:
                    end_text_alpha = 0
                    end_text_state = "hold"

            elif end_text_state == "hold":
                end_text_hold_timer -= 1
                if end_text_hold_timer <= 0:
                    end_text_state = "fade_out"

            elif end_text_state == "fade_out":
                end_text_alpha += end_text_fade_speed
                if end_text_alpha >= 255:
                    end_text_alpha = 255
                    if end_text_index < len(end_text)-1:
                        end_text_index += 1
                        end_text_state = "fade_in"
                        end_text_hold_timer = 170
                        lines = end_text[end_text_index].split("\n")
                        line_height = font_big.get_height()
                        total_height = len(lines) * line_height
                        start_y = height // 2 - total_height // 2

                    if end_text_index == len(end_text) - 4 and not door:
                        door = True
                        door_timer = 1200
                    elif door_timer <= 0 and end_text_index >= len(end_text)-1:
                        minigame_on = False
                        
            

            if door:
                door_timer -= 1
                if door_timer >= 50:
                    door_alpha += 255/1150
                elif door_timer < 50:   
                    door_alpha -= 255/50
                sprites["door"].set_alpha(min(255,door_alpha))
                SCREEN.blit(sprites["door"],(width//2 - sprites["door"].get_width()//2,(height//2 - sprites["door"].get_height()//2)*0.75))

            for i, line in enumerate(lines):
                text_render = font_big.render(line, True, (255, 220, 220))
                text_render.set_alpha(255 - end_text_alpha)
                SCREEN.blit(text_render,(width // 2 - text_render.get_width() // 2, (start_y + i * line_height)*(1.25 if door else 1.0)))

        pygame.display.update()
        timer += 1
        if nr < 4:
            dt = clock.tick(5)
        else:
            dt = clock.tick(30)
        if minigame_on == False:
            for i in range (500):
                SCREEN.fill((0,0,0))
                pygame.display.update()
    if nr < 4:
        if nr == 2:
            glitch_channel.stop()
        if nr == 3:
            sfx["house_chase"].stop()
        sfx["ambience"].stop()
        sfx["step"].stop()
    else:
        sfx["ending"].stop()