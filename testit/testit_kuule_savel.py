import unittest
from unittest.mock import patch
from kuule_savel import Kuule_Savel

class Test_Nuottien_Toiminta(unittest.TestCase):

    @patch("pygame.midi.Output")
    def setUp(self, soitin): 
        self.kuule_savel = Kuule_Savel(soitin)

    # Sävelen arvonnan testaus

    def test_arvo_midi(self):
        self.kuule_savel.midi_alue = (60,71)
        self.kuule_savel.ilman_korotusta = True
        for i in range(100):    
            self.kuule_savel._Kuule_Savel__Arvo_Midi()
            self.assertIn(self.kuule_savel.midi,[60,62,64,65,67,69,71],"Vain korottamattomia säveliä pitäisi esiintyä")

        self.kuule_savel.ilman_korotusta = False
        for i in range(100):    
            self.kuule_savel._Kuule_Savel__Arvo_Midi()
            self.assertIn(self.kuule_savel.midi,[60,61,62,63,64,65,66,67,68,69,70,71],"Sävel ei ollut oikealla Midi-alueella")

    # Oikean ja väärän vastauksen testaus

    def test_oikea_vastaus(self):
        self.kuule_savel.midi = 60
        self.kuule_savel._Kuule_Savel__Tarkista_Vastaus("C")
        self.assertTrue(self.kuule_savel.valmistaudu, 'Oikealla vastauksella pelin pitäisi siirtyä "valmistaudu" tilaan')
        self.assertEqual(self.kuule_savel.vastauspainikkeet_vaarin, [], "Väärin vastattujen painikkeiden listan pitäisi tyhjentyä")
        self.assertEqual(self.kuule_savel.otsikkoteksti, f"Sävel oli C", "Otsikkotekstin arvoksi pitäisi tulla oikea sävel.")
        self.assertEqual(self.kuule_savel.oikein_vaarin_teksti, "Oikein", "Oikein ja väärin tekstin arvo ei ole oikein")
        self.assertEqual(self.kuule_savel.oikein_vaarin_ajastin, 60, "Oikein ja väärin tekstin ajastin ei ole oikeassa arvossa")
        self.assertEqual(self.kuule_savel.oikein_maara, 1, "Oikeiden vastausten laskurin pitäisi lisääntyä yhdellä")
        self.assertEqual(self.kuule_savel.pelitaso_oikein_talla_tasolla, 1, "Pelitason oikeiden vastausten laskurin pitäisi lisääntyä yhdellä")
        self.assertEqual(self.kuule_savel.pisteet, 30, "Annettu pistemäärä ei ole oikein")
        self.assertEqual(self.kuule_savel.arvausmaara, 3, "Arvausmäärä ei palautunut oikeaan arvoon")
    
    def test_vaara_vastaus(self):
        self.kuule_savel.midi = 60
        self.kuule_savel._Kuule_Savel__Tarkista_Vastaus("E")
        self.assertFalse(self.kuule_savel.valmistaudu, 'Väärällä vastauksella pelin ei pitäisi siirtyä "valmistaudu" tilaan')
        self.assertEqual(self.kuule_savel.vastauspainikkeet_vaarin, ["E"], "Väärin vastattujen painikkeiden listan pitäisi tyhjentyä")
        self.assertEqual(self.kuule_savel.oikein_vaarin_teksti, "Väärin", "Oikein ja väärin tekstin arvo ei ole oikein")
        self.assertEqual(self.kuule_savel.oikein_vaarin_ajastin, 60, "Oikein ja väärin tekstin ajastin ei ole oikeassa arvossa")
        self.assertEqual(self.kuule_savel.vaarin_maara, 1, "Väärien vastausten laskurin pitäisi lisääntyä yhdellä")
        self.assertEqual(self.kuule_savel.arvausmaara, 2, "Arvausmäärä ei ole oikein")

    # Pelin tilamuutosten testaus
    def test_pelitason_vaihtaminen(self):
        self.kuule_savel.pelitaso_vaihda = True
        self.kuule_savel.pelitaso = 1
        self.kuule_savel.otsikkoteksti = ""
        self.kuule_savel.ajastin = 0
        self.kuule_savel._Kuule_Savel__Tarkista_Pelin_Tila()
        
        self.assertEqual(self.kuule_savel.otsikkoteksti, "Aloitetaan peli", "Tasolla yksi otsikkoteksti on väärin")
        self.assertEqual(self.kuule_savel.ajastin, 1, "Ajastin ei liikkunut eteenpäin")
        self.assertFalse(self.kuule_savel.soita_savelet, "Soita sävelet tilan ei pitäisi olla aktiivinen")
        self.assertFalse(self.kuule_savel.valmistaudu, "Valmistaudu tilan ei pitäisi olla aktiivinen")
        self.assertEqual(self.kuule_savel.aliteksti, "Taso 1", "Alitekstin pitäisi näyttää nykyinen taso")

        self.kuule_savel.ajastin = 180

        self.kuule_savel._Kuule_Savel__Tarkista_Pelin_Tila()
        self.assertEqual(self.kuule_savel.ajastin, 0, "Ajastimen pitäisi nollaantua")
        self.assertEqual(self.kuule_savel.midi, 60, "Midi arvon pitäisi palautua arvoon 60")
        self.assertEqual(self.kuule_savel.aliteksti, "", "Alitekstin pitäisi olla tyhjä")
        self.assertTrue(self.kuule_savel.soita_savelet, "Soita sävelet tilan pitäisi olla aktiivinen")
        self.assertFalse(self.kuule_savel.pelitaso_vaihda, "Pelitason vaihtotilan ei pitäisi olla aktiivinen")
        self.assertFalse(self.kuule_savel.valmistaudu, "Valmistaudu tilan ei pitäisi olla aktiivinen")

    def test_soita_savelet(self):
        self.kuule_savel.soita_savelet = True
        self.kuule_savel.otsikkoteksti = ""
        self.kuule_savel.ajastin = 0
        self.kuule_savel.midi = 60
        self.kuule_savel.midi_alue = (60,72)
        self.kuule_savel._Kuule_Savel__Tarkista_Pelin_Tila()

        self.assertEqual(self.kuule_savel.otsikkoteksti, "Sävelten läpikäynti...", "Otsikkoteksti on väärin")
        self.assertEqual(self.kuule_savel.ajastin, 1, "Ajastin ei liikkunut eteenpäin")

        self.kuule_savel.ajastin = 60
        self.kuule_savel._Kuule_Savel__Tarkista_Pelin_Tila()

        self.assertEqual(self.kuule_savel.ajastin, 0, "Ajastimen pitäisi nollaantua")
        self.assertEqual(self.kuule_savel.aliteksti, "C", "Alitekstin ei näyttänyt oikeaa säveltä")
        self.assertEqual(self.kuule_savel.midi, 61, "Midin arvo ei lisääntynyt")

        self.kuule_savel.ajastin = 60
        self.kuule_savel.midi = 73
        self.kuule_savel._Kuule_Savel__Tarkista_Pelin_Tila()

        self.assertTrue(self.kuule_savel.valmistaudu, "Valmistaudu tilan pitäisi olla aktiivinen")
        self.assertEqual(self.kuule_savel.ajastin, 0, "Ajastimen pitäisi nollaantua")
        self.assertEqual(self.kuule_savel.midi, 60, "Midin arvo ei nollaantunut")
        self.assertFalse(self.kuule_savel.soita_savelet, "Soita sävelet tilan ei pitäisi olla aktiivinen")
        self.assertEqual(self.kuule_savel.otsikkoteksti, "", "Otsikkotekstiä ei tyhjennetty")

    def test_soita_savelet_jos_ei_savelten_korotuksia(self):
        self.kuule_savel.soita_savelet = True
        self.kuule_savel.otsikkoteksti = ""
        self.kuule_savel.ajastin = 60
        self.kuule_savel.midi = 60
        self.kuule_savel.midi_alue = (60,72)
        self.kuule_savel.ilman_korotusta = True
        self.kuule_savel._Kuule_Savel__Tarkista_Pelin_Tila()

        self.assertEqual(self.kuule_savel.aliteksti, "C", "Alitekstin ei näyttänyt oikeaa säveltä")
        self.assertEqual(self.kuule_savel.midi, 62, "Midin arvo ei lisääntynyt tarpeeksi")

        self.kuule_savel.ajastin = 60
        self.kuule_savel._Kuule_Savel__Tarkista_Pelin_Tila()

        self.assertEqual(self.kuule_savel.aliteksti, "D", "Alitekstin ei näyttänyt oikeaa säveltä")
        self.assertEqual(self.kuule_savel.midi, 64, "Midin arvo ei lisääntynyt tarpeeksi")

        self.kuule_savel.ajastin = 60
        self.kuule_savel._Kuule_Savel__Tarkista_Pelin_Tila()

        self.assertEqual(self.kuule_savel.aliteksti, "E", "Alitekstin ei näyttänyt oikeaa säveltä")
        self.assertEqual(self.kuule_savel.midi, 65, "Midin arvo ei lisääntynyt yhdellä")

        self.kuule_savel.ajastin = 60
        self.kuule_savel._Kuule_Savel__Tarkista_Pelin_Tila()

        self.assertEqual(self.kuule_savel.aliteksti, "F", "Alitekstin ei näyttänyt oikeaa säveltä")
        self.assertEqual(self.kuule_savel.midi, 67, "Midin arvo ei lisääntynyt yhdellä")

    def test_valmistaudu(self):
        self.kuule_savel.valmistaudu = True
        self.kuule_savel.ajastin = 0
        self.kuule_savel.valmistaudu_laskuri = 3
        self.kuule_savel._Kuule_Savel__Tarkista_Pelin_Tila()

        self.assertEqual(self.kuule_savel.ajastin, 1, "Ajastin ei liikkunut eteenpäin")

        self.kuule_savel.ajastin = 59
        self.kuule_savel._Kuule_Savel__Tarkista_Pelin_Tila()

        self.assertEqual(self.kuule_savel.ajastin, 60, "Ajastin ei liikkunut eteenpäin")
        self.assertEqual(self.kuule_savel.valmistaudu_laskuri, 2, "Sekunteja laskeva laskuri ei päivittynyt oikein")

        self.kuule_savel.ajastin = 180
        self.kuule_savel.midi = 0
        self.kuule_savel.midi_alue = (60,72)
        self.kuule_savel._Kuule_Savel__Tarkista_Pelin_Tila()

        self.assertFalse(self.kuule_savel.valmistaudu, "Valmistaudu tilan ei pitäisi olla aktiivinen")
        self.assertEqual(self.kuule_savel.ajastin, 0, "Ajastimen pitäisi nollaantua")
        self.assertEqual(self.kuule_savel.valmistaudu_laskuri, 3, "Sekunteja laskeva laskuri pitäisi palata oletukseen")
        self.assertEqual(self.kuule_savel.otsikkoteksti, "Mikä sävel?", "Otsikkoteksti ei ole oikea")
        self.assertGreaterEqual(self.kuule_savel.midi, 60, "Midiä ei arvottu oikein")
        self.assertLessEqual(self.kuule_savel.midi, 72, "Midiä ei arvottu oikein")