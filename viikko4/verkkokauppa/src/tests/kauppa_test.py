import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.varasto_mock = Mock()


    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):

        # palautetaan aina arvo 42
        self.viitegeneraattori_mock.uusi.return_value = 42

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        # otetaan toteutukset käyttöön
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        # tehdään ostokset
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_maksettaessa_tilisiirtoa_kutsutaan_oikeilla_parametreilla(self):
        
        self.viitegeneraattori_mock.uusi.return_value = 41

        def varasto_saldo(tuote_id):
            if tuote_id == 2:
                return 10
            
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 2:
                return Tuote(2, "jauheliha", 5)
            
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("Seppo", "54321")

        self.pankki_mock.tilisiirto.assert_called_with("Seppo", ANY, "54321", "33333-44455", 5)

    def test_maksettaessa_kaksi_eri_tuotetta_tilisiirtoa_kutsutaan_oikeilla_parametreilla(self):
        
        self.viitegeneraattori_mock.uusi.return_value = 43

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 10
            
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "jauheliha", 7)
            
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("Matti", "67890")

        self.pankki_mock.tilisiirto.assert_called_with("Matti", ANY, "67890", "33333-44455", 12)

    def test_maksettaessa_kaksi_samaa_tuotetta_tilisiirtoa_kutsutaan_oikeilla_parametreilla(self):
        
        self.viitegeneraattori_mock.uusi.return_value = 44

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("Liisa", "11223")

        self.pankki_mock.tilisiirto.assert_called_with("Liisa", ANY, "11223", "33333-44455", 10)

    def test_maksettaessa_tuote_jota_on_varastossa_sekä_tuote_jota_ei_ole_tilisiirtoa_kutsutaan_oikeilla_parametreilla(self):
        
        self.viitegeneraattori_mock.uusi.return_value = 45

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 0
            
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "jauheliha", 7)
            
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("Henrik", "99887")
        
        self.pankki_mock.tilisiirto.assert_called_with("Henrik", ANY, "99887", "33333-44455", 5)

    def test_aloita_asiointi_nollaa_edellisen_ostoksen_tiedot(self):
        self.viitegeneraattori_mock.uusi.return_value = 46

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("Anna", "33445")

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("Anna", "33445")

        self.pankki_mock.tilisiirto.assert_called_with("Anna", ANY, "33445", "33333-44455", 5)

    def test_jokaiselle_maksulle_uusi_viitenumero(self):

        viitegeneraattori_mock = Mock(Wraps=Viitegeneraattori())

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 10
            
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "jauheliha", 7)
            
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("Kalle", "12345")

        self.assertEqual(viitegeneraattori_mock.uusi.call_count, 1)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("Liisa", "67890")

        self.assertEqual(viitegeneraattori_mock.uusi.call_count, 2)

    def test_poista_korista_toimii(self):
        self.viitegeneraattori_mock.uusi.return_value = 47

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.poista_korista(1)
        kauppa.tilimaksu("Olli", "55667")

        self.pankki_mock.tilisiirto.assert_called_with("Olli", ANY, "55667", "33333-44455", 0)
