#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Roberto Preste
import random

from Bio.Data.IUPACData import (
    ambiguous_dna_letters, extended_dna_letters, unambiguous_dna_letters
)


class BioFaker:

    _dna_alphabets = {
        "ambiguous": ambiguous_dna_letters,
        "extended": extended_dna_letters,
        "unambiguous": unambiguous_dna_letters,
    }

    def dna(self,
            length: int = 10,
            alphabet: str = "unambiguous") -> str:
        """ Create a random DNA sequence.

        Args:
            length: length of the sequence
            alphabet: alphabet to use [ambiguous, extended, unambiguous]

        Returns:
            sequence: random DNA sequence.
        """
        if alphabet not in ["ambiguous", "extended", "unambiguous"]:
            raise ValueError("Alphabet not valid.")

        letters = self._dna_alphabets[alphabet]

        sequence_lst = [random.choice(letters) for _ in range(length)]
        sequence = "".join(sequence_lst)
        return sequence
