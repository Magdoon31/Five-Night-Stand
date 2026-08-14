import random
from lib import sfx_manager as sfx

def girl_try_movement(girl_AI,height):
    rnd = random.random()
    move_chance = (girl_AI / 100) ** 1.5 * 0.01333
    if rnd < move_chance:
        sfx.play("psst")
        return "You", random.randint(1,height//2)
    else:
        return "C", 0
    
def girl_try_sabotage(girl_AI, nightmare, scan_timer):
    rnd = random.randint(1,3)
    if rnd == 1:
        sfx.play("girl_laugh")
        if nightmare:
            return 1080, True
        else:
            return 1380, False
    else:
        return scan_timer, False