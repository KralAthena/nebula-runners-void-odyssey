import pygame
import random
import os
import math
from src.utils.constants import ISO_WIDTH, ISO_HEIGHT, OFFSET_X, OFFSET_Y, GRID_SIZE, COLOR_VOID

class Board:
    def __init__(self):
        self.grid_size = GRID_SIZE
        self.tiles = self.generate_grid()
        self.tile_img = self.load_tile()
        self.pod_img = self.load_img("pod.png", (180, 180))
        self.key_imgs = [self.load_img("key_1.png", (50, 50)), self.load_img("key_2.png", (50, 50))]
        self.void_level = 0
        self.keys_on_board = []
        self.spawn_keys()

    def load_tile(self):
        try:
            img = pygame.image.load("assets/images/iso_tile.png").convert_alpha()
            img.set_colorkey((255, 255, 255))
            return pygame.transform.scale(img, (ISO_WIDTH, ISO_HEIGHT + 20))
        except: return None

    def load_img(self, name, size):
        try:
            img = pygame.image.load(os.path.join("assets", "images", name)).convert_alpha()
            return pygame.transform.scale(img, size)
        except: return None

    def generate_grid(self):
        grid = {}
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                grid[(r, c)] = {"state": "NORMAL"}
        return grid

    def spawn_keys(self):
        for _ in range(4):
            r, c = random.randint(1, 10), random.randint(1, 10)
            if (r, c) != (5, 5) and (r, c) != (6, 6):
                self.keys_on_board.append([r, c, random.randint(0, 1)])

    def get_iso_coords(self, r, c):
        cart_x = (c - r) * (ISO_WIDTH // 2)
        cart_y = (c + r) * (ISO_HEIGHT // 2)
        return OFFSET_X + cart_x, OFFSET_Y + cart_y

    def advance_void(self):
        self.void_level += 1
        for (r, c) in self.tiles:
            dist = min(r, c, self.grid_size - 1 - r, self.grid_size - 1 - c)
            if dist < self.void_level:
                self.tiles[(r, c)]["state"] = "VOID"

    def draw(self, canvas, font_small):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                state = self.tiles[(r, c)]["state"]
                if state == "VOID":
                    x_void, y_void = self.get_iso_coords(r, c)
                    void_surf = pygame.Surface((ISO_WIDTH, ISO_HEIGHT + 10), pygame.SRCALPHA)
                    pygame.draw.polygon(
                        void_surf,
                        (40, 0, 70, 160),
                        [
                            (ISO_WIDTH // 2, 0),
                            (ISO_WIDTH, ISO_HEIGHT // 2),
                            (ISO_WIDTH // 2, ISO_HEIGHT),
                            (0, ISO_HEIGHT // 2),
                        ],
                    )
                    canvas.blit(void_surf, (int(x_void - ISO_WIDTH // 2), int(y_void)))
                    continue
                
                x, y = self.get_iso_coords(r, c)
                
                dist = min(r, c, self.grid_size - 1 - r, self.grid_size - 1 - c)
                offset_v = 0
                if dist == self.void_level:
                    offset_v = int(math.sin(pygame.time.get_ticks() * 0.05) * 2)
                    pygame.draw.circle(canvas, (255, 0, 0, 100), (int(x), int(y + 20)), 40, 2)

                if self.tile_img:
                    canvas.blit(self.tile_img, (int(x - ISO_WIDTH//2), int(y + offset_v)))
                else:
                    tile_surf = pygame.Surface((ISO_WIDTH, ISO_HEIGHT + 10), pygame.SRCALPHA)
                    pygame.draw.polygon(
                        tile_surf,
                        (25, 40 + dist * 5, 70 + dist * 5, 220),
                        [
                            (ISO_WIDTH // 2, 0),
                            (ISO_WIDTH, ISO_HEIGHT // 2),
                            (ISO_WIDTH // 2, ISO_HEIGHT),
                            (0, ISO_HEIGHT // 2),
                        ],
                    )
                    canvas.blit(tile_surf, (int(x - ISO_WIDTH // 2), int(y + offset_v)))
                
                if (r, c) == (self.grid_size // 2, self.grid_size // 2):
                    if self.pod_img:
                        canvas.blit(self.pod_img, (int(x - 90), int(y - 130)))
                    pygame.draw.circle(canvas, (0, 255, 255, 120), (int(x), int(y + 10)), 55, 3)
                
                for k in self.keys_on_board:
                    if k[0] == r and k[1] == c:
                        img = self.key_imgs[k[2]]
                        if img:
                            bob = int(math.sin(pygame.time.get_ticks() * 0.01) * 5)
                            canvas.blit(img, (int(x - 25), int(y - 40 + bob)))
