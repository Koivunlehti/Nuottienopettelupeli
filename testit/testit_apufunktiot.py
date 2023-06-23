import unittest
import apufunktiot

class Test_Apufunktioiden_Toiminta(unittest.TestCase):

    def test_luo_nuottien_paikat(self):
        """Testaa, että kaikki 128 midisäveltä löytyvät, niillä on oikeat y-koordinaatit ja että mustien koskettimien sävelet jakavat valkoisten koskettimien y-koordinaatit."""

        paikat = apufunktiot.Luo_Nuottien_Paikat(0, 1)

        self.assertEqual(len(paikat), 128, "Paikkoja pitäisi olla 128 eli midisävelten määrä")
        self.assertEqual(paikat[60][0], 0, "Keski-C y-koordinaatti piätisi olla 0")
        self.assertEqual(paikat[0][0], 35, "Sävelen nolla pitäisi sijaita y-koordinaatissa 35")
        self.assertEqual(paikat[127][0], -39, "Sävelen 127 pitäisi sijaita y-koordinaatissa -39")

        vali_y = 35 # Tämä luku on valkoisten koskettimien määrä keski-C:n alapuolella.
        
        for i in range(11):
            for j in range(0, 12):
                midi_arvo = i * 12 + j
                if midi_arvo >= 128:
                    return
                if j in [1,3,6,8,10]:
                    self.assertEqual(paikat[midi_arvo][0], vali_y, "Paikan y-koordinaatti on väärä")
                    self.assertEqual(paikat[midi_arvo][1], "m", 'Paikka pitäisi olla merkattu mustaksi koskettimeksi "m"')
                else:
                    self.assertEqual(paikat[midi_arvo][0], vali_y, "Paikan y-koordinaatti on väärä")
                    self.assertEqual(paikat[midi_arvo][1], "v", 'Paikka pitäisi olla merkattu valkoiseksi koskettimeksi "v"')

                if j in [1,3,4,6,8,10,11]:
                    vali_y -= 1
    
    def test_savellaji_vaikutus(self):
        """Testaa, että kaikki sävellajiin kuuluvat sävelet ylennetään tai alennetaan oikein ja että muut sävelet ovat normaaleja"""

        duurit = ["Cb", "Gb", "Db", "Ab", "Eb", "B", "F", "C", "G", "D", "A", "E", "H", "F#", "C#"]
        mollit = ["ab", "eb", "b", "f", "c", "g" , "d", "a", "e", "h", "f#", "c#", "g#", "d#", "a#"]

        def testaa_savelet(self, savellaji, savelet, ylennetty):
            """ Testin apufunktio, jonka avulla koko sävelalue käydään läpi"""
            for i in range(12):
                for j in range(12):
                    midi_arvo = j + i * 12
                    if midi_arvo <= 128:
                        if midi_arvo in savelet:
                            if ylennetty:
                                self.assertEqual(apufunktiot.Tarkista_Savellaji_Vaikutus(savellaji, midi_arvo), "y", f"Midi-sävel {midi_arvo} ei ole ylennetty vaikka sen pitäisi olla")
                            else:
                                self.assertEqual(apufunktiot.Tarkista_Savellaji_Vaikutus(savellaji, midi_arvo), "a", f"Midi-sävel {midi_arvo} ei ole alennettu vaikka sen pitäisi olla")
                        else:
                            self.assertEqual(apufunktiot.Tarkista_Savellaji_Vaikutus(savellaji, midi_arvo), "", f"Midi-sävel {midi_arvo} pitäisi olla normaalitilassa")
                    else:
                        return
                    
                savelet = [ midi + 12 for midi in savelet ] # Korotetaan haettavat sävelet yhdellä oktaavilla eli arvolla 12 

        for i in range(len(duurit)):
            duuri = duurit[i]
            molli = mollit[i]
            if duuri == "Cb" or duuri == "C#" or molli == "ab" or molli == "a#":
                savelet = [0, 2, 4, 5, 7, 9, 11]
                if duuri == "C#" or molli == "a#":
                    testaa_savelet(self, duuri, savelet, True)
                    testaa_savelet(self, molli, savelet, True)
                else:
                    testaa_savelet(self, duuri, savelet, False)
                    testaa_savelet(self, molli, savelet, False)
            elif duuri == "Gb" or duuri == "F#" or molli == "eb" or molli == "d#":
                if duuri == "F#" or molli == "d#":
                    savelet = [0, 4, 2, 5, 7, 9]
                    testaa_savelet(self, duuri, savelet, True)
                    testaa_savelet(self, molli, savelet, True)
                else:
                    savelet = [0, 2, 4, 7, 9, 11]
                    testaa_savelet(self, duuri, savelet, False)
                    testaa_savelet(self, molli, savelet, False)

            elif duuri == "Db" or duuri == "H" or molli == "b" or molli == "g#":
                if duuri == "H" or molli == "g#":
                    savelet = [0, 2, 5, 7, 9]
                    testaa_savelet(self, duuri, savelet, True)
                    testaa_savelet(self, molli, savelet, True)
                else:
                    savelet = [2, 4, 7, 9, 11]
                    testaa_savelet(self, duuri, savelet, False)
                    testaa_savelet(self, molli, savelet, False)

            elif duuri == "Ab" or duuri == "E" or molli == "f" or molli == "c#":
                if duuri == "E" or molli == "c#":
                    savelet = [0, 2, 5, 7]
                    testaa_savelet(self, duuri, savelet, True)
                    testaa_savelet(self, molli, savelet, True)
                else:
                    savelet = [2, 4, 9, 11]
                    testaa_savelet(self, duuri, savelet, False)
                    testaa_savelet(self, molli, savelet, False)

            elif duuri == "Eb" or duuri == "A" or molli == "c" or molli == "f#":
                if duuri == "A" or molli == "f#":
                    savelet = [0, 5, 7]
                    testaa_savelet(self, duuri, savelet, True)
                    testaa_savelet(self, molli, savelet, True)
                else:
                    savelet = [4, 9, 11]
                    testaa_savelet(self, duuri, savelet, False)
                    testaa_savelet(self, molli, savelet, False)

            elif duuri == "B" or duuri == "D" or molli == "g" or molli == "h":
                if duuri == "D" or molli == "h":
                    savelet = [0, 5]
                    testaa_savelet(self, duuri, savelet, True)
                    testaa_savelet(self, molli, savelet, True)
                else:
                    savelet = [4, 11]
                    testaa_savelet(self, duuri, savelet, False)
                    testaa_savelet(self, molli, savelet, False)

            elif duuri == "F" or duuri == "G" or molli == "d" or molli == "e":
                if duuri == "G" or molli == "e":
                    savelet = [5]
                    testaa_savelet(self, duuri, savelet, True)
                    testaa_savelet(self, molli, savelet, True)
                else:
                    savelet = [11]
                    testaa_savelet(self, duuri, savelet, False)
                    testaa_savelet(self, molli, savelet, False)

            elif duurit[i] == "C" or mollit[i] == "a":
                    savelet = []
                    testaa_savelet(self, duuri, savelet, True)
                    testaa_savelet(self, molli, savelet, True)
    
    def test_savel_tekstina(self):
        
        nimet = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","H"]
        nimet_ylen = ["H#","C#","D","D#","E","E#","F#","G","G#","A","A#","H"]
        nimet_alen = ["C","Db","D","Eb","Fb","F","Gb","G","Ab","A","Hb","Cb"]
        oktaavi = -1

        for i in range(11):
            for j in range(12):
                midi_arvo = j + i * 12
                if midi_arvo >= 128: # Lopetetaan silmukka
                    return

                elif midi_arvo >= 0 and midi_arvo < 128:
                    self.assertEqual(apufunktiot.Savel_Tekstina(midi_arvo, ""), (nimet[j], oktaavi), f"Midi arvo {midi_arvo} ei antanut oikeaa tulosta.")
                    self.assertEqual(apufunktiot.Savel_Tekstina(midi_arvo, "y"), (nimet_ylen[j], oktaavi), f"Ylennetty Midi arvo {midi_arvo} ei antanut oikeaa tulosta.")
                    self.assertEqual(apufunktiot.Savel_Tekstina(midi_arvo, "a"), (nimet_alen[j], oktaavi), f"Alennettu Midi arvo {midi_arvo} ei antanut oikeaa tulosta.")

            oktaavi += 1
