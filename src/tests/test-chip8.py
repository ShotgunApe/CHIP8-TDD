import unittest
import sys

sys.path.append('../components/')

import chip8

class TestChip8Instructions(unittest.TestCase):

    def test_Input00E0_OutputClearScreen(self):
        emu = chip8.ChipEmu()
        emu.pc = 0x00E0
        self.assertEqual(chip8.chip8(emu), "Screen Cleared")

    def test_Input00EE_OutputExitSubroutine(self):
        emu = chip8.ChipEmu()
        emu.pc = 0x00EE
        self.assertEqual(chip8.chip8(emu), "Exited Subroutine")

    def test_Input1NNN_OutputJumpedInstruction(self):
        emu = chip8.ChipEmu()
        emu.pc = 0x1ABF
        self.assertEqual(chip8.chip8(emu), "Jumped to Instruction 0xABF")

        emu.pc = 0x1000
        self.assertEqual(chip8.chip8(emu), "Jumped to Instruction 0x000")

        emu.pc = 0x1FFF
        self.assertEqual(chip8.chip8(emu), "Jumped to Instruction 0xFFF")

    def test_Input6XNN_OutputSetRegister(self):
        emu = chip8.ChipEmu()
        emu.pc = 0x6A00
        self.assertEqual(chip8.chip8(emu), "Placed Value 0x00 in register va")

        emu.pc = 0x60F5
        self.assertEqual(chip8.chip8(emu), "Placed Value 0xF5 in register v0")

    def test_Input7XNN_OutputAddedRegister(self):
        emu = chip8.ChipEmu()
        emu.pc = 0x72AA
        self.assertEqual(chip8.chip8(emu), "Value 0xAA in register v2")

        emu.pc = 0x7A99
        self.assertEqual(chip8.chip8(emu), "Value 0x99 in register va")


if __name__ == "__main__":
    unittest.main()