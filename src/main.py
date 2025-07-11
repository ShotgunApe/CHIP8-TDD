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

    emu = chip8.ChipEmu()
    running = True

    screen.fill("black")
    pygame.display.flip()

    with open('../roms/ibm.ch8', 'rb') as f:
        rom_data = f.read()
        for i in range(len(rom_data)):
            emu.memory[START_INSTRUCTION + i] = rom_data[i]

    while running:
        # Check for Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get opcode
        opcode = (emu.memory[emu.pc] << 8) | emu.memory[emu.pc + 1]

        # Change State
        chip8.chip8(emu, opcode)

        # Tick
        if opcode & 0xF000 != 0x1000:
            chip8.update(emu)

        if emu.draw_flag:
            screen.fill("Black")
            for y in range(32):
                for x in range(64):
                    if emu.display[y][x]:
                        rect = pygame.Rect(x * SCALE, y * SCALE, SCALE, SCALE)
                        pygame.draw.rect(screen, (255, 255, 255), rect)
            emu.draw_flag = False
        
        pygame.display.flip()
        clock.tick(60)  # limits FPS to 60
        
if __name__ == "__main__":
    main()