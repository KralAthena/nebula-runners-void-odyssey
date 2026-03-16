import pygame
from collections import deque

class InputHandler:
    def __init__(self):
        self.buffer = deque(maxlen=1)
        self.key_map = {
            pygame.K_w: "UP",
            pygame.K_s: "DOWN",
            pygame.K_a: "LEFT",
            pygame.K_d: "RIGHT",
            pygame.K_SPACE: "ACTION",
            pygame.K_ESCAPE: "BACK",
            pygame.K_h: "HELP"
        }

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.key_map:
                cmd = self.key_map[event.key]
                self.buffer.append(cmd)
                return cmd
        return None

    def get_next_command(self):
        if self.buffer:
            return self.buffer.popleft()
        return None

    def clear(self):
        self.buffer.clear()
