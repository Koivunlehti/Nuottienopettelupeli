import unittest
from nuottiarvaus import Nuottiarvaus
import pygame.midi

pygame.midi.init()
soitin = pygame.midi.Output(0)

class Test_Nuottien_Toiminta(unittest.TestCase):

    def setUp(self):
        
        self.nuottiarvaus = Nuottiarvaus(soitin)
        self.paikat_diskantti = self.nuottiarvaus.paikat_diskantti

    # Nuottien Arvonnan testejä

    def test_arvo_nuotti_yla_ja_alaraja(self):
        """ Testaa, että nuotin midiarvo arvotaan annetuissa rajoissa """
        for i in range(100):
            self.nuottiarvaus._Nuottiarvaus__Arvo_Nuotti(60, 72, self.paikat_diskantti)
            self.assertGreaterEqual(self.nuottiarvaus.nuotti_midi, 60, "Nuotti meni yli asetetun ylärajan")
            self.assertLessEqual(self.nuottiarvaus.nuotti_midi, 72, "Nuotti meni yli asetetun ylärajan")

    def test_arvo_nuotti_mustan_koskettimen_nuotti_alemmas(self):
        """ Testaa, että jos nuotin midiarvo osuu mustalle koskettimelle, se alennetaan """
        self.nuottiarvaus._Nuottiarvaus__Arvo_Nuotti(61, 61, self.paikat_diskantti)
        self.assertEqual(self.nuottiarvaus.nuotti_midi, 60, "Annetun nuotin midi-arvoa ei alennettu vaikka se on mustalla koskettimella")

    def test_arvo_nuotti_oikea_y_koordinaatti(self):
        """ Testaa, että arvotulle nuotille annetaan oikea y-koordinaatti"""
        self.nuottiarvaus._Nuottiarvaus__Arvo_Nuotti(60, 60, self.paikat_diskantti)
        self.assertEqual(self.nuottiarvaus.nuotti_y, self.paikat_diskantti[60][0], "Nuotti ei saanut oikeaa y-koordinaattia")

    # Sävellajin vaikutus

    def test_savellaji_ylentaa_nuotin(self):
        """ Testaa, että sävellaji ylentää nuotin midiarvon oikein bassolla ja diskantilla """
        # Diskantti
        self.nuottiarvaus.nuotti_midi = 60
        self.nuottiarvaus.diskantti = True
        self.nuottiarvaus._Nuottiarvaus__Savellajin_Vaikutus_Ylennys(62, 62)
        self.assertEqual(self.nuottiarvaus.nuotti_midi, 61, "Sävellaji ei ylentänyt nuottia (diskantti)")
        # Basso
        self.nuottiarvaus.nuotti_midi = 60
        self.nuottiarvaus.diskantti = False
        self.nuottiarvaus._Nuottiarvaus__Savellajin_Vaikutus_Ylennys(62, 62)
        self.assertEqual(self.nuottiarvaus.nuotti_midi, 61, "Sävellaji ei ylentänyt nuottia (basso)")

    def test_savellaji_ei_ylenna_nuottia_jos_se_on_ylarajalla(self):
        """ Testaa, että sävellaji ei ylennä nuotin midiarvoa jos arvo menee yli annetun rajan bassolla ja diskantilla """
        # Diskantti
        self.nuottiarvaus.nuotti_midi = 60
        self.nuottiarvaus.diskantti = True
        self.nuottiarvaus._Nuottiarvaus__Savellajin_Vaikutus_Ylennys(60, 60)
        self.assertEqual(self.nuottiarvaus.nuotti_midi, 60, "Sävellaji ylensi nuotin vaikka se on ylärajalla (diskantti)")
        self.assertEqual(self.nuottiarvaus.piirra_palautus, True, "Koska sävellajin vaatimaa ylennysta ei voitu tehdä, pitää nuotille piirtää palautusmerkki (diskantti)")
        # Basso
        self.nuottiarvaus.nuotti_midi = 60
        self.nuottiarvaus.diskantti = False
        self.nuottiarvaus._Nuottiarvaus__Savellajin_Vaikutus_Ylennys(60, 60)
        self.assertEqual(self.nuottiarvaus.nuotti_midi, 60, "Sävellaji ylensi nuotin vaikka se on ylärajalla (basso)")
        self.assertEqual(self.nuottiarvaus.piirra_palautus, True, "Koska sävellajin vaatimaa ylennysta ei voitu tehdä, pitää nuotille piirtää palautusmerkki (basso)")

    def test_savellaji_alentaa_savelen(self):
        """ Testaa, että sävellaji alentaa nuotin midiarvon oikein bassolla ja diskantilla """
        # Diskantti
        self.nuottiarvaus.nuotti_midi = 60
        self.nuottiarvaus.diskantti = True
        self.nuottiarvaus._Nuottiarvaus__Savellajin_Vaikutus_Alennus(58, 58)
        self.assertEqual(self.nuottiarvaus.nuotti_midi, 59, "Sävellaji ei alentanut nuottia (diskantti)")
        # Basso
        self.nuottiarvaus.nuotti_midi = 60
        self.nuottiarvaus.diskantti = False
        self.nuottiarvaus._Nuottiarvaus__Savellajin_Vaikutus_Alennus(58, 58)
        self.assertEqual(self.nuottiarvaus.nuotti_midi, 59, "Sävellaji ei alentanut nuottia (basso)")

    def test_savellaji_ei_alenna_nuottia_jos_se_on_alarajalla(self):
        """ Testaa, että sävellaji ei alenna nuotin midiarvoa jos arvo menee alle annetun rajan bassolla ja diskantilla """
        # Diskantti
        self.nuottiarvaus.nuotti_midi = 60
        self.nuottiarvaus.diskantti = True
        self.nuottiarvaus._Nuottiarvaus__Savellajin_Vaikutus_Alennus(60, 60)
        self.assertEqual(self.nuottiarvaus.nuotti_midi, 60, "Sävellaji alensi nuotin vaikka se on alarajalla (diskantti)")
        self.assertEqual(self.nuottiarvaus.piirra_palautus, True, "Koska sävellajin vaatimaa alennusta ei voitu tehdä, pitää nuotille piirtää palautusmerkki (diskantti)") 
        # Basso
        self.nuottiarvaus.nuotti_midi = 60
        self.nuottiarvaus.diskantti = False
        self.nuottiarvaus._Nuottiarvaus__Savellajin_Vaikutus_Alennus(60, 60)
        self.assertEqual(self.nuottiarvaus.nuotti_midi, 60, "Sävellaji alensi nuotin vaikka se on alarajalla (basso)")
        self.assertEqual(self.nuottiarvaus.piirra_palautus, True, "Koska sävellajin vaatimaa alennusta ei voitu tehdä, pitää nuotille piirtää palautusmerkki (basso)")

     # Nuotin ylennys

    def test_nuotin_ylennys(self):
        """ Testaa, että nuotin midiarvoa voidaan ylentää"""
        # Diskantti
        self.nuottiarvaus.nuotti_midi = 60
        self.nuottiarvaus.diskantti = True
        self.nuottiarvaus._Nuottiarvaus__Nuotti_Ylennys("",72, 72)
        self.assertEqual(self.nuottiarvaus.nuotti_midi, 61, "Nuotin pitäisi olla ylennetty (diskantti)")
        self.assertEqual(self.nuottiarvaus.piirra_ylennetty, True, "Ylennysmerkki pitäisi piirtää (diskantti)")
        # Basso
        self.nuottiarvaus.nuotti_midi = 60
        self.nuottiarvaus.diskantti = False
        self.nuottiarvaus._Nuottiarvaus__Nuotti_Ylennys("",72, 72)
        self.assertEqual(self.nuottiarvaus.nuotti_midi, 61, "Nuotin pitäisi olla ylennetty (basso)")
        self.assertEqual(self.nuottiarvaus.piirra_ylennetty, True, "Ylennysmerkki pitäisi piirtää (basso)")

    def test_nuottia_ei_ylenneta_jos_se_on_ylarajalla(self):
        """ Testaa, että nuotin midiarvoa ei voida ylentää ylärajalla """
        # Diskantti
        self.nuottiarvaus.nuotti_midi = 60
        self.nuottiarvaus.diskantti = True
        self.nuottiarvaus._Nuottiarvaus__Nuotti_Ylennys("", 60, 60)
        self.assertEqual(self.nuottiarvaus.nuotti_midi, 60, "Nuottia ei pitäisi ylentää (diskantti)")
        self.assertEqual(self.nuottiarvaus.piirra_ylennetty, False, "Ylennysmerkkiä ei pitäisi piirtää (diskantti)")
        # Basso
        self.nuottiarvaus.nuotti_midi = 60
        self.nuottiarvaus.diskantti = False
        self.nuottiarvaus._Nuottiarvaus__Nuotti_Ylennys("", 60, 60)
        self.assertEqual(self.nuottiarvaus.nuotti_midi, 60, "Nuottia ei pitäisi ylentää (basso)")
        self.assertEqual(self.nuottiarvaus.piirra_ylennetty, False, "Ylennysmerkkiä ei pitäisi piirtää (basso)")
    
    def test_nuotin_ylennys_savellajin_alentamaan_nuottiin(self):
        """ Testaa, että nuotin ylennys toimii oikein sävellajin alentamassa nuotissa """
        # Diskantti
        self.nuottiarvaus.nuotti_midi = 59
        self.nuottiarvaus.diskantti = True
        self.nuottiarvaus._Nuottiarvaus__Nuotti_Ylennys("a", 72, 72)
        self.assertEqual(self.nuottiarvaus.nuotti_midi, 60, "Nuotin pitäisi olla ylennetty (diskantti)")
        self.assertEqual(self.nuottiarvaus.piirra_palautus, True, "Palautusmerkki pitäisi piirtää (diskantti)")
        # Basso
        self.nuottiarvaus.nuotti_midi = 59
        self.nuottiarvaus.diskantti = False
        self.nuottiarvaus._Nuottiarvaus__Nuotti_Ylennys("a", 72, 72)
        self.assertEqual(self.nuottiarvaus.nuotti_midi, 60, "Nuotin pitäisi olla ylennetty (basso)")
        self.assertEqual(self.nuottiarvaus.piirra_palautus, True, "Palautusmerkki pitäisi piirtää (basso)")

    # Nuotin alennus

    def test_nuotin_alennus(self):
        """ Testaa, että nuotin midiarvoa voidaan alentaa"""
        # Diskantti
        self.nuottiarvaus.nuotti_midi = 60
        self.nuottiarvaus.diskantti = True
        self.nuottiarvaus._Nuottiarvaus__Nuotti_Alennus("", 48, 48)
        self.assertEqual(self.nuottiarvaus.nuotti_midi, 59, "Nuotin pitäisi olla alennettu (diskantti)")
        self.assertEqual(self.nuottiarvaus.piirra_alennettu, True, "Alennusmerkki pitäisi piirtää (diskantti)")
        # Basso
        self.nuottiarvaus.nuotti_midi = 60
        self.nuottiarvaus.diskantti = False
        self.nuottiarvaus._Nuottiarvaus__Nuotti_Alennus("", 48, 48)
        self.assertEqual(self.nuottiarvaus.nuotti_midi, 59, "Nuotin pitäisi olla alennettu (basso)")
        self.assertEqual(self.nuottiarvaus.piirra_alennettu, True, "Alennusmerkki pitäisi piirtää (basso)")

    def test_nuottia_ei_alenneta_jos_se_on_alarajalla(self):
        """ Testaa, että nuotin midiarvoa ei voida alentaa alarajalla """
        # Diskantti
        self.nuottiarvaus.nuotti_midi = 60
        self.nuottiarvaus.diskantti = True
        self.nuottiarvaus._Nuottiarvaus__Nuotti_Alennus("", 60, 60)
        self.assertEqual(self.nuottiarvaus.nuotti_midi, 60, "Nuottia ei pitäisi alentaa (diskantti)")
        self.assertEqual(self.nuottiarvaus.piirra_alennettu, False, "Alennusmerkkiä ei pitäisi piirtää (diskantti)")
        # Basso
        self.nuottiarvaus.nuotti_midi = 60
        self.nuottiarvaus.diskantti = False
        self.nuottiarvaus._Nuottiarvaus__Nuotti_Alennus("", 60, 60)
        self.assertEqual(self.nuottiarvaus.nuotti_midi, 60, "Nuottia ei pitäisi alentaa (basso)")
        self.assertEqual(self.nuottiarvaus.piirra_alennettu, False, "Alennusmerkkiä ei pitäisi piirtää (basso)")
    
    def test_nuotin_alennus_savellajin_ylentamaan_nuottiin(self):
        """ Testaa, että nuotin alennus toimii oikein sävellajin ylentämässä nuotissa """
        # Diskantti
        self.nuottiarvaus.nuotti_midi = 61
        self.nuottiarvaus.diskantti = True
        self.nuottiarvaus._Nuottiarvaus__Nuotti_Alennus("y", 48, 48)
        self.assertEqual(self.nuottiarvaus.nuotti_midi, 60, "Nuotin pitäisi olla alennettu (diskantti)")
        self.assertEqual(self.nuottiarvaus.piirra_palautus, True, "Palautusmerkki pitäisi piirtää (diskantti)")
        # Basso
        self.nuottiarvaus.nuotti_midi = 61
        self.nuottiarvaus.diskantti = False
        self.nuottiarvaus._Nuottiarvaus__Nuotti_Alennus("y", 48, 48)
        self.assertEqual(self.nuottiarvaus.nuotti_midi, 60, "Nuotin pitäisi olla alennettu (basso)")
        self.assertEqual(self.nuottiarvaus.piirra_palautus, True, "Palautusmerkki pitäisi piirtää (basso)")

    # Pelitasot

    def test_pelitason_nousu(self):
        """ Testaa, että pelitasoa voidaan nostaa halutulla määrällä oikeita vastauksia """
        self.assertEqual(self.nuottiarvaus.taso, 1, "Pelitason pitäisi alkaa arvosta 1")
        self.assertEqual(self.nuottiarvaus.oikein_maara, 0, "Oikeiden vastausten määrän pitäisi alkaa arvosta 0")
        for i in range(1, 12):
            self.nuottiarvaus._Nuottiarvaus__Luo_Nuotti()
            if i <= 10:
                self.assertEqual(self.nuottiarvaus.taso, 1, "Pelitason pitäisi olla 1 kunnes 10 oikeaa vastausta on saatu")
            else:
                self.assertEqual(self.nuottiarvaus.taso, 2, "Pelitason pitäisi olla 2 10 oikean vastauksen jälkeen")
                self.assertEqual(self.nuottiarvaus.oikein_maara, 0, "Oikein vastausten pitäisi palata takaisin 0 arvoon")
            self.nuottiarvaus.oikein_maara += 1
    
    def test_pelitason_lasku(self):
        """ Testaa, että pelitasoa voidaan laskea halutulla määrällä vääriä vastauksia """
        self.nuottiarvaus.taso = 2
        self.assertEqual(self.nuottiarvaus.virhe_maara, 0, "Virheiden määrän pitäisi olla 0")
        for i in range(1, 7):
            self.nuottiarvaus._Nuottiarvaus__Virhelaskuri()
            if i <= 5:
                self.assertEqual(self.nuottiarvaus.taso, 2, "Pelitason pitäisi olla 2 kunnes 5 virhettä on saatu")
            else:
                self.assertEqual(self.nuottiarvaus.taso, 1, "Pelitason pitäisi olla 1 viiden virheen jälkeen")
                self.assertEqual(self.nuottiarvaus.virhe_maara, 0, "Virheiden määrän pitäisi palata takaisin 0 arvoon")
            self.nuottiarvaus.virhe_maara += 1
        
        self.nuottiarvaus.taso = 1
        self.nuottiarvaus.virhe_maara = 5
        self.nuottiarvaus._Nuottiarvaus__Virhelaskuri()
        self.assertEqual(self.nuottiarvaus.taso, 1, "Pelitason ei pitäisi laskea alle yhden")