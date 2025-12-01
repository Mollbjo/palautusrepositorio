KAPASITEETTI = 5
OLETUSKASVATUS = 5


class IntJoukko:
    def _luo_lista(self, koko):
        return [0] * koko
    
    def __init__(self, kapasiteetti=None, kasvatuskoko=None):
        if kapasiteetti is None:
            self.kapasiteetti = KAPASITEETTI
        elif not isinstance(kapasiteetti, int) or kapasiteetti < 0:
            raise Exception("Väärä kapasiteetti")
        else:
            self.kapasiteetti = kapasiteetti

        if kasvatuskoko is None:
            self.kasvatuskoko = OLETUSKASVATUS
        elif not isinstance(kasvatuskoko, int) or kasvatuskoko < 0:
            raise Exception("Väärä kasvatuskoko")
        else:
            self.kasvatuskoko = kasvatuskoko

        self.ljono = self._luo_lista(self.kapasiteetti)
        self.alkioiden_lkm = 0

    def _find_index(self, arvo):
        for i in range(self.alkioiden_lkm):
            if self.ljono[i] == arvo:
                return i
        return -1

    def _ensure_capacity(self):
        if self.alkioiden_lkm < len(self.ljono):
            return
        uusi_koko = self.alkioiden_lkm + self.kasvatuskoko
        uusi = self._luo_lista(uusi_koko)
        for i in range(self.alkioiden_lkm):
            uusi[i] = self.ljono[i]
        self.ljono = uusi

    def kuuluu_listaan(self, n):
        return self._find_index(n) != -1

    def lisaa_listaan(self, n):
        if self.kuuluu_listaan(n):
            return False
        self._ensure_capacity()
        self.ljono[self.alkioiden_lkm] = n
        self.alkioiden_lkm += 1
        return True

    def poista_listasta(self, n):
        kohta = self._find_index(n)
        if kohta == -1:
            return False
        for i in range(kohta, self.alkioiden_lkm - 1):
            self.ljono[i] = self.ljono[i + 1]
        self.alkioiden_lkm -= 1
        self.ljono[self.alkioiden_lkm] = 0
        return True

    def kopioi_lista(self, a, b):
        maara = min(len(a), len(b))
        for i in range(maara):
            b[i] = a[i]

    def listan_suuruus(self):
        return self.alkioiden_lkm

    def to_int_list(self):
        taulu = self._luo_lista(self.alkioiden_lkm)
        for i in range(self.alkioiden_lkm):
            taulu[i] = self.ljono[i]
        return taulu

    def __str__(self):
        if self.alkioiden_lkm == 0:
            return "{}"
        sisalto = ", ".join(str(x) for x in self.ljono[: self.alkioiden_lkm])
        return "{" + sisalto + "}"

    @staticmethod
    def yhdiste(a, b):
        tulos = IntJoukko()
        for arvo in a.to_int_list():
            tulos.lisaa_listaan(arvo)
        for arvo in b.to_int_list():
            tulos.lisaa_listaan(arvo)
        return tulos

    @staticmethod
    def leikkaus(a, b):
        tulos = IntJoukko()
        b_arvot = b.to_int_list()
        for arvo in a.to_int_list():
            if arvo in b_arvot:
                tulos.lisaa_listaan(arvo)
        return tulos

    @staticmethod
    def erotus(a, b):
        tulos = IntJoukko()
        for arvo in a.to_int_list():
            tulos.lisaa_listaan(arvo)
        for arvo in b.to_int_list():
            tulos.poista_listasta(arvo)
        return tulos
