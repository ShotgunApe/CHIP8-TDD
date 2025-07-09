from dataclasses import dataclass

@dataclass
class ChipEmu:
    # Program Counter "pseudo-register" (Python uses int to define every base)
    # Defines current instruction to execute
    pc: int = 0x0000

    

def chip8(state: ChipEmu):
    match (state.pc):
        case (0x00E0):
            return "Screen Cleared"

        case (0x00EE):
            return "Exited Subroutine"

        case pc if (pc & 0xF000) == 0x1000:
            # Mask address from PC
            state.pc = state.pc & 0xFFF
            return f"Jumped to Instruction 0x{state.pc:03X}"