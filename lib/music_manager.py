import random, pygame
music_volume = 1.0
menu_music = pygame.mixer.Sound("assets/MUSIC/menu1.mp3")
music_channel = pygame.mixer.Channel(1)
music_active = False
night_start_music = pygame.mixer.Sound("assets/SOUND/next_night.mp3")
game_music = pygame.mixer.Sound("assets/MUSIC/Game1.mp3")
win_sfx = pygame.mixer.Sound("assets/SOUND/6AM.mp3")

def play_music(name):
    global menu_music, music_channel, music_active, night_start_music, win_sfx
    if name == "menu" and not music_active:
        music_channel.play(menu_music,-1)
        music_active = True
    if name == "night_start":
        music_channel.play(night_start_music)
    elif name == "game" and not music_active:
        music_channel.play(game_music,-1)
        music_active = True
    elif name == "win":
        music_channel.play(win_sfx)

def music_stop():
    global music_channel, music_active
    music_channel.stop()
    music_active = False

def volume_update():
    global music_channel, music_volume
    music_channel.set_volume(music_volume)