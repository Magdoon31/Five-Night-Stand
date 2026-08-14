import random, pygame
pygame.mixer.init()
door_squeak = [pygame.mixer.Sound("assets/SOUND/door squeak1.mp3"), pygame.mixer.Sound("assets/SOUND/door squeak2.mp3")]
clock_chime = pygame.mixer.Sound("assets/SOUND/clockchimes.mp3")
light = pygame.mixer.Sound("assets/SOUND/light_flickering.mp3")
flashlight_sfx = pygame.mixer.Sound("assets/SOUND/flashlight.mp3")

sounds = {
    "metal_door_bang": pygame.mixer.Sound("assets/SOUND/metal_door_bang.mp3"),
    "metal_door_close": pygame.mixer.Sound("assets/SOUND/metal_door_close.mp3"),
    "camera_pull_up": pygame.mixer.Sound("assets/SOUND/camera pullout.mp3"),
    "steps_left": pygame.mixer.Sound("assets/SOUND/steps_left.mp3"),
    "steps_right": pygame.mixer.Sound("assets/SOUND/steps_right.mp3"),
    "psst": pygame.mixer.Sound("assets/SOUND/psst.mp3"),
    "girl_laugh": pygame.mixer.Sound("assets/SOUND/girl_laugh.mp3"),
    "girl_vanish": pygame.mixer.Sound("assets/SOUND/girl_disappear.mp3"),
    "last_7_sec": pygame.mixer.Sound("assets/SOUND/last 7 sec.mp3"),
    "jumpscare": pygame.mixer.Sound("assets/SOUND/Jumpscare.mp3"),
    "audio_lure": pygame.mixer.Sound("assets/SOUND/AudioLure.mp3"),
    "click": pygame.mixer.Sound("assets/SOUND/click.mp3"),
    "error": pygame.mixer.Sound("assets/SOUND/Error.mp3"),
    "secret_text": pygame.mixer.Sound("assets/SOUND/secret.mp3"),
    "scan": pygame.mixer.Sound("assets/SOUND/scan.mp3"),
    "breath": pygame.mixer.Sound("assets/SOUND/locust/breath.mp3"),
    "camera_static": pygame.mixer.Sound("assets/SOUND/locust/camera_static.mp3"),
    "deep_footsteps_left": pygame.mixer.Sound("assets/SOUND/locust/deepfootstepsleft.mp3"),
    "deep_footsteps_right": pygame.mixer.Sound("assets/SOUND/locust/deepfootstepsright.mp3"),
    "door_creak_left": pygame.mixer.Sound("assets/SOUND/locust/doorcreak_left.mp3"),
    "door_creak_right": pygame.mixer.Sound("assets/SOUND/locust/doorcreak_right.mp3"),
    "fast_run_left": pygame.mixer.Sound("assets/SOUND/locust/fastrunleft.mp3"),
    "fast_run_right": pygame.mixer.Sound("assets/SOUND/locust/fastrunright.mp3"),
    "small_footsteps": pygame.mixer.Sound("assets/SOUND/locust/small_footsteps.mp3"),
    "small_footsteps2": pygame.mixer.Sound("assets/SOUND/locust/small_footsteps2.mp3"),
    "small_footsteps3": pygame.mixer.Sound("assets/SOUND/locust/small_footsteps3.mp3")
}


sfx_volume = 1.0

# random ambience sfx 
sfx_timer = 0
door_squeak_channel = None
sfx_on = False
flashlight_sfx_status = False
clock_chime_channel = None
light_channel = None

def random_ambience_sfx(CamON):
    global sfx_timer, sfx_on, door_squeak_channel, clock_chime, light, clock_chime_channel, light_channel
    sfx_timer += 1
    if sfx_timer >= 100:
        sfx_timer = 0
        if not sfx_on:
            SFXrnd = random.randint(1, 2000)
            if SFXrnd == 1 and CamON:
                sfx_on = True
                door_squeak_channel = door_squeak[random.randint(0, len(door_squeak) - 1)].play()
            if SFXrnd == 2:
                sfx_on = True
                clock_chime_channel = clock_chime.play()
            if SFXrnd == 3 and CamON:
                sfx_on = True
                light_channel = light.play()
    if (door_squeak_channel and not door_squeak_channel.get_busy()) or (clock_chime_channel and not clock_chime_channel.get_busy()) or (light_channel and not light_channel.get_busy()):
        sfx_on = False
def play(name):  
    sounds[name].play()

def stop():
    for sound in sounds.values():
        sound.stop()
def volume_update():
    for sound in sounds.values():
        sound.set_volume(sfx_volume)

def flashlight(flashlight_toogle):
    global flashlight_sfx_status
    if not flashlight_toogle:
        flashlight_sfx_status = False
        flashlight_sfx.stop()
        return
    if not flashlight_sfx_status:
        flashlight_sfx.play(-1)
        flashlight_sfx_status = True
    

        