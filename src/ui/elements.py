import pygame
from src.utils.constants import COLOR_ACCENT, COLOR_BG

class UIButton:
    def __init__(self, x, y, w, h, text, font, color, action=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.color = color
        self.hovered = False
        self.action = action
        self.clicked = False

    def draw(self, screen):
        draw_color = tuple(min(255, c + 50) for c in self.color) if self.hovered else self.color
        
        glow_rect = self.rect.inflate(6, 6)
        pygame.draw.rect(screen, (0, 0, 0, 150), glow_rect, border_radius=10)
        
        pygame.draw.rect(screen, (20, 20, 40), self.rect, border_radius=8)
        pygame.draw.rect(screen, draw_color, self.rect, width=2, border_radius=8)
        
        txt = self.font.render(self.text, True, draw_color)
        t_rect = txt.get_rect(center=self.rect.center)
        screen.blit(txt, t_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                self.clicked = True
        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.hovered and self.clicked:
                if self.action: 
                    self.action()
            self.clicked = False

class ProgressBar:
    def __init__(self, x, y, w, h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.progress = 1.0

    def draw(self, screen, current, maximum):
        self.progress = max(0, min(1, current / maximum))
        pygame.draw.rect(screen, (30, 30, 50), self.rect, border_radius=5)
        fill_w = self.rect.width * self.progress
        if fill_w > 0:
            pygame.draw.rect(screen, self.color, (self.rect.x, self.rect.y, fill_w, self.rect.height), border_radius=5)

class GameLog:
    def __init__(self, x, y, font):
        self.x = x
        self.y = y
        self.font = font
        self.messages = []

    def add_message(self, text, color=(255, 255, 255)):
        self.messages.append({"text": text, "color": color, "alpha": 255})
        if len(self.messages) > 8:
            self.messages.pop(0)

    def draw(self, screen):
        for i, m in enumerate(self.messages):
            alpha_surf = self.font.render(m["text"], True, m["color"])
            alpha_surf.set_alpha(m["alpha"])
            screen.blit(alpha_surf, (self.x, self.y + i * 25))
            m["alpha"] = max(0, m["alpha"] - 0.5)
