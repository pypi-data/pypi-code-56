from .types import *
POK = Instruction(
        'POK',
        0x00,
        [
            Argument('value', BYTE),
            Argument('location', PTR),
        ]
    )

DEL = Instruction(
        'DEL',
        0x02,
        [
            Argument('time', LONG),
        ]
    )

JMP = Instruction(
        'JMP',
        0x04,
        [
            Argument('location', PTR),
            Argument('saveip', BYTE),
        ]
    )

ADB = Instruction(
        'ADB',
        0x05,
        [
            Argument('location', PTR),
            Argument('value', BYTE),
        ]
    )

ADI = Instruction(
        'ADI',
        0x06,
        [
            Argument('location', PTR),
            Argument('value', INT),
        ]
    )

ADL = Instruction(
        'ADL',
        0x07,
        [
            Argument('location', PTR),
            Argument('value', LONG),
        ]
    )

JEB = Instruction(
        'JEB',
        0x08,
        [
            Argument('target', PTR),
            Argument('check', PTR),
            Argument('value', BYTE),
            Argument('saveip', BYTE),
        ]
    )

JLB = Instruction(
        'JLB',
        0x09,
        [
            Argument('target', PTR),
            Argument('check', PTR),
            Argument('value', BYTE),
            Argument('saveip', BYTE),
        ]
    )

JGB = Instruction(
        'JGB',
        0x0A,
        [
            Argument('target', PTR),
            Argument('check', PTR),
            Argument('value', BYTE),
            Argument('saveip', BYTE),
        ]
    )

JEI = Instruction(
        'JEI',
        0x0B,
        [
            Argument('target', PTR),
            Argument('check', PTR),
            Argument('value', INT),
            Argument('saveip', BYTE),
        ]
    )

JLI = Instruction(
        'JLI',
        0x0C,
        [
            Argument('target', PTR),
            Argument('check', PTR),
            Argument('value', INT),
            Argument('saveip', BYTE),
        ]
    )

JGI = Instruction(
        'JGI',
        0x0D,
        [
            Argument('target', PTR),
            Argument('check', PTR),
            Argument('value', INT),
            Argument('saveip', BYTE),
        ]
    )

SCW = Instruction(
        'SCW',
        0x0E,
        [
            Argument('x', BYTE),
            Argument('y', BYTE),
        ]
    )

SCB = Instruction(
        'SCB',
        0x0F,
        [
            Argument('x', BYTE),
            Argument('y', BYTE),
        ]
    )

HLT = Instruction(
        'HLT',
        0x10,
        [
        ]
    )

SCF = Instruction(
        'SCF',
        0x11,
        [
        ]
    )

SBB = Instruction(
        'SBB',
        0x12,
        [
            Argument('location', PTR),
            Argument('value', BYTE),
        ]
    )

GBD = Instruction(
        'GBD',
        0x13,
        [
            Argument('button', BYTE),
            Argument('location', PTR),
        ]
    )

RET = Instruction(
        'RET',
        0x14,
        [
        ]
    )

REB = Instruction(
        'REB',
        0x15,
        [
            Argument('check', PTR),
            Argument('value', BYTE),
        ]
    )

RLB = Instruction(
        'RLB',
        0x16,
        [
            Argument('check', PTR),
            Argument('value', BYTE),
        ]
    )

RGB = Instruction(
        'RGB',
        0x17,
        [
            Argument('check', PTR),
            Argument('value', BYTE),
        ]
    )

SCT = Instruction(
        'SCT',
        0x18,
        [
            Argument('x', BYTE),
            Argument('y', BYTE),
            Argument('char', BYTE),
        ]
    )

DUB = Instruction(
        'DUB',
        0x19,
        [
            Argument('value', PTR),
            Argument('start', PTR),
        ]
    )

MOV = Instruction(
        'MOV',
        0x1A,
        [
            Argument('src', PTR),
            Argument('dest', PTR),
        ]
    )

SCS = Instruction(
        'SCS',
        0x1B,
        [
            Argument('x', BYTE),
            Argument('y', BYTE),
            Argument('charstart', BYTE),
        ]
    )

SCC = Instruction(
        'SCC',
        0x1C,
        [
            Argument('x', BYTE),
            Argument('y', BYTE),
            Argument('width', BYTE),
            Argument('height', BYTE),
        ]
    )

instructions = {
        0x00: POK,
        0x02: DEL,
        0x04: JMP,
        0x05: ADB,
        0x06: ADI,
        0x07: ADL,
        0x08: JEB,
        0x09: JLB,
        0x0A: JGB,
        0x0B: JEI,
        0x0C: JLI,
        0x0D: JGI,
        0x0E: SCW,
        0x0F: SCB,
        0x10: HLT,
        0x11: SCF,
        0x12: SBB,
        0x13: GBD,
        0x14: RET,
        0x15: REB,
        0x16: RLB,
        0x17: RGB,
        0x18: SCT,
        0x19: DUB,
        0x1A: MOV,
        0x1B: SCS,
        0x1C: SCC,
}
