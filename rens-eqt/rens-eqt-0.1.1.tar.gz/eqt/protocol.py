from paillier.crypto import decrypt, encrypt

from eqt.util.exceptions import ProtocolError
from eqt.party_a import PartyA
from eqt.party_b import PartyB
from eqt.util.log import logger


class Protocol:
    def __init__(self, a, b, length, kappa):
        self.__a = a
        self.__b = b
        self._l = length
        self._kappa = kappa
        self._setup()

    def _setup(self):
        self.party_b = PartyB(k=self._kappa, length=self._l)

        a = encrypt(self.party_b.pk, self.__a)
        b = encrypt(self.party_b.pk, self.__b)

        logger.debug('[a]: %s, [b]: %s, l: %s', a, b, self._l)
        logger.debug('a: %s, b: %s', self.__a, self.__b)

        self.party_a = PartyA(self.party_b.pk, a, b, self._l, self._kappa)

    def start(self):
        logger.debug('Starting protocol')
        self._step1()
        self._step2()
        self._step3()
        self._step4()
        self._coinsteps()
        self._step12()
        self._step13()
        self._step14()
        self._step15()

    @property
    def result(self):
        result = self.party_a.curly_theta
        if result is None:
            raise ProtocolError("Start hasn't been called or protocol failed")
        return result

    @property
    def decrypted_result(self):
        return decrypt(self.party_b.pk, self.party_b.sk, self.result)

    def validate_outcome(self):
        outcome = bool(self.decrypted_result)
        equality = self.__a == self.__b
        if outcome != equality:
            logger.error(f"Equality was {equality} but protocol said it was {outcome}")

    def _step1(self):
        self.party_a.generate_r()
        self.party_b.x = self.party_a.x
        logger.debug('[x]: %s', self.party_b.x)

    def _step2(self):
        self.party_a.xis = self.party_b.xis
        logger.debug('[xi]: %s', self.party_a.xis)

    def _step3(self):
        self.party_a.compute_xor()
        logger.debug('[ri xor xi]: %s', self.party_a.xors)

    def _step4(self):
        self.party_a.determine_delta()

    def _coinsteps(self):
        self.party_a.compute_cis()

    def _step12(self):
        logger.debug('[ci] (before shuffle): %s', self.party_a.cis)
        self.party_a.shuffle_cis()
        self.party_b.cis = self.party_a.cis
        logger.debug('[ci] (after shuffle): %s', self.party_a.cis)

    def _step13(self):
        pass

    def _step14(self):
        self.party_a.delta_b = self.party_b.delta

    def _step15(self):
        pass
