# DEPRECATED TESTS - USED FOR INITIAL DEVELOPMENT

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

    def test_InputANNN_OutputStoredMemoryAddress(self):
        emu = chip8.ChipEmu()
        emu.pc = 0xA0E0
        self.assertEqual(chip8.chip8(emu), "Stored Value 0x00E0 in register I")

        emu.pc = 0xAF30
        self.assertEqual(chip8.chip8(emu), "Stored Value 0x0F30 in register I")

    def test_InputDXYN_Output(self):
        emu = chip8.ChipEmu()
        emu.pc = 0xD012
        emu.vx['v0'] = 0x04
        emu.vx['v1'] = 0x03
        self.assertEqual(chip8.chip8(emu), "Drew 2-byte sprite at memory location I at 0x04, 0x03")

        emu.pc = 0xD4EA
        emu.vx['v4'] = 0xAF
        emu.vx['ve'] = 0x27
        self.assertEqual(chip8.chip8(emu), "Drew 10-byte sprite at memory location I at 0xAF, 0x27")


if __name__ == "__main__":
    unittest.main()