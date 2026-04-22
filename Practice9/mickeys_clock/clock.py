import pygame
import datetime
import os


class MickeyClock:
    def __init__(self, screen_width, screen_height):
        self.screen_size = (screen_width, screen_height)
        self.center = (screen_width // 2, screen_height // 2)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(base_dir, "images")

        # 🔥 BACKGROUND (если картинка сломана → будет белый фон)
        try:
            self.bg = pygame.image.load(os.path.join(img_dir, "clock.png"))
            self.bg = pygame.transform.scale(self.bg, self.screen_size)
        except:
            self.bg = pygame.Surface(self.screen_size)
            self.bg.fill((255, 255, 255))

        # Mickey body
        try:
            self.mickey_body = pygame.image.load(os.path.join(img_dir, "mickey.png")).convert_alpha()
            self.mickey_body = pygame.transform.scale(self.mickey_body, (380, 500))
            self.mickey_rect = self.mickey_body.get_rect(center=self.center)
        except:
            self.mickey_body = None

        # Hands
        self.min_hand_orig = pygame.image.load(os.path.join(img_dir, "right_hand.png")).convert_alpha()
        self.min_hand_orig = pygame.transform.scale(self.min_hand_orig, (200, 300))

        self.sec_hand_orig = pygame.image.load(os.path.join(img_dir, "left_hand.png")).convert_alpha()
        self.sec_hand_orig = pygame.transform.scale(self.sec_hand_orig, (190, 280))

    def blit_rotate_pivot(self, surface, image, pos, origin, angle):
        image_rect = image.get_rect(topleft=(pos[0] - origin[0], pos[1] - origin[1]))
        offset = pygame.math.Vector2(pos) - image_rect.center
        rotated_offset = offset.rotate(-angle)
        rotated_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rect = rotated_image.get_rect(center=rotated_center)

        surface.blit(rotated_image, rotated_rect)

    def render(self, surface):
        surface.blit(self.bg, (0, 0))

        if self.mickey_body:
            surface.blit(self.mickey_body, self.mickey_rect.topleft)

        now = datetime.datetime.now()

        sec_angle = -now.second * 6
        min_angle = -now.minute * 6

        # pivot points
        min_pivot = (self.min_hand_orig.get_width() // 2,
                     self.min_hand_orig.get_height())

        sec_pivot = (self.sec_hand_orig.get_width() // 2,
                     self.sec_hand_orig.get_height())

        # draw hands
        self.blit_rotate_pivot(surface, self.min_hand_orig, self.center, min_pivot, min_angle)
        self.blit_rotate_pivot(surface, self.sec_hand_orig, self.center, sec_pivot, sec_angle)