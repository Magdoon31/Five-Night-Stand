from lib import sfx_manager as sfx


def camera_manager(width, height, room_positions, mouse_pos, SelectedCam):
    audio_lure_width = 0.02 * width
    audio_lure_height = 0.06 * height

    # Camera positions
    if (
        room_positions["C"][0] - audio_lure_width // 2
        <= mouse_pos[0]
        <= room_positions["C"][0] + audio_lure_width // 2
        and
        room_positions["C"][1] - audio_lure_height // 2
        <= mouse_pos[1]
        <= room_positions["C"][1] + audio_lure_height // 2
    ):
        return "C"

    if (
        room_positions["LH"][0] - audio_lure_width // 2
        <= mouse_pos[0]
        <= room_positions["LH"][0] + audio_lure_width // 2
        and
        room_positions["LH"][1] - audio_lure_height // 2
        <= mouse_pos[1]
        <= room_positions["LH"][1] + audio_lure_height // 2
    ):
        return "LH"

    if (
        room_positions["BH"][0] - audio_lure_width // 2
        <= mouse_pos[0]
        <= room_positions["BH"][0] + audio_lure_width // 2
        and
        room_positions["BH"][1] - audio_lure_height // 2
        <= mouse_pos[1]
        <= room_positions["BH"][1] + audio_lure_height // 2
    ):
        return "BH"

    if (
        room_positions["BR"][0] - audio_lure_width // 2
        <= mouse_pos[0]
        <= room_positions["BR"][0] + audio_lure_width // 2
        and
        room_positions["BR"][1] - audio_lure_height // 2
        <= mouse_pos[1]
        <= room_positions["BR"][1] + audio_lure_height // 2
    ):
        return "BR"

    if (
        room_positions["E"][0] - audio_lure_width // 2
        <= mouse_pos[0]
        <= room_positions["E"][0] + audio_lure_width // 2
        and
        room_positions["E"][1] - audio_lure_height // 2
        <= mouse_pos[1]
        <= room_positions["E"][1] + audio_lure_height // 2
    ):
        return "E"

    if (
        room_positions["DB"][0] - audio_lure_width // 2
        <= mouse_pos[0]
        <= room_positions["DB"][0] + audio_lure_width // 2
        and
        room_positions["DB"][1] - audio_lure_height // 2
        <= mouse_pos[1]
        <= room_positions["DB"][1] + audio_lure_height // 2
    ):
        return "DB"

    if (
        room_positions["DA"][0] - audio_lure_width // 2
        <= mouse_pos[0]
        <= room_positions["DA"][0] + audio_lure_width // 2
        and
        room_positions["DA"][1] - audio_lure_height // 2
        <= mouse_pos[1]
        <= room_positions["DA"][1] + audio_lure_height // 2
    ):
        return "DA"

    if (
        room_positions["A"][0] - audio_lure_width // 2
        <= mouse_pos[0]
        <= room_positions["A"][0] + audio_lure_width // 2
        and
        room_positions["A"][1] - audio_lure_height // 2
        <= mouse_pos[1]
        <= room_positions["A"][1] + audio_lure_height // 2
    ):
        return "A"
    
    return SelectedCam


def door_manager(door_positions, mouse_pos, LockedDoor, DoorTimer):
    if (
        door_positions["DA"][0]
        <= mouse_pos[0]
        <= door_positions["DA"][0] + 60
        and
        door_positions["DA"][1]
        <= mouse_pos[1]
        <= door_positions["DA"][1] + 22
    ):
        if LockedDoor == "DA":
            LockedDoor = None
        else:
            LockedDoor = "DA"
        sfx.play("metal_door_close")
        DoorTimer = 250

    elif (
        door_positions["E"][0]
        <= mouse_pos[0]
        <= door_positions["E"][0] + 60
        and
        door_positions["E"][1]
        <= mouse_pos[1]
        <= door_positions["E"][1] + 22
    ):
        if LockedDoor == "E":
            LockedDoor = None
        else:
            LockedDoor = "E"
        sfx.play("metal_door_close")
        DoorTimer = 250

    elif (
        door_positions["UH"][0]
        <= mouse_pos[0]
        <= door_positions["UH"][0] + 60
        and
        door_positions["UH"][1]
        <= mouse_pos[1]
        <= door_positions["UH"][1] + 22
    ):
        if LockedDoor == "UH":
            LockedDoor = None
        else:
            LockedDoor = "UH"
        sfx.play("metal_door_close")
        DoorTimer = 250

    

    

    return LockedDoor, DoorTimer
