import unittest
from unittest.mock import patch
from nuottiarvaus import Nuottiarvaus
import pygame

class Test_Nuottien_Toiminta(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.init()

    @patch("pygame.midi.Output")
    def setUp(self, soitin):
        self.nuottiarvaus = Nuottiarvaus(soitin)
        self.paikat_diskantti = self.nuottiarvaus.paikat_diskantti

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

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
        self.assertEqual(self.nuottiarvaus.taso_oikein_talla_tasolla, 0, "Tason oikeiden vastausten määrän pitäisi alkaa arvosta 0")
        self.assertEqual(self.nuottiarvaus.taso_vaadittu_oikein_maara, 20, "Vaadittujen oikeiden vastausten määrän pitäisi alkaa arvosta 20")
        for i in range(1, 22):
            self.nuottiarvaus._Nuottiarvaus__Luo_Nuotti()
            if i <= 20:
                self.assertEqual(self.nuottiarvaus.taso, 1, "Pelitason pitäisi olla 1 kunnes 20 oikeaa vastausta on saatu")
            else:
                self.assertEqual(self.nuottiarvaus.taso, 2, "Pelitason pitäisi olla 2 20 oikean vastauksen jälkeen")
                self.assertEqual(self.nuottiarvaus.taso_oikein_talla_tasolla, 0, "Oikein vastausten pitäisi palata takaisin 0 arvoon")
            self.nuottiarvaus.taso_oikein_talla_tasolla += 1
    
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

    def pelitasojen_testaaja(self, taso:int, savellajit:list, diskantti_sallitut_arvot:list, diskantti_midialue:tuple, basso_midialue:tuple,
                             ylennyksen_sallitut_arvot:list, alennuksen_sallitut_arvot:list, palautuksen_sallitut_arvot:list, palautus_vain_rajoilla:bool):
        """Apufunktio eri pelitasojen testaamiseen"""
        self.nuottiarvaus.taso = taso
        normaali_laskuri = 0
        ylennys_laskuri = 0
        alennus_laskuri = 0
        palautus_laskuri = 0
        for i in range(100):
            self.nuottiarvaus._Nuottiarvaus__Luo_Nuotti()

            # Sävellajit
            self.assertIn(self.nuottiarvaus.savellaji, savellajit, f"Tasolla {taso} sävellajin pitäisi olla jokin seuraavista {savellajit}")

            # Ylennykset, Alennukset, Palautukset
            self.assertIn(self.nuottiarvaus.piirra_ylennetty, ylennyksen_sallitut_arvot, f"Tasolla {taso} ei pitäisi olla nuottien ylennyksiä")
            self.assertIn(self.nuottiarvaus.piirra_alennettu, alennuksen_sallitut_arvot, f"Tasolla {taso} ei pitäisi olla nuottien alennuksia")
            self.assertIn(self.nuottiarvaus.piirra_palautus, palautuksen_sallitut_arvot, f"Tasolla {taso} ei pitäisi olla nuottien palautuksia")
            if self.nuottiarvaus.piirra_ylennetty:
                ylennys_laskuri += 1
            elif self.nuottiarvaus.piirra_alennettu:
                alennus_laskuri += 1
            elif self.nuottiarvaus.piirra_palautus:
                if palautus_vain_rajoilla:
                     self.assertIn(self.nuottiarvaus.nuotti_midi,
                                   [diskantti_midialue[0],
                                    diskantti_midialue[1],
                                    basso_midialue[0], 
                                    basso_midialue[1]], 
                                    f"Tasolla {taso} nuotin palautuksen saa tehdään vain midiarvojen rajoilla")
                palautus_laskuri += 1
            else:
                normaali_laskuri += 1

            # Midi rajat
            self.assertIn(self.nuottiarvaus.diskantti, diskantti_sallitut_arvot, f"Tasolla {taso} diskantin pitäisi olla arvossa {diskantti_sallitut_arvot}")
            if self.nuottiarvaus.diskantti == True:
                self.assertGreaterEqual(self.nuottiarvaus.nuotti_midi, diskantti_midialue[0], f"Tasolla {taso} diskantin midiarvon pitäisi olla minimissään {diskantti_midialue[0]}")
                self.assertLessEqual(self.nuottiarvaus.nuotti_midi, diskantti_midialue[1], f"Tasolla {taso} diskantin midiarvon pitäisi olla maksimissaan {diskantti_midialue[1]}")
            else:
                self.assertGreaterEqual(self.nuottiarvaus.nuotti_midi, basso_midialue[0], f"Tasolla {taso} basson midiarvon pitäisi olla minimissään {basso_midialue[0]}")
                self.assertLessEqual(self.nuottiarvaus.nuotti_midi, basso_midialue[1], f"Tasolla {taso} basson midiarvon pitäisi olla maksimissaan {basso_midialue[1]}")

        if True in ylennyksen_sallitut_arvot:
            self.assertNotEqual(ylennys_laskuri, 0, "Yhtään ylennettyä nuottia ei arvottu, vaikka niitä pitäisi esiintyä")
        if True in alennuksen_sallitut_arvot:
            self.assertNotEqual(alennus_laskuri, 0, "Yhtään alennettua nuottia ei arvottu, vaikka niitä pitäisi esiintyä")
        if True in palautuksen_sallitut_arvot and palautus_vain_rajoilla == False:
            self.assertNotEqual(palautus_laskuri, 0,"Yhtään palautettua nuottia ei arvottu, vaikka niitä pitäisi esiintyä")
        
        self.assertNotEqual(normaali_laskuri, 0, "Yhtään normaalia nuottia ei arvottu, vaikka niitä pitäisi esiintyä")
        
    def test_taso_1(self):
        self.pelitasojen_testaaja(1, ["C"], [True], (60,72), (), [False], [False], [False], False)

    def test_taso_2(self):
        self.pelitasojen_testaaja(2, ["C"], [True], (self.nuottiarvaus.midi_diskantti_alaraja, self.nuottiarvaus.loppu_midi), (), [False], [False], [False], False)
    
    def test_taso_3(self):
        self.pelitasojen_testaaja(3, ["C"], [False], (), (48, 60), [False], [False], [False], False)

    def test_taso_4(self):
        self.pelitasojen_testaaja(4, ["C"], [False], (), (self.nuottiarvaus.alku_midi, self.nuottiarvaus.midi_basso_ylaraja), [False], [False], [False], False)

    def test_taso_5(self):
        self.pelitasojen_testaaja(5, ["C"], [True, False], (self.nuottiarvaus.midi_diskantti_alaraja, self.nuottiarvaus.loppu_midi), 
                                  (self.nuottiarvaus.alku_midi, self.nuottiarvaus.midi_basso_ylaraja), [True, False], [False], [False], False)
    
    def test_taso_6(self):
        self.pelitasojen_testaaja(6, ["C"], [True, False], (self.nuottiarvaus.midi_diskantti_alaraja, self.nuottiarvaus.loppu_midi), 
                                  (self.nuottiarvaus.alku_midi, self.nuottiarvaus.midi_basso_ylaraja), [False], [True, False], [False], False)

    def test_taso_7(self):
        self.pelitasojen_testaaja(7, ["C"], [True, False], (self.nuottiarvaus.midi_diskantti_alaraja, self.nuottiarvaus.loppu_midi), 
                                  (self.nuottiarvaus.alku_midi, self.nuottiarvaus.midi_basso_ylaraja), [True, False], [True, False], [False], False)

    def test_taso_8(self):
        self.pelitasojen_testaaja(8, ["F", "d", "G", "e"], [True, False], (self.nuottiarvaus.midi_diskantti_alaraja, self.nuottiarvaus.loppu_midi), 
                                  (self.nuottiarvaus.alku_midi, self.nuottiarvaus.midi_basso_ylaraja), [False], [False], [True, False], True)

    def test_taso_9(self):
        self.pelitasojen_testaaja(9, ["B", "g", "D", "h"], [True, False], (self.nuottiarvaus.midi_diskantti_alaraja, self.nuottiarvaus.loppu_midi), 
                                  (self.nuottiarvaus.alku_midi, self.nuottiarvaus.midi_basso_ylaraja), [False], [False], [True, False], True)
    
    def test_taso_10(self):
        self.pelitasojen_testaaja(10, ["Eb", "c", "A", "f#"], [True, False], (self.nuottiarvaus.midi_diskantti_alaraja, self.nuottiarvaus.loppu_midi), 
                                  (self.nuottiarvaus.alku_midi, self.nuottiarvaus.midi_basso_ylaraja), [False], [False], [True, False], True)
    
    def test_taso_11(self):
        self.pelitasojen_testaaja(11, ["Ab", "f", "E", "c#"], [True, False], (self.nuottiarvaus.midi_diskantti_alaraja, self.nuottiarvaus.loppu_midi), 
                                  (self.nuottiarvaus.alku_midi, self.nuottiarvaus.midi_basso_ylaraja), [False], [False], [True, False], True)
    
    def test_taso_12(self):
        self.pelitasojen_testaaja(12, ["Db", "b", "H", "g#"], [True, False], (self.nuottiarvaus.midi_diskantti_alaraja, self.nuottiarvaus.loppu_midi), 
                                  (self.nuottiarvaus.alku_midi, self.nuottiarvaus.midi_basso_ylaraja), [False], [False], [True, False], True)
    
    def test_taso_13(self):
        self.pelitasojen_testaaja(13, ["Gb", "eb", "F#", "d#"], [True, False], (self.nuottiarvaus.midi_diskantti_alaraja, self.nuottiarvaus.loppu_midi), 
                                  (self.nuottiarvaus.alku_midi, self.nuottiarvaus.midi_basso_ylaraja), [False], [False], [True, False], True)
    
    def test_taso_14(self):
        self.pelitasojen_testaaja(14, ["Cb", "ab", "C#", "a#"], [True, False], (self.nuottiarvaus.midi_diskantti_alaraja, self.nuottiarvaus.loppu_midi), 
                                  (self.nuottiarvaus.alku_midi, self.nuottiarvaus.midi_basso_ylaraja), [False], [False], [True, False], True)

    def test_taso_15(self):
        self.pelitasojen_testaaja(15, ["Cb","ab", "Gb","eb", "Db","b", "Ab","f", "Eb","c", "B","g", "F","d", "C","a", "G","e", "D","h", "A","f#", "E","c#", "H","g#", "F#","d#", "C#","a#"], 
                                  [True, False], (self.nuottiarvaus.midi_diskantti_alaraja, self.nuottiarvaus.loppu_midi), 
                                  (self.nuottiarvaus.alku_midi, self.nuottiarvaus.midi_basso_ylaraja), [True, False], [True, False], [True, False], False)