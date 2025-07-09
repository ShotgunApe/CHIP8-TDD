from dataclasses import dataclass, field

VX_REGISTER_COUNT = 16

@dataclass
class ChipEmu:
    # Program Counter "pseudo-register" (Python uses int to define every base)
    # Defines current instruction to execute
    pc: int = 0x0000

    # Memory Index Register
    i: int = 0x0000

    # General Purpose 8-bit registers stored as a dictionary
    # vf register stored here as well, flag for some instructions
    vx: dict = field(default_factory = lambda: {f"v{hex(i)[-1]}": 0x00 for i in range(VX_REGISTER_COUNT)})

# Helper to format hex with lowercase '0x' and uppercase digits
def hex_upper(val: int, length: int) -> str:
    return f"0x{val:0{length}X}"

def chip8(state: ChipEmu):

    match (state.pc):
        case (0x00E0):
            return "Screen Cleared"

        case (0x00EE):
            return "Exited Subroutine"

        case pc if (pc & 0xF000) == 0x1000:
            state.pc = state.pc & 0x0FFF
            return f"Jumped to Instruction {hex_upper(state.pc, 3)}"
        
        case pc if (pc & 0xF000) == 0x6000:
            VX_REGISTER = f"v{(pc & 0x0F00) >> 8:x}"
            state.vx[VX_REGISTER] = pc & 0x00FF
            return f"Placed Value {hex_upper(state.vx[VX_REGISTER], 2)} in register {VX_REGISTER}"

        case pc if (pc & 0xF000) == 0x7000:
            VX_REGISTER = f"v{(pc & 0x0F00) >> 8:x}"
            state.vx[VX_REGISTER] += (pc & 0x00FF)
            state.vx[VX_REGISTER] &= 0xFF
            return f"Value {hex_upper(state.vx[VX_REGISTER], 2)} in register {VX_REGISTER}"

        case pc if (pc & 0xF000) == 0xA000:
            state.i = pc & 0x0FFF
            return f"Stored Value {hex_upper(state.i, 4)} in register I"

        case pc if (pc & 0xF000) == 0xD000:
            # Draw to screen - FIX
            VX_REGISTER_X = f"v{(pc & 0x0F00) >> 8:x}"
            VX_REGISTER_Y = f"v{(pc & 0x00F0) >> 4:x}"
            BYTES_TO_DRAW = f"{(pc & 0x000F)}"
            return f"Drew {BYTES_TO_DRAW}-byte sprite at memory location I at {hex_upper(state.vx[VX_REGISTER_X], 2)}, {hex_upper(state.vx[VX_REGISTER_Y], 2)}"