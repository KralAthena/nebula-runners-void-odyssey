import pygame
import random
from src.utils.constants import WIDTH, HEIGHT

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.canvas = pygame.Surface((WIDTH, HEIGHT))
        self.shake_amount = 0
        self.shake_decay = 0.9

    def start_frame(self, bg_color=(2, 2, 8)):
        self.canvas.fill(bg_color)

    def trigger_shake(self, amount=5):
        self.shake_amount = amount

    def end_frame(self):
        offset_x = 0
        offset_y = 0
        if self.shake_amount > 0.1:
            offset_x = random.uniform(-self.shake_amount, self.shake_amount)
            offset_y = random.uniform(-self.shake_amount, self.shake_amount)
            self.shake_amount *= self.shake_decay
        
        self.screen.blit(self.canvas, (offset_x, offset_y))
        pygame.display.flip()

    def draw_on_canvas(self, drawable, *args):
        drawable.draw(self.canvas, *args)
