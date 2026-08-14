import pygame
from lib import music_manager, sfx_manager

slider_x = 0
music_slider_y = 0
sfx_slider_y = 0
slider_width = 0
slider_height = 6
dragging_music = False
dragging_sfx = False
music_img = pygame.image.load("assets/IMAGE/music_icon.png")
sfx_img = pygame.image.load("assets/IMAGE/sfx_icon.png")
AL_count_on = False
show_timer_on = False
delete = False
al_count_rect = None
show_timer_rect = None
delete_rect = None
delete_progress_rect = None

def image_render(SCREEN, width, height):
    global music_img, sfx_img
    music_img = pygame.transform.scale(music_img, (height*0.1,height*0.1))
    sfx_img = pygame.transform.scale(sfx_img, (height*0.1,height*0.1))
def settings_data_render():
    global AL_count_on, show_timer_on
    try:
        with open("lib/text/progres/settings.txt", "r+") as settings:
            settings_data = settings.read().splitlines()
        try:
            music = float(settings_data[1])
            sfx = float(settings_data[3])
            AL_count_on = bool(int(settings_data[5]))
            show_timer_on = bool(int(settings_data[7]))
        except IndexError or ValueError:
            with open("lib/text/progres/settings.txt", "w+") as settings:
                settings.write("music_volume\n1.0\n")
                settings.write("sfx_volume\n1.0\n")
                settings.write("al_counter\n0\n")
                settings.write("show_timer:\n0\n")
                music = 1.0
                sfx = 1.0
                AL_count_on = False
                show_timer_on = False
        if 0 > music > 1.0 or 0 > sfx > 1.0 or AL_count_on not in (True,False) or show_timer_on not in (True,False):
            with open("lib/text/progres/settings.txt", "w+") as settings:
                settings.write("music_volume:\n1.0\n")
                settings.write("sfx_volume:\n1.0\n")
                settings.write("al_counter:\n0\n")
                settings.write("show_timer:\n0\n")
    except FileNotFoundError:
        with open("lib/text/progres/settings.txt", "w+") as settings:
            settings.write("music_volume\n1.0\n")
            settings.write("sfx_volume\1.0\n")
            settings.write("al_counter\n0\n")
            settings.write("show_timer:\n0\n")
    with open("lib/text/progres/settings.txt", "r+") as settings:
        settings_data = settings.read().splitlines()
    music_manager.music_volume = float(settings_data[1])
    sfx_manager.sfx_volume = float(settings_data[3])
    AL_count_on = bool(int(settings_data[5]))
    show_timer_on = bool(int(settings_data[7]))
    return AL_count_on, show_timer_on

def settings_data_save():
    global AL_count_on, show_timer_on
    with open("lib/text/progres/settings.txt", "w+") as settings:
                settings.write(f"music_volume\n{music_manager.music_volume}\n")
                settings.write(f"sfx_volume\n{sfx_manager.sfx_volume}\n")
                settings.write(f"al_counter\n{1 if AL_count_on else 0}\n")
                settings.write(f"show_timer:\n{1 if show_timer_on else 0}\n")
def settings_render(SCREEN, width, height, fancy_font):
    global slider_x, music_slider_y, sfx_slider_y, slider_width, music_img, sfx_img, AL_count_on, show_timer_on, delete, delete_rect, al_count_rect , show_timer_rect, delete_progress_rect
    print(show_timer_on, AL_count_on, music_manager.music_volume)
    slider_x = width * 0.4
    music_slider_y = height * 0.3
    sfx_slider_y = height * 0.45
    slider_width = width * 0.25
# music slider
    pygame.draw.rect(SCREEN,(100, 100, 100),(slider_x, music_slider_y, slider_width, slider_height))
    music_circle_x = slider_x + slider_width * music_manager.music_volume

    pygame.draw.circle(SCREEN, (255, 255, 255), (int(music_circle_x), music_slider_y + slider_height // 2), 15)
    SCREEN.blit(music_img, (slider_x - music_img.get_width()*1.2, music_slider_y + slider_height//2 - music_img.get_height()//2))
#sfx slider
    pygame.draw.rect(SCREEN,(100, 100, 100),(slider_x, sfx_slider_y, slider_width, slider_height))
    sfx_circle_x = slider_x + slider_width * sfx_manager.sfx_volume

    pygame.draw.circle(SCREEN, (255, 255, 255), (int(sfx_circle_x), sfx_slider_y + slider_height // 2), 15)
    SCREEN.blit(sfx_img, (slider_x - sfx_img.get_width()*1.2, sfx_slider_y + slider_height//2 - sfx_img.get_height()//2))

# AL count
    pygame.draw.rect(SCREEN, (255,255,255),(width//2.5 - 50,height*0.55,30,30), 0 if AL_count_on else 2)
    al_count_text = pygame.font.Font.render(fancy_font, "Show AL percentage", True, (255,255,255))
    al_count_rect = pygame.Rect(width//2.7,height*0.55 - al_count_text.get_height()//5,al_count_text.get_width()*1.1,al_count_text.get_height())
    SCREEN.blit(al_count_text, (width//2.5,height*0.55 - al_count_text.get_height()//5))

# Show in-game timer    
    pygame.draw.rect(SCREEN, (255,255,255),(width//2.5 - 50,height*0.65,30,30), 0 if show_timer_on else 2)
    show_timer_text = pygame.font.Font.render(fancy_font, "Show In game timer", True, (255,255,255))
    show_timer_rect = pygame.Rect(width//2.7,height*0.65 - show_timer_text.get_height()//5,show_timer_text.get_width()*1.1,show_timer_text.get_height())
    SCREEN.blit(show_timer_text, (width//2.5,height*0.65 - show_timer_text.get_height()//5))

# delete progres
    delete_text = pygame.font.Font.render(fancy_font, "Delete Progress", True, (255,255,255))
    delete_rect = pygame.Rect(width//2.7,height*0.75 - delete_text.get_height()//5,delete_text.get_width()*1.1,delete_text.get_height())
    pygame.draw.rect(SCREEN, (255,255,255),(width//2.5 - 50,height*0.75,30,30), 0 if delete else 2)
    SCREEN.blit(delete_text, (width//2.5,height*0.75 - delete_text.get_height()//5))

    delete_progress_text = pygame.font.Font.render(fancy_font, "Delete Progress", True, (255,60,60))
    delete_progress_rect = delete_progress_text.get_rect(topleft=(width-delete_progress_text.get_width()*1.1,height - delete_progress_text.get_height()))
    if delete:
        SCREEN.blit(delete_progress_text, (width-delete_progress_text.get_width()*1.1,height - delete_progress_text.get_height()))



def settings_logic(mouse_pos, event):
    global slider_x, music_slider_y, sfx_slider_y, slider_width, dragging_music, dragging_sfx, AL_count_on, show_timer_on, delete, delete_rect, show_timer_rect, al_count_rect, delete_progress_rect

    if event.type == pygame.MOUSEBUTTONDOWN:
        
        if pygame.Rect(slider_x, music_slider_y - 12, slider_width, 30).collidepoint(mouse_pos[0], mouse_pos[1]):
            dragging_music = True
        if pygame.Rect(slider_x, sfx_slider_y - 12, slider_width, 30).collidepoint(mouse_pos[0], mouse_pos[1]):
            dragging_sfx = True
        if al_count_rect.collidepoint(mouse_pos):
            sfx_manager.play("click")
            AL_count_on = not AL_count_on
        if show_timer_rect.collidepoint(mouse_pos):
            sfx_manager.play("click")
            show_timer_on = not show_timer_on
        if delete_rect.collidepoint(mouse_pos):
            sfx_manager.play("click")
            delete = not delete
        if delete_progress_rect.collidepoint(mouse_pos):
            with open("lib/text/progres/game.txt", "w+") as progress:
                progress.write("Night\n1\n")
                progress.write("Extras\nFalse\n")
                progress.write("Nightmare\nFalse\n")
                progress.write("deaf_mode_beaten:\nFalse\n")
                progress.write("deaf_unlocked:\nFalse")
            with open("lib/text/progres/settings.txt", "w+") as settings:
                settings.write("music_volume:\n1.0\n")
                settings.write("sfx_volume:\n1.0\n")
                settings.write("al_counter:\n0\n")
                settings.write("show_timer:\n0\n")
            return True, False, False
        

    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            dragging_music = False
            dragging_sfx = False

    elif event.type == pygame.MOUSEMOTION:
        if dragging_music:

            mouse_x = mouse_pos[0]
            music_manager.music_volume = (mouse_x - slider_x) / slider_width
            music_manager.music_volume = max(0.0, min(1.0, music_manager.music_volume))

            music_manager.volume_update()

        elif dragging_sfx:

            mouse_x = mouse_pos[0]
            sfx_manager.sfx_volume = (mouse_x - slider_x) / slider_width
            sfx_manager.sfx_volume = max(0.0, min(1.0, sfx_manager.sfx_volume))

            sfx_manager.volume_update()
    return False, AL_count_on, show_timer_on
