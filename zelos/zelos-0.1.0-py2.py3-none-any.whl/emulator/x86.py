# Copyright (C) 2020 Zeropoint Dynamics

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.
# ======================================================================
import unicorn.x86_const as uc

from zelos.emulator.base import IEmuHelper


REGMAP = {
    "ah": uc.UC_X86_REG_AH,
    "al": uc.UC_X86_REG_AL,
    "ax": uc.UC_X86_REG_AX,
    "bh": uc.UC_X86_REG_BH,
    "bl": uc.UC_X86_REG_BL,
    "bp": uc.UC_X86_REG_BP,
    "bpl": uc.UC_X86_REG_BPL,
    "bx": uc.UC_X86_REG_BX,
    "ch": uc.UC_X86_REG_CH,
    "cl": uc.UC_X86_REG_CL,
    "cs": uc.UC_X86_REG_CS,
    "cx": uc.UC_X86_REG_CX,
    "dh": uc.UC_X86_REG_DH,
    "di": uc.UC_X86_REG_DI,
    "dil": uc.UC_X86_REG_DIL,
    "dl": uc.UC_X86_REG_DL,
    "ds": uc.UC_X86_REG_DS,
    "dx": uc.UC_X86_REG_DX,
    "eax": uc.UC_X86_REG_EAX,
    "ebp": uc.UC_X86_REG_EBP,
    "ebx": uc.UC_X86_REG_EBX,
    "ecx": uc.UC_X86_REG_ECX,
    "edi": uc.UC_X86_REG_EDI,
    "edx": uc.UC_X86_REG_EDX,
    "flags": uc.UC_X86_REG_EFLAGS,
    "eip": uc.UC_X86_REG_EIP,
    "eiz": uc.UC_X86_REG_EIZ,
    "es": uc.UC_X86_REG_ES,
    "esi": uc.UC_X86_REG_ESI,
    "esp": uc.UC_X86_REG_ESP,
    "fpsw": uc.UC_X86_REG_FPSW,
    "fs": uc.UC_X86_REG_FS,
    "gs": uc.UC_X86_REG_GS,
    "ip": uc.UC_X86_REG_IP,
    "rax": uc.UC_X86_REG_RAX,
    "rbp": uc.UC_X86_REG_RBP,
    "rbx": uc.UC_X86_REG_RBX,
    "rcx": uc.UC_X86_REG_RCX,
    "rdi": uc.UC_X86_REG_RDI,
    "rdx": uc.UC_X86_REG_RDX,
    "rip": uc.UC_X86_REG_RIP,
    "riz": uc.UC_X86_REG_RIZ,
    "rsi": uc.UC_X86_REG_RSI,
    "rsp": uc.UC_X86_REG_RSP,
    "si": uc.UC_X86_REG_SI,
    "sil": uc.UC_X86_REG_SIL,
    "sp": uc.UC_X86_REG_SP,
    "spl": uc.UC_X86_REG_SPL,
    "ss": uc.UC_X86_REG_SS,
    "cr0": uc.UC_X86_REG_CR0,
    "cr1": uc.UC_X86_REG_CR1,
    "cr2": uc.UC_X86_REG_CR2,
    "cr3": uc.UC_X86_REG_CR3,
    "cr4": uc.UC_X86_REG_CR4,
    "cr5": uc.UC_X86_REG_CR5,
    "cr6": uc.UC_X86_REG_CR6,
    "cr7": uc.UC_X86_REG_CR7,
    "cr8": uc.UC_X86_REG_CR8,
    "cr9": uc.UC_X86_REG_CR9,
    "cr10": uc.UC_X86_REG_CR10,
    "cr11": uc.UC_X86_REG_CR11,
    "cr12": uc.UC_X86_REG_CR12,
    "cr13": uc.UC_X86_REG_CR13,
    "cr14": uc.UC_X86_REG_CR14,
    "cr15": uc.UC_X86_REG_CR15,
    "dr0": uc.UC_X86_REG_DR0,
    "dr1": uc.UC_X86_REG_DR1,
    "dr2": uc.UC_X86_REG_DR2,
    "dr3": uc.UC_X86_REG_DR3,
    "dr4": uc.UC_X86_REG_DR4,
    "dr5": uc.UC_X86_REG_DR5,
    "dr6": uc.UC_X86_REG_DR6,
    "dr7": uc.UC_X86_REG_DR7,
    "dr8": uc.UC_X86_REG_DR8,
    "dr9": uc.UC_X86_REG_DR9,
    "dr10": uc.UC_X86_REG_DR10,
    "dr11": uc.UC_X86_REG_DR11,
    "dr12": uc.UC_X86_REG_DR12,
    "dr13": uc.UC_X86_REG_DR13,
    "dr14": uc.UC_X86_REG_DR14,
    "dr15": uc.UC_X86_REG_DR15,
    "fp0": uc.UC_X86_REG_FP0,
    "fp1": uc.UC_X86_REG_FP1,
    "fp2": uc.UC_X86_REG_FP2,
    "fp3": uc.UC_X86_REG_FP3,
    "fp4": uc.UC_X86_REG_FP4,
    "fp5": uc.UC_X86_REG_FP5,
    "fp6": uc.UC_X86_REG_FP6,
    "fp7": uc.UC_X86_REG_FP7,
    "k0": uc.UC_X86_REG_K0,
    "k1": uc.UC_X86_REG_K1,
    "k2": uc.UC_X86_REG_K2,
    "k3": uc.UC_X86_REG_K3,
    "k4": uc.UC_X86_REG_K4,
    "k5": uc.UC_X86_REG_K5,
    "k6": uc.UC_X86_REG_K6,
    "k7": uc.UC_X86_REG_K7,
    "mm0": uc.UC_X86_REG_MM0,
    "mm1": uc.UC_X86_REG_MM1,
    "mm2": uc.UC_X86_REG_MM2,
    "mm3": uc.UC_X86_REG_MM3,
    "mm4": uc.UC_X86_REG_MM4,
    "mm5": uc.UC_X86_REG_MM5,
    "mm6": uc.UC_X86_REG_MM6,
    "mm7": uc.UC_X86_REG_MM7,
    "r8": uc.UC_X86_REG_R8,
    "r9": uc.UC_X86_REG_R9,
    "r10": uc.UC_X86_REG_R10,
    "r11": uc.UC_X86_REG_R11,
    "r12": uc.UC_X86_REG_R12,
    "r13": uc.UC_X86_REG_R13,
    "r14": uc.UC_X86_REG_R14,
    "r15": uc.UC_X86_REG_R15,
    "st(0)": uc.UC_X86_REG_ST0,
    "st(1)": uc.UC_X86_REG_ST1,
    "st(2)": uc.UC_X86_REG_ST2,
    "st(3)": uc.UC_X86_REG_ST3,
    "st(4)": uc.UC_X86_REG_ST4,
    "st(5)": uc.UC_X86_REG_ST5,
    "st(6)": uc.UC_X86_REG_ST6,
    "st(7)": uc.UC_X86_REG_ST7,
    "xmm0": uc.UC_X86_REG_XMM0,
    "xmm1": uc.UC_X86_REG_XMM1,
    "xmm2": uc.UC_X86_REG_XMM2,
    "xmm3": uc.UC_X86_REG_XMM3,
    "xmm4": uc.UC_X86_REG_XMM4,
    "xmm5": uc.UC_X86_REG_XMM5,
    "xmm6": uc.UC_X86_REG_XMM6,
    "xmm7": uc.UC_X86_REG_XMM7,
    "xmm8": uc.UC_X86_REG_XMM8,
    "xmm9": uc.UC_X86_REG_XMM9,
    "xmm10": uc.UC_X86_REG_XMM10,
    "xmm11": uc.UC_X86_REG_XMM11,
    "xmm12": uc.UC_X86_REG_XMM12,
    "xmm13": uc.UC_X86_REG_XMM13,
    "xmm14": uc.UC_X86_REG_XMM14,
    "xmm15": uc.UC_X86_REG_XMM15,
    "xmm16": uc.UC_X86_REG_XMM16,
    "xmm17": uc.UC_X86_REG_XMM17,
    "xmm18": uc.UC_X86_REG_XMM18,
    "xmm19": uc.UC_X86_REG_XMM19,
    "xmm20": uc.UC_X86_REG_XMM20,
    "xmm21": uc.UC_X86_REG_XMM21,
    "xmm22": uc.UC_X86_REG_XMM22,
    "xmm23": uc.UC_X86_REG_XMM23,
    "xmm24": uc.UC_X86_REG_XMM24,
    "xmm25": uc.UC_X86_REG_XMM25,
    "xmm26": uc.UC_X86_REG_XMM26,
    "xmm27": uc.UC_X86_REG_XMM27,
    "xmm28": uc.UC_X86_REG_XMM28,
    "xmm29": uc.UC_X86_REG_XMM29,
    "xmm30": uc.UC_X86_REG_XMM30,
    "xmm31": uc.UC_X86_REG_XMM31,
    "ymm0": uc.UC_X86_REG_YMM0,
    "ymm1": uc.UC_X86_REG_YMM1,
    "ymm2": uc.UC_X86_REG_YMM2,
    "ymm3": uc.UC_X86_REG_YMM3,
    "ymm4": uc.UC_X86_REG_YMM4,
    "ymm5": uc.UC_X86_REG_YMM5,
    "ymm6": uc.UC_X86_REG_YMM6,
    "ymm7": uc.UC_X86_REG_YMM7,
    "ymm8": uc.UC_X86_REG_YMM8,
    "ymm9": uc.UC_X86_REG_YMM9,
    "ymm10": uc.UC_X86_REG_YMM10,
    "ymm11": uc.UC_X86_REG_YMM11,
    "ymm12": uc.UC_X86_REG_YMM12,
    "ymm13": uc.UC_X86_REG_YMM13,
    "ymm14": uc.UC_X86_REG_YMM14,
    "ymm15": uc.UC_X86_REG_YMM15,
    "ymm16": uc.UC_X86_REG_YMM16,
    "ymm17": uc.UC_X86_REG_YMM17,
    "ymm18": uc.UC_X86_REG_YMM18,
    "ymm19": uc.UC_X86_REG_YMM19,
    "ymm20": uc.UC_X86_REG_YMM20,
    "ymm21": uc.UC_X86_REG_YMM21,
    "ymm22": uc.UC_X86_REG_YMM22,
    "ymm23": uc.UC_X86_REG_YMM23,
    "ymm24": uc.UC_X86_REG_YMM24,
    "ymm25": uc.UC_X86_REG_YMM25,
    "ymm26": uc.UC_X86_REG_YMM26,
    "ymm27": uc.UC_X86_REG_YMM27,
    "ymm28": uc.UC_X86_REG_YMM28,
    "ymm29": uc.UC_X86_REG_YMM29,
    "ymm30": uc.UC_X86_REG_YMM30,
    "ymm31": uc.UC_X86_REG_YMM31,
    "zmm0": uc.UC_X86_REG_ZMM0,
    "zmm1": uc.UC_X86_REG_ZMM1,
    "zmm2": uc.UC_X86_REG_ZMM2,
    "zmm3": uc.UC_X86_REG_ZMM3,
    "zmm4": uc.UC_X86_REG_ZMM4,
    "zmm5": uc.UC_X86_REG_ZMM5,
    "zmm6": uc.UC_X86_REG_ZMM6,
    "zmm7": uc.UC_X86_REG_ZMM7,
    "zmm8": uc.UC_X86_REG_ZMM8,
    "zmm9": uc.UC_X86_REG_ZMM9,
    "zmm10": uc.UC_X86_REG_ZMM10,
    "zmm11": uc.UC_X86_REG_ZMM11,
    "zmm12": uc.UC_X86_REG_ZMM12,
    "zmm13": uc.UC_X86_REG_ZMM13,
    "zmm14": uc.UC_X86_REG_ZMM14,
    "zmm15": uc.UC_X86_REG_ZMM15,
    "zmm16": uc.UC_X86_REG_ZMM16,
    "zmm17": uc.UC_X86_REG_ZMM17,
    "zmm18": uc.UC_X86_REG_ZMM18,
    "zmm19": uc.UC_X86_REG_ZMM19,
    "zmm20": uc.UC_X86_REG_ZMM20,
    "zmm21": uc.UC_X86_REG_ZMM21,
    "zmm22": uc.UC_X86_REG_ZMM22,
    "zmm23": uc.UC_X86_REG_ZMM23,
    "zmm24": uc.UC_X86_REG_ZMM24,
    "zmm25": uc.UC_X86_REG_ZMM25,
    "zmm26": uc.UC_X86_REG_ZMM26,
    "zmm27": uc.UC_X86_REG_ZMM27,
    "zmm28": uc.UC_X86_REG_ZMM28,
    "zmm29": uc.UC_X86_REG_ZMM29,
    "zmm30": uc.UC_X86_REG_ZMM30,
    "zmm31": uc.UC_X86_REG_ZMM31,
    "r8b": uc.UC_X86_REG_R8B,
    "r9b": uc.UC_X86_REG_R9B,
    "r10b": uc.UC_X86_REG_R10B,
    "r11b": uc.UC_X86_REG_R11B,
    "r12b": uc.UC_X86_REG_R12B,
    "r13b": uc.UC_X86_REG_R13B,
    "r14b": uc.UC_X86_REG_R14B,
    "r15b": uc.UC_X86_REG_R15B,
    "r8d": uc.UC_X86_REG_R8D,
    "r9d": uc.UC_X86_REG_R9D,
    "r10d": uc.UC_X86_REG_R10D,
    "r11d": uc.UC_X86_REG_R11D,
    "r12d": uc.UC_X86_REG_R12D,
    "r13d": uc.UC_X86_REG_R13D,
    "r14d": uc.UC_X86_REG_R14D,
    "r15d": uc.UC_X86_REG_R15D,
    "r8w": uc.UC_X86_REG_R8W,
    "r9w": uc.UC_X86_REG_R9W,
    "r10w": uc.UC_X86_REG_R10W,
    "r11w": uc.UC_X86_REG_R11W,
    "r12w": uc.UC_X86_REG_R12W,
    "r13w": uc.UC_X86_REG_R13W,
    "r14w": uc.UC_X86_REG_R14W,
    "r15w": uc.UC_X86_REG_R15W,
    "gdtr": uc.UC_X86_REG_GDTR,
}


class x86EmuHelper(IEmuHelper):
    ip_reg = "eip"
    sp_reg = "esp"
    fp_reg = "ebp"
    regmap = REGMAP

    imp_regs = [
        "eax",
        "ebx",
        "ecx",
        "edx",
        "esi",
        "edi",
        "ebp",
        "esp",
        "eip",
        "flags",
    ]

    def msr_read(self, msr_id):
        return self._uc.msr_read(msr_id)

    def msr_write(self, msr_id, value):
        return self._uc.msr_write(msr_id, value)


class x86_64EmuHelper(IEmuHelper):
    ip_reg = "rip"
    sp_reg = "rsp"
    fp_reg = "rbp"
    regmap = REGMAP

    imp_regs = [
        "rax",
        "rbx",
        "rcx",
        "rdx",
        "rsi",
        "rdi",
        "rbp",
        "rsp",
        "rip",
        "flags",
    ]

    def msr_read(self, msr_id):
        return self._uc.msr_read(msr_id)

    def msr_write(self, msr_id, value):
        return self._uc.msr_write(msr_id, value)
