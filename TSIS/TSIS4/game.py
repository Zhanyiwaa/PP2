# game.py - snake gameplay TSIS4

import pygame
import random
import json
import os

# grid settings
CELL = 20
COLS = 28
ROWS = 26
W    = COLS * CELL
H    = ROWS * CELL + 60

# directions
UP    = (0, -1)
DOWN  = (0,  1)
LEFT  = (-1, 0)
RIGHT = (1,  0)

# colors
BG      = (0,   0,   0)
GRID_C  = (30,  30,  30)
WHITE   = (255, 255, 255)
GREEN   = (80,  210, 100)
DKGREEN = (50,  160, 70)
RED     = (220, 50,  50)
DARKRED = (100, 20,  20)
YELLOW  = (255, 220, 50)
CYAN    = (0,   210, 210)
GRAY    = (150, 150, 160)

def load_settings():
    if os.path.exists("settings.json"):
        data = json.load(open("settings.json"))
        data.setdefault("grid",        True)
        data.setdefault("sound",       False)
        data.setdefault("snake_color", [80, 210, 100])
        return data
    return {"snake_color": [80, 210, 100], "grid": True, "sound": False}

# run one game - returns (score, level)
def run_game(screen, personal_best):
    clock       = pygame.time.Clock()
    font        = pygame.font.SysFont("Arial", 18)
    font_big    = pygame.font.SysFont("Arial", 22, bold=True)
    s           = load_settings()
    snake_color = tuple(s["snake_color"])
    grid_on     = s["grid"]
    sound_on    = s["sound"]
    HUD         = 60

    # init mixer and load sound
    eat_sound = None
    if sound_on:
        try:
            pygame.mixer.init(44100, -16, 2, 512)
            eat_sound = pygame.mixer.Sound("eat.wav")
            print("Sound loaded OK")
        except Exception as e:
            print(f"Sound error: {e}")

    # starting snake in center
    snake     = [(COLS//2, ROWS//2)]
    direction = RIGHT
    next_dir  = RIGHT
    food      = None
    poison    = None
    obstacles = []

    score       = 0
    level       = 1
    foods_eaten = 0
    shield_on   = False
    active_pu   = None
    pu_end      = 0

    # speed - lower number = faster snake
    def move_delay():
        base = max(80, 180 - (level - 1) * 15)
        if active_pu == "speed": return max(50, base - 60)
        if active_pu == "slow":  return base + 70
        return base

    # get all empty cells on grid
    def free():
        taken = set(snake) | set(obstacles)
        if food:   taken.add(food)
        if poison: taken.add(poison)
        return [(c, r) for c in range(COLS) for r in range(ROWS) if (c, r) not in taken]

    def place_food():
        f = free()
        return random.choice(f) if f else None

    # place wall obstacles from level 3
    def place_obstacles():
        count = (level - 2) * 4
        head  = snake[0]
        cells = [c for c in free() if abs(c[0]-head[0]) + abs(c[1]-head[1]) > 5]
        random.shuffle(cells)
        return cells[:count]

    food   = place_food()
    poison = place_food()

    last_move = pygame.time.get_ticks()

    while True:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return score, level
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP    and direction != DOWN:  next_dir = UP
                if event.key == pygame.K_DOWN  and direction != UP:    next_dir = DOWN
                if event.key == pygame.K_LEFT  and direction != RIGHT: next_dir = LEFT
                if event.key == pygame.K_RIGHT and direction != LEFT:  next_dir = RIGHT

        # move snake every move_delay ms
        if now - last_move >= move_delay():
            last_move = now
            direction = next_dir
            hx, hy   = snake[0]
            nx, ny   = hx + direction[0], hy + direction[1]

            # hit wall
            if not (0 <= nx < COLS and 0 <= ny < ROWS):
                if shield_on:
                    shield_on = False
                    active_pu = None
                    nx, ny = nx % COLS, ny % ROWS
                else:
                    return score, level

            # hit itself
            if (nx, ny) in snake[1:]:
                if shield_on:
                    shield_on = False
                    active_pu = None
                else:
                    return score, level

            # hit obstacle
            if (nx, ny) in obstacles:
                if shield_on:
                    shield_on = False
                    active_pu = None
                    obstacles.remove((nx, ny))
                else:
                    return score, level

            snake.insert(0, (nx, ny))

            # ate normal food
            if (nx, ny) == food:
                score       += 10
                foods_eaten += 1
                # play sound
                if eat_sound:
                    eat_sound.play()
                food = place_food()
                # level up every 5 foods
                if foods_eaten % 5 == 0:
                    level += 1
                    if level >= 3:
                        obstacles = place_obstacles()
                    poison = place_food()

            # ate poison - shorten snake by 2
            elif (nx, ny) == poison:
                snake = snake[:-2]
                if len(snake) <= 0:
                    return score, level
                poison = place_food()

            else:
                # normal move - remove tail
                snake.pop()

            # check power up expired
            if active_pu in ("speed", "slow") and now > pu_end:
                active_pu = None

        # ── draw ──────────────────────────────────────────────
        screen.fill(BG)

        # HUD bar at top
        pygame.draw.rect(screen, (15, 15, 15), (0, 0, W, HUD))
        pygame.draw.line(screen, GRAY, (0, HUD), (W, HUD), 1)
        screen.blit(font.render(f"Score: {score}",         True, WHITE), (10, 10))
        screen.blit(font.render(f"Level: {level}",         True, WHITE), (10, 34))
        screen.blit(font.render(f"Best:  {personal_best}", True, GRAY),  (200, 10))
        if active_pu:
            screen.blit(font_big.render(f"[{active_pu.upper()}]", True, YELLOW), (200, 34))

        OY = HUD  # arena starts below HUD

        # grid lines
        if grid_on:
            for c in range(COLS + 1):
                pygame.draw.line(screen, GRID_C, (c*CELL, OY), (c*CELL, OY + ROWS*CELL))
            for r in range(ROWS + 1):
                pygame.draw.line(screen, GRID_C, (0, r*CELL+OY), (W, r*CELL+OY))

        # obstacles - gray squares
        for ox, oy in obstacles:
            pygame.draw.rect(screen, GRAY, (ox*CELL, oy*CELL+OY, CELL, CELL))

        # food - white square
        if food:
            fx, fy = food
            pygame.draw.rect(screen, WHITE, (fx*CELL+2, fy*CELL+OY+2, CELL-4, CELL-4))

        # poison - dark red square with X
        if poison:
            px, py = poison
            r = pygame.Rect(px*CELL+2, py*CELL+OY+2, CELL-4, CELL-4)
            pygame.draw.rect(screen, DARKRED, r)
            pygame.draw.line(screen, RED, r.topleft, r.bottomright, 2)
            pygame.draw.line(screen, RED, r.topright, r.bottomleft, 2)

        # snake - squares
        for i, (sc, sr) in enumerate(snake):
            color = snake_color if i == 0 else DKGREEN
            rect  = pygame.Rect(sc*CELL+1, sr*CELL+OY+1, CELL-2, CELL-2)
            pygame.draw.rect(screen, color, rect)
            # cyan border when shield active
            if i == 0 and shield_on:
                pygame.draw.rect(screen, CYAN, rect, 2)

        pygame.display.flip()
        clock.tick(60)