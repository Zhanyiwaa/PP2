# ui.py - all game screens (menu, leaderboard, settings, gameover)

import pygame
from persistence import load_scores

WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
GRAY   = (180, 180, 180)
DARK   = (30,  30,  50)
YELLOW = (255, 220, 50)
RED    = (220, 50,  50)
BLUE   = (60,  100, 220)

def draw_button(screen, text, rect, font, active=False):
    color = BLUE if active else GRAY
    pygame.draw.rect(screen, color, rect, border_radius=8)
    lbl = font.render(text, True, WHITE)
    screen.blit(lbl, (rect.centerx - lbl.get_width()//2,
                      rect.centery - lbl.get_height()//2))

# main menu - returns what user clicked
def main_menu(screen, clock):
    font_big = pygame.font.SysFont("Arial", 52, bold=True)
    font     = pygame.font.SysFont("Arial", 24)
    W, H     = screen.get_size()

    buttons = {
        "play":     pygame.Rect(W//2-100, 220, 200, 48),
        "lb":       pygame.Rect(W//2-100, 284, 200, 48),
        "settings": pygame.Rect(W//2-100, 348, 200, 48),
        "quit":     pygame.Rect(W//2-100, 412, 200, 48),
    }
    labels = {"play":"Play","lb":"Leaderboard","settings":"Settings","quit":"Quit"}

    while True:
        screen.fill(DARK)
        title = font_big.render("RACER", True, YELLOW)
        screen.blit(title, (W//2 - title.get_width()//2, 120))

        mx, my = pygame.mouse.get_pos()
        for key, rect in buttons.items():
            draw_button(screen, labels[key], rect, font, rect.collidepoint(mx, my))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                for key, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        return key

# ask player name before game
def ask_name(screen, clock):
    font = pygame.font.SysFont("Arial", 24)
    W, H = screen.get_size()
    name = ""

    while True:
        screen.fill(DARK)
        lbl = font.render("Enter your name:", True, WHITE)
        screen.blit(lbl, (W//2 - lbl.get_width()//2, 200))
        box = font.render(name + "|", True, YELLOW)
        screen.blit(box, (W//2 - box.get_width()//2, 260))
        hint = font.render("Press Enter to start", True, GRAY)
        screen.blit(hint, (W//2 - hint.get_width()//2, 320))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ""
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.unicode.isprintable() and len(name) < 16:
                    name += event.unicode

# game over screen
def gameover_screen(screen, clock, score, dist, coins):
    font_big = pygame.font.SysFont("Arial", 44, bold=True)
    font     = pygame.font.SysFont("Arial", 22)
    W, H     = screen.get_size()

    retry_btn = pygame.Rect(W//2-110, 380, 200, 48)
    menu_btn  = pygame.Rect(W//2-110, 444, 200, 48)

    while True:
        screen.fill(DARK)
        title = font_big.render("GAME OVER", True, RED)
        screen.blit(title, (W//2 - title.get_width()//2, 100))

        for i, text in enumerate([f"Score: {score}", f"Distance: {dist}m", f"Coins: {coins}"]):
            lbl = font.render(text, True, WHITE)
            screen.blit(lbl, (W//2 - lbl.get_width()//2, 200 + i*44))

        mx, my = pygame.mouse.get_pos()
        draw_button(screen, "Retry",     retry_btn, font, retry_btn.collidepoint(mx, my))
        draw_button(screen, "Main Menu", menu_btn,  font, menu_btn.collidepoint(mx, my))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_btn.collidepoint(event.pos): return "retry"
                if menu_btn.collidepoint(event.pos):  return "menu"

# leaderboard screen
def leaderboard_screen(screen, clock):
    font_big = pygame.font.SysFont("Arial", 36, bold=True)
    font     = pygame.font.SysFont("Arial", 20)
    W, H     = screen.get_size()
    scores   = load_scores()
    back_btn = pygame.Rect(W//2-100, H-80, 200, 48)

    while True:
        screen.fill(DARK)
        title = font_big.render("LEADERBOARD", True, YELLOW)
        screen.blit(title, (W//2 - title.get_width()//2, 30))

        for i, entry in enumerate(scores[:10]):
            color = YELLOW if i == 0 else WHITE
            row = f"{i+1}. {entry['name']}  score:{entry['score']}  dist:{entry['dist']}m  coins:{entry['coins']}"
            lbl = font.render(row, True, color)
            screen.blit(lbl, (50, 90 + i*36))

        if not scores:
            lbl = font.render("No scores yet!", True, GRAY)
            screen.blit(lbl, (W//2 - lbl.get_width()//2, 200))

        mx, my = pygame.mouse.get_pos()
        draw_button(screen, "Back", back_btn, font, back_btn.collidepoint(mx, my))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos): return

# settings screen
def settings_screen(screen, clock, settings):
    font_big = pygame.font.SysFont("Arial", 36, bold=True)
    font     = pygame.font.SysFont("Arial", 22)
    W, H     = screen.get_size()

    colors   = ["blue", "red", "green", "yellow", "white"]
    diffs    = ["easy", "normal", "hard"]
    save_btn = pygame.Rect(W//2-110, H-90, 220, 48)

    while True:
        screen.fill(DARK)
        title = font_big.render("SETTINGS", True, YELLOW)
        screen.blit(title, (W//2 - title.get_width()//2, 30))

        # sound toggle
        sound_btn = pygame.Rect(W//2+20, 120, 120, 38)
        screen.blit(font.render("Sound:", True, WHITE), (W//2-160, 128))
        draw_button(screen, "ON" if settings.get("sound", True) else "OFF",
                    sound_btn, font, sound_btn.collidepoint(*pygame.mouse.get_pos()))

        # car color buttons
        screen.blit(font.render("Car color:", True, WHITE), (W//2-160, 190))
        color_btns = []
        for i, c in enumerate(colors):
            r = pygame.Rect(W//2-160 + i*90, 220, 82, 36)
            color_btns.append((r, c))
            # use .get() so no crash if key missing
            active = settings.get("color", "blue") == c
            pygame.draw.rect(screen, BLUE if active else GRAY, r, border_radius=6)
            lbl = font.render(c, True, WHITE)
            screen.blit(lbl, (r.x+4, r.y+8))

        # difficulty buttons
        screen.blit(font.render("Difficulty:", True, WHITE), (W//2-160, 290))
        diff_btns = []
        for i, d in enumerate(diffs):
            r = pygame.Rect(W//2-160 + i*120, 320, 110, 36)
            diff_btns.append((r, d))
            # use .get() so no crash if key missing
            active = settings.get("difficulty", "normal") == d
            pygame.draw.rect(screen, BLUE if active else GRAY, r, border_radius=6)
            lbl = font.render(d, True, WHITE)
            screen.blit(lbl, (r.x+8, r.y+8))

        mx, my = pygame.mouse.get_pos()
        draw_button(screen, "Save & Back", save_btn, font, save_btn.collidepoint(mx, my))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return settings
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_btn.collidepoint(event.pos):
                    settings["sound"] = not settings.get("sound", True)
                for r, c in color_btns:
                    if r.collidepoint(event.pos):
                        settings["color"] = c
                for r, d in diff_btns:
                    if r.collidepoint(event.pos):
                        settings["difficulty"] = d
                if save_btn.collidepoint(event.pos):
                    return settings