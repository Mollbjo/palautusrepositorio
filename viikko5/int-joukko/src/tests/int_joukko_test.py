import unittest
from int_joukko import IntJoukko


class TestIntJoukko(unittest.TestCase):
    def setUp(self):
        self.joukko = IntJoukko()
        self.joukko.lisaa_listaan(10)
        self.joukko.lisaa_listaan(3)

    def tee_joukko(self, *luvut):
        joukko = IntJoukko()

        for luku in luvut:
            joukko.lisaa_listaan(luku)

        return joukko

    def toimii_kasvatuksen_jalkeen(self, joukko):
        lisattavat = [1, 2, 4, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

        for luku in lisattavat:
            joukko.lisaa_listaan(luku)

        self.assertEqual(joukko.listan_suuruus(), 14)
        self.assertTrue(joukko.kuuluu_listaan(11))
        joukko.poista_listasta(11)
        self.assertFalse(joukko.kuuluu_listaan(11))
        self.assertEqual(joukko.listan_suuruus(), 13)

    def test_lukuja_lisatty_maara(self):
        self.joukko.lisaa_listaan(4)
        self.assertEqual(self.joukko.listan_suuruus(), 3)

    def test_sama_luku_menee_joukkoon_vaan_kerran(self):
        self.joukko.lisaa_listaan(10)
        self.joukko.lisaa_listaan(3)
        self.assertEqual(self.joukko.listan_suuruus(), 2)

    def test_vain_lisatyt_luvut_loytyvat(self):
        self.assertTrue(self.joukko.kuuluu_listaan(10))
        self.assertFalse(self.joukko.kuuluu_listaan(5))
        self.assertTrue(self.joukko.kuuluu_listaan(3))

    def test_poistettu_ei_ole_enaa_joukossa(self):
        self.joukko.poista_listasta(3)
        self.assertFalse(self.joukko.kuuluu_listaan(3))
        self.assertEqual(self.joukko.listan_suuruus(), 1)

    def test_palautetaan_oikea_taulukko(self):
        odotettu = [3, 55, 99]

        self.joukko.lisaa_listaan(55)
        self.joukko.poista_listasta(10)
        self.joukko.lisaa_listaan(99)

        vastaus = self.joukko.to_int_list()

        self.assertListEqual(sorted(vastaus), odotettu)

    def test_toimii_kasvatuksen_jalkeen(self):
        joukko_a = IntJoukko()
        joukko_b = IntJoukko(8)
        joukko_c = IntJoukko(10, 20)

        self.toimii_kasvatuksen_jalkeen(joukko_a)
        self.toimii_kasvatuksen_jalkeen(joukko_b)
        self.toimii_kasvatuksen_jalkeen(joukko_c)

    def test_merkkijonoesitys_toimii(self):
        self.assertEqual(str(self.joukko), "{10, 3}")

    def test_merkkijonoesitys_toimii_yhden_kokeisella_joukolla(self):
        joukko = IntJoukko()
        joukko.lisaa_listaan(1)
        self.assertEqual(str(joukko), "{1}")

    def test_merkkijonoesitys_toimii_tyhjalla_joukolla(self):
        joukko = IntJoukko()
        self.assertEqual(str(joukko), "{}")

    def test_yhdiste(self):
        eka = self.tee_joukko(1, 2)
        toka = self.tee_joukko(3, 4)

        tulos = IntJoukko.yhdiste(eka, toka)
        vastauksen_luvut = tulos.to_int_list()

        odotettu = [1, 2, 3, 4]

        self.assertListEqual(sorted(vastauksen_luvut), odotettu)

    def test_leikkaus(self):
        eka = self.tee_joukko(1, 2)
        toka = self.tee_joukko(2, 3, 4)

        tulos = IntJoukko.leikkaus(eka, toka)
        vastauksen_luvut = tulos.to_int_list()

        odotettu = [2]

        self.assertListEqual(sorted(vastauksen_luvut), odotettu)

    def test_erotus(self):
        eka = self.tee_joukko(1, 2, 5, 6)
        toka = self.tee_joukko(2, 3, 4)

        tulos = IntJoukko.erotus(eka, toka)
        vastauksen_luvut = tulos.to_int_list()

        odotettu = [1, 5, 6]

        self.assertListEqual(sorted(vastauksen_luvut), odotettu)
