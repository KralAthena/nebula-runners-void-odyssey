import pygame
import math
import random
import os
from src.utils.constants import CLASS_COLORS, ISO_WIDTH, ISO_HEIGHT, OFFSET_X, OFFSET_Y, MAX_HP, MAX_AMMO

class Player:
    def __init__(self, name, p_class):
        self.name = name
        self.p_class = p_class
        self.color = CLASS_COLORS[p_class]
        self.pos_coord = [0, 0]
        self.visual_pos = [0, 0] 
        self.hp = MAX_HP
        self.ammo = MAX_AMMO
        self.keys = 0
        self.is_dead = False
        self.bobbing = random.uniform(0, 6.28)
        self.sprite = self.load_sprite()
        self.is_moving = False

    def load_sprite(self):
        try:
            path = os.path.join("assets", "images", f"{self.p_class.lower()}_character_icon.png")
            img = pygame.image.load(path).convert_alpha()
            img.set_colorkey((255, 255, 255))
            return pygame.transform.scale(img, (80, 80))
        except:
            surf = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(surf, self.color, (20, 20), 18)
            return surf

    def update(self):
        target_r, target_c = self.pos_coord
        self.visual_pos[0] += (target_r - self.visual_pos[0]) * 0.15
        self.visual_pos[1] += (target_c - self.visual_pos[1]) * 0.15
        
        self.bobbing += 0.08

    def get_iso_coords(self):
        r, c = self.visual_pos
        cart_x = (c - r) * (ISO_WIDTH / 2)
        cart_y = (c + r) * (ISO_HEIGHT / 2)
        return OFFSET_X + cart_x, OFFSET_Y + cart_y - 25

    def draw(self, canvas):
        if self.is_dead: return
        cx, cy = self.get_iso_coords()
        bob_y = math.sin(self.bobbing) * 8
        
        rect = self.sprite.get_rect(center=(cx, cy + bob_y))
        canvas.blit(self.sprite, rect)
        
        bar_w = 40
        pygame.draw.rect(canvas, (50, 0, 0), (int(cx - 20), int(cy - 50), bar_w, 5))
        pygame.draw.rect(canvas, (0, 255, 0), (int(cx - 20), int(cy - 50), int(bar_w * (self.hp/MAX_HP)), 5))

    def move_to(self, r, c):
        self.pos_coord = [r, c]
