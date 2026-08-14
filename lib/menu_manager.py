import pygame


def menu_GUI(
    fancy_font_title,
    SCREEN,
    width,
    height,
    mouse_pos,
    play,
    custom_night,
    extras_unlocked,
    extra,
    settings
):
    # Play
    play_color = (
        (255, 255, 255)
        if not play
        else (255, 90, 90)
    )

    play_text = pygame.font.Font.render(
        fancy_font_title,
        "Night",
        True,
        play_color
    )

    play_rect = play_text.get_rect(
        topleft=((width // 6) * 0.9, height * 0.05)
    )

    SCREEN.blit(
        play_text,
        ((width // 6) * 0.9, height * 0.05)
    )


    # Custom
    if extras_unlocked == "True":
        custom_color = (
            (255, 255, 255)
            if not custom_night
            else (255, 90, 90)
        )
    else:
        custom_color = (150, 150, 150)

    custom_text = pygame.font.Font.render(
        fancy_font_title,
        "Custom",
        True,
        custom_color
    )

    custom_rect = custom_text.get_rect(
        topleft=((width // 6) * 1.8, height * 0.05)
    )

    SCREEN.blit(
        custom_text,
        ((width // 6) * 1.8, height * 0.05)
    )


    # Extra
    if extras_unlocked == "True":
        extra_color = (
            (255, 255, 255)
            if not extra
            else (255, 90, 90)
        )
    else:
        extra_color = (150, 150, 150)

    extra_text = pygame.font.Font.render(
        fancy_font_title,
        "Extra",
        True,
        extra_color
    )

    extra_rect = extra_text.get_rect(
        topleft=((width // 6) * 3.2, height * 0.05)
    )

    SCREEN.blit(
        extra_text,
        ((width // 6) * 3.2, height * 0.05)
    )


    # Settings
    settings_color = (
        (255, 255, 255)
        if not settings
        else (255, 90, 90)
    )

    settings_text = pygame.font.Font.render(
        fancy_font_title,
        "Settings",
        True,
        settings_color
    )

    settings_rect = settings_text.get_rect(
        topleft=((width // 6) * 4.15, height * 0.05)
    )

    SCREEN.blit(
        settings_text,
        ((width // 6) * 4.15, height * 0.05)
    )


    # Mouse hover
    if play_rect.collidepoint(mouse_pos):
        pygame.draw.rect(
            SCREEN,
            (255, 255, 255) if not play else (255, 90, 90),
            (
                width // 6 * 0.9,
                height * 0.05 + play_rect.height * 0.80,
                play_rect.width,
                3
            ),
            0
        )

    elif custom_rect.collidepoint(mouse_pos) and extras_unlocked == "True":
        pygame.draw.rect(
            SCREEN,
            (255, 255, 255) if not custom_night else (255, 90, 90),
            (
                width // 6 * 1.8,
                height * 0.05 + custom_rect.height * 0.80,
                custom_rect.width,
                3
            ),
            0
        )

    elif extra_rect.collidepoint(mouse_pos) and extras_unlocked == "True":
        pygame.draw.rect(
            SCREEN,
            (255, 255, 255) if not extra else (255, 90, 90),
            (
                width // 6 * 3.2,
                height * 0.05 + extra_rect.height * 0.80,
                extra_rect.width,
                3
            ),
            0
        )

    elif settings_rect.collidepoint(mouse_pos):
        pygame.draw.rect(
            SCREEN,
            (255, 255, 255) if not settings else (255, 90, 90),
            (
                width // 6 * 4.15,
                height * 0.05 + settings_rect.height * 0.80,
                settings_rect.width,
                3
            ),
            0
        )


    return play_rect, custom_rect, extra_rect, settings_rect

