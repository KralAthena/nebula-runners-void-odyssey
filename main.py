import pygame
import sys
import os
from src.utils.constants import WIDTH, HEIGHT, FPS
from src.core.state_manager import GameStateMachine

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("NEBULA RUNNERS: VOID ODYSSEY - v1.0")
    clock = pygame.time.Clock()

    # Asset dizin kontrolü
    if not os.path.exists("assets/images"):
        os.makedirs("assets/images", exist_ok=True)

    state_manager = GameStateMachine(screen)

    running = True
    while running:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            state_manager.handle_event(event)

        # Logic Update
        state_manager.update()

        # Render
        state_manager.draw()
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()