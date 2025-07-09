from dataclasses import dataclass, field

VX_REGISTER_COUNT = 16

@dataclass
class ChipEmu:
    # Program Counter "pseudo-register" (Python uses int to define every base)
    # Defines current instruction to execute
    pc: int = 0x200

    # Memory Index Register
    i: int = 0x0000

    # General Purpose 8-bit registers stored as a dictionary
    # vf register stored here as well, flag for some instructions
    vx: dict = field(default_factory = lambda: {f"v{hex(i)[-1]}": 0x00 for i in range(VX_REGISTER_COUNT)})

    memory: bytearray = field(default_factory = lambda: bytearray(4096))
    display: list = field(default_factory = lambda: [[0] * 64 for _ in range(32)])
    draw_flag: bool = False

# Helper to format hex with lowercase '0x' and uppercase digits
def hex_upper(val: int, length: int) -> str:
    return f"0x{val:0{length}X}"

def update(state: ChipEmu):
    state.pc += 2

def chip8(state: ChipEmu, opcode: int):

    match (opcode):
        case (0x00E0):
            state.display = [[0] * 64 for _ in range(32)]
            state.draw_flag = True
            print("Screen Cleared")

        case (0x00EE):
            print("Exited Subroutine")

        case pc if (pc & 0xF000) == 0x1000:
            state.pc = opcode & 0x0FFF
            print(f"Jumped to Instruction {hex_upper(state.pc, 3)}")
        
        case pc if (pc & 0xF000) == 0x6000:
            VX_REGISTER = f"v{(pc & 0x0F00) >> 8:x}"
            state.vx[VX_REGISTER] = pc & 0x00FF
            print(f"Placed Value {hex_upper(state.vx[VX_REGISTER], 2)} in register {VX_REGISTER}")

        case pc if (pc & 0xF000) == 0x7000:
            VX_REGISTER = f"v{(pc & 0x0F00) >> 8:x}"
            state.vx[VX_REGISTER] += (pc & 0x00FF)
            state.vx[VX_REGISTER] &= 0xFF
            print(f"Value {hex_upper(state.vx[VX_REGISTER], 2)} in register {VX_REGISTER}")

        case pc if (pc & 0xF000) == 0xA000:
            state.i = pc & 0x0FFF
            print(f"Stored Value {hex_upper(state.i, 4)} in register I")

        case pc if (pc & 0xF000) == 0xD000:
            VX_REGISTER_X = f"v{(pc & 0x0F00) >> 8:x}"
            VX_REGISTER_Y = f"v{(pc & 0x00F0) >> 4:x}"
            BYTES_TO_DRAW = f"{(pc & 0x000F)}"

            x = state.vx[VX_REGISTER_X] % 64
            y = state.vx[VX_REGISTER_Y] % 32

            state.vx["vf"] = 0

            for row in range(int(BYTES_TO_DRAW)):
                sprite_byte = state.memory[state.i + row]
                for col in range(8):
                    sprite_pixel = (sprite_byte >> (7 - col)) & 1
                    screen_x = (x + col) % 64
                    screen_y = (y + row) % 32

                    current_pixel = state.display[screen_y][screen_x]
                    new_pixel = current_pixel ^ sprite_pixel
                    state.display[screen_y][screen_x] = new_pixel

                    if current_pixel == 1 and sprite_pixel == 1:
                        state.vx["vf"] = 1
                        
            state.draw_flag = True

            print(f"Drew {BYTES_TO_DRAW}-byte sprite at memory location I at {hex_upper(state.vx[VX_REGISTER_X], 2)}, {hex_upper(state.vx[VX_REGISTER_Y], 2)}")
        
        case _:
            print("Unimplemented Opcode")