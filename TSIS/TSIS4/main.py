# main.py - entry point Snake TSIS4

import pygame
import sys
import json
import os
from db   import init_db, save_session, get_top10, get_best
from game import run_game, W, H

# init pygame and mixer before anything
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Snake - TSIS4")
clock  = pygame.time.Clock()

# colors
DARK   = (0,   0,   0)
WHITE  = (255, 255, 255)
YELLOW = (255, 220, 50)
GREEN  = (80,  210, 100)
GRAY   = (150, 150, 160)
RED    = (220, 50,  50)
BLUE   = (60,  100, 220)

font     = pygame.font.SysFont("Arial", 22)
font_big = pygame.font.SysFont("Arial", 44, bold=True)
font_sm  = pygame.font.SysFont("Arial", 17)

# load background music
try:
    pygame.mixer.music.load("eat.wav")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)  # -1 means loop forever
    print("Music loaded OK")
except Exception as e:
    print(f"Music error: {e}")

# try to connect db
db_ok = True
try:
    init_db()
except Exception as e:
    print(f"DB not connected: {e}")
    db_ok = False

def draw_btn(text, rect, hover=False):
    pygame.draw.rect(screen, BLUE if hover else (50, 80, 160), rect)
    pygame.draw.rect(screen, GREEN, rect, 2)
    lbl = font.render(text, True, WHITE)
    screen.blit(lbl, (rect.centerx - lbl.get_width()//2,
                      rect.centery - lbl.get_height()//2))

# main menu screen
def main_menu():
    name   = ""
    typing = True
    bx     = W//2 - 100
    btns   = {
        "play":        pygame.Rect(bx, 280, 200, 46),
        "leaderboard": pygame.Rect(bx, 340, 200, 46),
        "settings":    pygame.Rect(bx, 400, 200, 46),
        "quit":        pygame.Rect(bx, 460, 200, 46),
    }
    while True:
        screen.fill(DARK)
        title = font_big.render("SNAKE", True, GREEN)
        screen.blit(title, (W//2 - title.get_width()//2, 60))

        screen.blit(font_sm.render("Your name:", True, GRAY), (bx, 180))
        field = pygame.Rect(bx, 205, 200, 36)
        pygame.draw.rect(screen, (25, 25, 25), field)
        pygame.draw.rect(screen, GREEN if typing else GRAY, field, 2)
        screen.blit(font.render(name + ("|" if typing else ""), True, WHITE), (bx+8, 210))

        mx, my = pygame.mouse.get_pos()
        for action, rect in btns.items():
            draw_btn(action.capitalize(), rect, rect.collidepoint(mx, my))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", ""
            if event.type == pygame.KEYDOWN and typing:
                if event.key == pygame.K_RETURN:
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.unicode.isprintable() and len(name) < 16:
                    name += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                typing = field.collidepoint(event.pos)
                for action, rect in btns.items():
                    if rect.collidepoint(event.pos):
                        return action, name or "Player"

# game over screen
def game_over(score, level, best):
    bx    = W//2 - 100
    retry = pygame.Rect(bx, 340, 200, 46)
    menu  = pygame.Rect(bx, 400, 200, 46)

    while True:
        screen.fill(DARK)
        title = font_big.render("GAME OVER", True, RED)
        screen.blit(title, (W//2 - title.get_width()//2, 80))

        for i, txt in enumerate([f"Score: {score}", f"Level: {level}", f"Best:  {best}"]):
            lbl = font.render(txt, True, WHITE)
            screen.blit(lbl, (W//2 - lbl.get_width()//2, 180 + i*44))

        mx, my = pygame.mouse.get_pos()
        draw_btn("Retry",     retry, retry.collidepoint(mx, my))
        draw_btn("Main Menu", menu,  menu.collidepoint(mx, my))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "menu"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry.collidepoint(event.pos): return "retry"
                if menu.collidepoint(event.pos):  return "menu"

# leaderboard - loads fresh from db every time
def leaderboard():
    back = pygame.Rect(W//2 - 100, H-70, 200, 44)

    while True:
        # load fresh every frame so it updates automatically
        rows = get_top10() if db_ok else []

        screen.fill(DARK)
        title = font_big.render("TOP 10", True, YELLOW)
        screen.blit(title, (W//2 - title.get_width()//2, 20))

        # column headers
        screen.blit(font_sm.render("#", True, GRAY),     (30,  75))
        screen.blit(font_sm.render("Name", True, GRAY),  (60,  75))
        screen.blit(font_sm.render("Score", True, GRAY), (260, 75))
        screen.blit(font_sm.render("Level", True, GRAY), (370, 75))
        screen.blit(font_sm.render("Date", True, GRAY),  (450, 75))
        pygame.draw.line(screen, GRAY, (20, 95), (W-20, 95), 1)

        for i, e in enumerate(rows):
            color = YELLOW if i == 0 else WHITE
            y     = 100 + i * 34
            screen.blit(font_sm.render(str(i+1),              True, color), (30,  y))
            screen.blit(font_sm.render(e['username'][:12],    True, color), (60,  y))
            screen.blit(font_sm.render(str(e['score']),       True, color), (260, y))
            screen.blit(font_sm.render(str(e['level_reached']),True,color), (370, y))
            screen.blit(font_sm.render(e['date'],             True, color), (450, y))

        if not rows:
            lbl = font.render("No scores yet — play first!", True, GRAY)
            screen.blit(lbl, (W//2 - lbl.get_width()//2, 200))

        mx, my = pygame.mouse.get_pos()
        draw_btn("Back", back, back.collidepoint(mx, my))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.collidepoint(event.pos): return

# settings screen
def settings():
    if os.path.exists("settings.json"):
        data = json.load(open("settings.json"))
    else:
        data = {}
    data.setdefault("grid",        True)
    data.setdefault("sound",       False)
    data.setdefault("snake_color", [80, 210, 100])

    save = pygame.Rect(W//2 - 110, H-80, 220, 44)

    color_opts = [
        ("Green",  [80,  210, 100]),
        ("Blue",   [60,  130, 220]),
        ("Orange", [255, 140, 0]),
        ("Pink",   [220, 80,  160]),
    ]

    while True:
        screen.fill(DARK)
        title = font_big.render("SETTINGS", True, GREEN)
        screen.blit(title, (W//2 - title.get_width()//2, 20))

        # grid toggle
        g_btn = pygame.Rect(W//2 + 20, 120, 110, 36)
        screen.blit(font.render("Grid:", True, WHITE), (W//2 - 160, 126))
        pygame.draw.rect(screen, BLUE if data["grid"] else (80, 80, 80), g_btn)
        pygame.draw.rect(screen, WHITE, g_btn, 2)
        lbl = font.render("ON" if data["grid"] else "OFF", True, WHITE)
        screen.blit(lbl, (g_btn.centerx - lbl.get_width()//2,
                          g_btn.centery - lbl.get_height()//2))

        # sound toggle
        s_btn = pygame.Rect(W//2 + 20, 180, 110, 36)
        screen.blit(font.render("Music:", True, WHITE), (W//2 - 160, 186))
        pygame.draw.rect(screen, BLUE if data["sound"] else (80, 80, 80), s_btn)
        pygame.draw.rect(screen, WHITE, s_btn, 2)
        lbl = font.render("ON" if data["sound"] else "OFF", True, WHITE)
        screen.blit(lbl, (s_btn.centerx - lbl.get_width()//2,
                          s_btn.centery - lbl.get_height()//2))

        # snake color
        screen.blit(font.render("Snake color:", True, WHITE), (W//2 - 160, 250))
        crects = []
        for i, (name, rgb) in enumerate(color_opts):
            r = pygame.Rect(W//2 - 160 + i*90, 280, 82, 34)
            crects.append((r, rgb))
            pygame.draw.rect(screen, rgb, r)
            if data["snake_color"] == rgb:
                pygame.draw.rect(screen, WHITE, r, 3)
            lbl = font_sm.render(name, True, WHITE)
            screen.blit(lbl, (r.centerx - lbl.get_width()//2,
                               r.centery - lbl.get_height()//2))

        mx, my = pygame.mouse.get_pos()
        draw_btn("Save & Back", save, save.collidepoint(mx, my))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if g_btn.collidepoint(event.pos):
                    data["grid"] = not data["grid"]
                if s_btn.collidepoint(event.pos):
                    data["sound"] = not data["sound"]
                    # toggle background music
                    if data["sound"]:
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.stop()
                for r, rgb in crects:
                    if r.collidepoint(event.pos):
                        data["snake_color"] = rgb
                if save.collidepoint(event.pos):
                    json.dump(data, open("settings.json", "w"), indent=2)
                    return

# main loop
while True:
    action, username = main_menu()

    if action == "quit":
        pygame.quit()
        sys.exit()

    elif action == "leaderboard":
        leaderboard()

    elif action == "settings":
        settings()

    elif action == "play":
        best = get_best(username) if db_ok else 0
        while True:
            score, level = run_game(screen, best)
            # save to db right after game ends
            if db_ok:
                save_session(username, score, level)
                best = max(best, score)
                print(f"Saved: {username} score={score} level={level}")
            result = game_over(score, level, best)
            if result == "retry": continue
            break