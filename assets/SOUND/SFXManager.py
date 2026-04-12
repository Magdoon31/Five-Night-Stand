import random, pygame
pygame.mixer.init()
DoorSqueak = [pygame.mixer.Sound("assets/SOUND/door squeak1.mp3"), pygame.mixer.Sound("assets/SOUND/door squeak2.mp3")]
ClockChime = pygame.mixer.Sound("assets/SOUND/clockchimes.mp3")
light = pygame.mixer.Sound("assets/SOUND/light_flickering.mp3")


sfx_timer = 0
DSChanel = None
SFXon = False
CChChanel = None
LChanel = None
def SFX(CamON, dt):
    global sfx_timer, SFXon, DSChanel, ClockChime, light, CChChanel, LChanel
    sfx_timer += dt
    if sfx_timer >= 100:
        sfx_timer = 0
        if not SFXon:
            SFXrnd = random.randint(1, 2000)
            if SFXrnd == 1 and CamON:
                SFXon = True
                DSChanel = DoorSqueak[random.randint(0, len(DoorSqueak) - 1)].play()
            if SFXrnd == 2:
                SFXon = True
                CChChanel = ClockChime.play()
            if SFXrnd == 3 and CamON:
                SFXon = True
                LChanel = light.play()
    if (DSChanel and not DSChanel.get_busy()) or (CChChanel and not CChChanel.get_busy()) or (LChanel and not LChanel.get_busy()):
        SFXon = False
def MetalDoor(type):
    pygame.mixer.Sound(f"assets/SOUND/metal_door_{type}.mp3").play()
def CameraPullUp():
    pygame.mixer.Sound("assets/SOUND/camera pullout.mp3").play()
def Steps(type):
    pygame.mixer.Sound(f"assets/SOUND/steps_{type}.mp3").play()