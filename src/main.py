import sys
import pygame

sys.path.append('components/')
import chip8

SCALE = 16
START_INSTRUCTION = 0x200

def main():

    pygame.init()
    screen = pygame.display.set_mode((64 * SCALE, 32 * SCALE))
    clock = pygame.time.Clock()

    emu = chip8.ChipEmu(pc = START_INSTRUCTION)
    running = True

    screen.fill("black")
    pygame.display.flip()

    while running:
        # Check for Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Change State
        chip8.chip8(emu)

        # Tick
        chip8.update(emu)
        pygame.display.flip()
        clock.tick(60)  # limits FPS to 60
        
if __name__ == "__main__":
    main()