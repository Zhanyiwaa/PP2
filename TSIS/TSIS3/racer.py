# racer.py - main game logic for TSIS3

import pygame
import random

# car color options
CAR_COLORS = {
    "blue":   (0,   150, 255),
    "red":    (220, 50,  50),
    "green":  (50,  200, 80),
    "yellow": (255, 220, 0),
    "white":  (230, 230, 230),
}

# difficulty changes spawn speed
DIFF_SPEED = {"easy": 3, "normal": 5, "hard": 7}

# run one game session, returns score, distance, coins
def run(screen, clock, settings, name):
    W, H = screen.get_size()
    font = pygame.font.SysFont("Arial", 20, bold=True)

    # load images - put car.png, enemy.png, coin.png in same folder
    car_img   = pygame.image.load("car.png").convert_alpha()
    enemy_img = pygame.image.load("enemy.png").convert_alpha()
    coin_img  = pygame.image.load("coin.png").convert_alpha()

    # scale images to fit
    car_img   = pygame.transform.scale(car_img,   (50, 90))
    enemy_img = pygame.transform.scale(enemy_img, (50, 90))
    coin_img  = pygame.transform.scale(coin_img,  (30, 30))

    # road lanes x positions
    lanes     = [120, 220, 320, 420]
    car_lane  = 1
    car_x     = lanes[car_lane]
    car_y     = H - 120
    car_rect  = pygame.Rect(car_x, car_y, 50, 90)

    speed     = DIFF_SPEED.get(settings.get("difficulty", "normal"), 5)
    car_color = CAR_COLORS.get(settings.get("color", "blue"), (0,150,255))

    # game state
    score    = 0
    distance = 0
    coins    = 0
    enemies  = []
    coin_list= []

    # road stripe positions for scrolling effect
    stripes  = [{"x": l+25, "y": i*120} for l in [170,270,370] for i in range(6)]

    # timers for spawning
    enemy_timer = 0
    coin_timer  = 0

    # power up state
    nitro_active = False
    nitro_timer  = 0
    shield_active= False
    shield_timer = 0

    # spawn a new enemy in a random lane not same as player
    def spawn_enemy():
        lane = random.choice([l for l in lanes if l != lanes[car_lane]])
        enemies.append({"rect": pygame.Rect(lane, -90, 50, 90), "speed": speed + random.randint(0,2)})

    # spawn a coin in random lane
    def spawn_coin():
        lane = random.choice(lanes)
        coin_list.append(pygame.Rect(lane, -30, 30, 30))

    # draw scrolling road
    def draw_road():
        # gray road background
        pygame.draw.rect(screen, (60, 60, 60), (90, 0, 400, H))
        # white lane dividers
        for stripe in stripes:
            pygame.draw.rect(screen, (255,255,255), (stripe["x"], stripe["y"], 5, 60))

    running = True
    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return score, distance, coins

        # move player left/right between lanes
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            car_lane = max(0, car_lane - 1)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            car_lane = min(len(lanes)-1, car_lane + 1)

        # smooth car movement to target lane
        target_x = lanes[car_lane]
        car_x += (target_x - car_x) * 0.2
        car_rect.x = int(car_x)

        # scroll road stripes down
        for stripe in stripes:
            stripe["y"] += speed
            if stripe["y"] > H:
                stripe["y"] = -60

        # spawn enemies and coins on timer
        enemy_timer += dt
        coin_timer  += dt
        if enemy_timer > 1500:
            spawn_enemy()
            enemy_timer = 0
        if coin_timer > 900:
            spawn_coin()
            coin_timer = 0

        # move enemies down
        for e in enemies:
            e["rect"].y += e["speed"]
        enemies = [e for e in enemies if e["rect"].y < H + 100]

        # move coins down
        for c in coin_list:
            c.y += speed
        coin_list[:] = [c for c in coin_list if c.y < H + 50]

        # check coin collection
        for c in coin_list[:]:
            if car_rect.colliderect(c):
                coins += 1
                score += 15
                coin_list.remove(c)

        # check enemy collision
        for e in enemies:
            if car_rect.colliderect(e["rect"]):
                if shield_active:
                    shield_active = False
                    enemies.remove(e)
                else:
                    running = False
                break

        # increase distance and score over time
        distance += speed
        score    += 1

        # draw everything
        screen.fill((30, 30, 45))
        draw_road()

        # draw coins
        for c in coin_list:
            screen.blit(coin_img, c)

        # draw enemies
        for e in enemies:
            screen.blit(enemy_img, e["rect"])

        # draw player car (tinted with chosen color)
        tinted = car_img.copy()
        tinted.fill(car_color + (100,), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(tinted, car_rect)

        # shield glow around car
        if shield_active:
            pygame.draw.rect(screen, (0,220,220), car_rect.inflate(8,8), 3, border_radius=8)

        # HUD top left
        screen.blit(font.render(f"Score: {score}",    True, (255,255,255)), (10, 10))
        screen.blit(font.render(f"Dist:  {distance//100}m", True, (255,255,255)), (10, 36))
        screen.blit(font.render(f"Coins: {coins}",    True, (255,255,255)), (10, 62))

        pygame.display.flip()

    return score, distance // 100, coins