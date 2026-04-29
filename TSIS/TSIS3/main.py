# main.py - entry point for Racer TSIS3

import pygame
import sys
from persistence import load_settings, save_settings, save_score
from ui import main_menu, ask_name, settings_screen, leaderboard_screen, gameover_screen
from racer import run

pygame.init()
screen = pygame.display.set_mode((600, 700))
pygame.display.set_caption("Racer - TSIS3")
clock  = pygame.time.Clock()

# load saved settings
settings = load_settings()

while True:
    action = main_menu(screen, clock)

    if action == "quit":
        save_settings(settings)
        pygame.quit()
        sys.exit()

    elif action == "lb":
        leaderboard_screen(screen, clock)

    elif action == "settings":
        settings = settings_screen(screen, clock, settings)
        save_settings(settings)

    elif action == "play":
        name = ask_name(screen, clock)
        if not name:
            continue

        # game loop - retry keeps playing, menu goes back
        while True:
            score, dist, coins = run(screen, clock, settings, name)
            save_score(name, score, dist, coins)
            result = gameover_screen(screen, clock, score, dist, coins)
            if result == "menu":
                break
            elif result == "quit":
                save_settings(settings)
                pygame.quit()
                sys.exit()