import pygame
import pygame.midi
from pygame.locals import *
import random
import nuottikirjoitus, koskettimet, apufunktiot, ui_komponentit

class Nuottiarvaus():
    def __init__(self, midi_soitin:pygame.midi.Output, resoluutio:tuple = (1000, 800)):

        # Midi soittimen alustus
        self.soitin = midi_soitin
        self.soitin.set_instrument(0,1)
        self.soitin.set_instrument(127,5)

        # Näytön alustus
        pygame.display.set_caption("Nuottiarvaus")
        self.naytto = pygame.display.set_mode(resoluutio, RESIZABLE)

        # Kello
        self.kello = pygame.time.Clock()
        self.oikea_vastaus_ajastin = 0

        # Viivasto
        self.viivasto_etaisyys_y = 30
        self.diskantti_keski_c_y = self.naytto.get_height() / 2 - self.viivasto_etaisyys_y
        self.basso_keski_c_y = self.naytto.get_height() / 2 + self.viivasto_etaisyys_y
        self.viivasto_rivivali = 20
        self.viivaston_leveys = 700
        self.merkkien_valinen_tila = 20

        # Koskettimet
        self.alku_midi = 36
        self.loppu_midi = 84
        self.kosk_korkeus = 100
        self.koskettimet_valkoinen, self.koskettimet_musta = koskettimet.Luo_Koskettimet(self.naytto, self.alku_midi, self.loppu_midi, self.kosk_korkeus)

        # Haettavan nuotin muuttujat
        self.paikat_diskantti, self.paikat_basso = self.__Nuottien_Paikat(self.viivasto_rivivali)
        self.luo_nuotti = True
        self.piirra_ylennetty = False
        self.piirra_alennettu = False
        self.piirra_palautus = False
        self.diskantti = True
        self.nuotti_x = 0
        self.nuotti_alku_x = 0
        self.nuotti_y = 0
        self.nuotin_ja_merkin_ero_x = 10
        self.nuotti_midi = 0
        self.midi_diskantti_alaraja = 57
        self.midi_basso_ylaraja = 65
        self.nuotin_vari = (200,200,200)
        
        # Rajaviivan sijainti
        self.rajaviiva_x = 0
        self.rajaviiva_paksuus = 4

        # Pisteet
        self.pisteet = 0
        self.taso = 1
        self.virhe_maara = 0
        self.oikein_maara = 0

        # Sävellaji
        self.savellaji = "C"

    def __Nuottien_Paikat(self, rivivali) -> tuple:
        return (apufunktiot.Luo_Nuottien_Paikat(self.diskantti_keski_c_y, rivivali / 2), 
                apufunktiot.Luo_Nuottien_Paikat(self.basso_keski_c_y, rivivali / 2))

    # Pelisilmukka
    def Aloita(self):
        
        while True:
            self.naytto.fill((0,0,0))
            naytto_vanha_koko = self.naytto.get_size()

            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:   # Ikkunan yläkulman X painike
                    exit() 
                
                if tapahtuma.type == pygame.KEYDOWN:    
                    if tapahtuma.key == pygame.K_ESCAPE:    # ESC-näppäin
                        return # suljetaan pelisilmukka return-lauseella, jonka jälkeen alkuvalikon suoritus jatkuu
                    
                if tapahtuma.type == pygame.VIDEORESIZE:    # Ikkunan koon muutos
                    
                    # Ruudun minimikoko
                    if pygame.display.get_window_size()[0] < 750:
                        self.naytto = pygame.display.set_mode((750, pygame.display.get_window_size()[1]), RESIZABLE)
                    if pygame.display.get_window_size()[1] < 700:
                        self.naytto = pygame.display.set_mode((pygame.display.get_window_size()[0], 700), RESIZABLE)

                    # Nuotin ero rajaviivaan x-akselilla ennen ikkunan koon muutosta
                    nuotti_x_ero = self.nuotti_x - naytto_vanha_koko[0] / 2 

                    # Tärkeiden elementtien x- ja y-koordinaattien päivitys
                    self.diskantti_keski_c_y = self.naytto.get_height() / 2 - self.viivasto_etaisyys_y
                    self.basso_keski_c_y = self.naytto.get_height() / 2 + self.viivasto_etaisyys_y
                    self.paikat_diskantti, self.paikat_basso = self.__Nuottien_Paikat(self.viivasto_rivivali)
                    self.rajaviiva_x = 0

                    # Nuotin uudet koordinaatit 
                    self.nuotti_x = self.naytto.get_width() / 2 + nuotti_x_ero
                    self.nuotti_alku_x = self.nuotti_alku_x + (self.naytto.get_width() - naytto_vanha_koko[0]) / 2
                    
                    if self.diskantti:
                        self.nuotti_y = self.paikat_diskantti[self.nuotti_midi][0]
                    else:
                        self.nuotti_y = self.paikat_basso[self.nuotti_midi][0]
                    
                    # Koskettimien uudet koordinaatit
                    self.koskettimet_valkoinen, self.koskettimet_musta = koskettimet.Luo_Koskettimet(self.naytto, self.alku_midi, self.loppu_midi, self.kosk_korkeus)

                if tapahtuma.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[0] == True:    # Hiiren vasen painike alhaalla
                    
                    def Koskettimen_Tapahtuma(kosketin):
                        self.soitin.note_off(kosketin[1], 127, 1)
                        self.soitin.note_on(kosketin[1], 127, 1)

                        # Painetun koskettimen vertaaminen haettavaan nuottiin
                        if kosketin[1] == self.nuotti_midi:
                            self.luo_nuotti = True
                            self.pisteet += 5 * self.taso
                            self.oikein_maara += 1
                            #self.edellinen_oikea_vastaus = self.fontti.render(self.nykyinen_vastaus_teksti, True, "green")
                            self.edellinen_oikea_vastaus = (self.nykyinen_vastaus_teksti, "green")
                            self.oikea_vastaus_ajastin = 200
                        else:
                            self.pisteet -= 5 * self.taso
                            self.oikein_maara -= 1
                            self.virhe_maara += 1

                    musta_klikattu = False
                    for kosketin in self.koskettimet_musta:
                        if kosketin[0].collidepoint(tapahtuma.pos):
                            musta_klikattu = True
                            Koskettimen_Tapahtuma(kosketin)
                            break

                    if musta_klikattu == False:
                        for kosketin in self.koskettimet_valkoinen:
                            if kosketin[0].collidepoint(tapahtuma.pos):
                                Koskettimen_Tapahtuma(kosketin)
                                break

            # Uuden nuotin luominen ja liikutus
            if self.luo_nuotti:
                self.__Luo_Nuotti()

            else:
                if self.nuotti_x > self.rajaviiva_x:
                    self.nuotti_x -= 1

                    # Nuotin väriarvon laskeminen
                    prosentti = (self.nuotti_x - self.rajaviiva_x) * 100 / (self.nuotti_alku_x - self.rajaviiva_x)  # Prosenttimäärä siitä, missä kohtaa nuotti on matkalla alkupaikan ja rajaviivan välillä.
                    prosentti -= 50                                                                                 # Vähennetään prosenttimäärää 50:llä, jotta saadaan arvot 50 - (-50).
                    if prosentti < 0:                                                                               # Kun arvot menevät negatiiviseksi, käännetään ne positiiviseksi.
                        prosentti *= -1
                    vari_arvo = 200 - 200/50 * prosentti                                                            # Lasketaan väriarvo. Käytetään jakajana lukua 50 luvun 100 sijaan, jotta saadaan kaikki arvot 220-0 välillä
                    # tarkistetaan sopiva arvo
                    if vari_arvo < 0:
                        vari_arvo *= -1
                    if vari_arvo > 255:  
                        vari_arvo = 255
                    # Nuotin puolessa matkassa vaihdetaan värin muutoksen kohdetta
                    if self.nuotti_x - self.rajaviiva_x > (self.nuotti_alku_x - self.rajaviiva_x) / 2:
                        self.nuotin_vari = (vari_arvo, 200, 20)
                    else:
                        self.nuotin_vari = (200, vari_arvo, 20)

                else:
                    self.luo_nuotti = True
                    self.soitin.note_off(60, 127,5)
                    self.soitin.note_on(60, 127,5)
                    self.pisteet -= 10 * self.taso
                    #self.edellinen_oikea_vastaus = self.fontti.render(self.nykyinen_vastaus_teksti, True, "red")
                    self.edellinen_oikea_vastaus = (self.nykyinen_vastaus_teksti, "red")
                    self.oikea_vastaus_ajastin = 200
                    self.virhe_maara += 1
                    self.oikein_maara -= 1

            # Koskettimien piirto 
            hiiri_x, hiiri_y = pygame.mouse.get_pos()
            hiiri_mustan_paalla = False 

            for kosketin in self.koskettimet_musta:  # Tarkistetaan onko hiiri mustan koskettimen päällä. Tämä pitää huomioida koska mustat ja valkoiset koskettimet ovat päällekkäin
                if kosketin[0].x <= hiiri_x <= kosketin[0].x + kosketin[0].width and kosketin[0].y <= hiiri_y <= kosketin[0].y + kosketin[0].height:
                    hiiri_mustan_paalla = True
                    break

            for kosketin in self.koskettimet_valkoinen:  # Piirretään valkoiset koskettimet ensin. Jos hiiri havaitaan koskettimen päällä, koskettimen väritystä muutetaan 
                if kosketin[0].x <= hiiri_x <= kosketin[0].x + kosketin[0].width and kosketin[0].y <= hiiri_y <= kosketin[0].y + kosketin[0].height and hiiri_mustan_paalla == False:
                    pygame.draw.rect(self.naytto,(140,140,140),kosketin[0])
                else:
                    pygame.draw.rect(self.naytto,(240,240,240),kosketin[0])
                if kosketin[1] == 60:   # Piirretään keski-C kirjain
                    keski_c = ui_komponentit.Luo_Teksti(teksti="C", vari="black", koko=26)
                    self.naytto.blit(keski_c, (kosketin[0].x + kosketin[0].width / 2 - keski_c.get_width() / 2, kosketin[0].y + kosketin[0].height / 2 + 18))

            for kosketin in self.koskettimet_musta:  # Piirretään mustat koskettimet. Jos hiiri havaitaan koskettimen päällä, koskettimen väritystä muutetaan
                if kosketin[0].x <= hiiri_x <= kosketin[0].x + kosketin[0].width and kosketin[0].y <= hiiri_y <= kosketin[0].y + kosketin[0].height:
                    pygame.draw.rect(self.naytto,(140,140,140),kosketin[0])
                else:
                    pygame.draw.rect(self.naytto,(50,50,50),kosketin[0])

            # GRAFIIKAN LUONTIA

            viivasto_diskantti = nuottikirjoitus.Luo_Viivasto(self.viivaston_leveys, self.viivasto_rivivali)
            viivasto_basso = nuottikirjoitus.Luo_Viivasto(self.viivaston_leveys, self.viivasto_rivivali)
            akkoladi = nuottikirjoitus.Luo_Akkoladi(self.paikat_basso[43][0] - self.paikat_diskantti[77][0])
            paatosviiva = nuottikirjoitus.Luo_Paatosviiva(self.paikat_basso[43][0] - self.paikat_diskantti[77][0])
            g_avain, g_korjaus = nuottikirjoitus.Luo_G_Avain()
            f_avain, f_korjaus = nuottikirjoitus.Luo_F_Avain()
            savellaji, savellaji_korjaus = nuottikirjoitus.Luo_Savellaji(self.savellaji, self.viivasto_rivivali)

            self.naytto.blit(viivasto_diskantti,(self.naytto.get_width() / 2 - viivasto_diskantti.get_width() / 2, self.paikat_diskantti[77][0]))
            self.naytto.blit(viivasto_basso,(self.naytto.get_width() / 2 - viivasto_basso.get_width() / 2, self.paikat_basso[57][0]))
            self.naytto.blit(akkoladi, (self.naytto.get_width() / 2 - self.viivaston_leveys / 2 - akkoladi.get_width(), self.paikat_diskantti[77][0]))
            self.naytto.blit(paatosviiva,(self.naytto.get_width() / 2 + self.viivaston_leveys / 2 - paatosviiva.get_width(), self.paikat_diskantti[77][0]))
            g_avain = self.naytto.blit(g_avain,(self.naytto.get_width() / 2 - self.viivaston_leveys / 2 + self.merkkien_valinen_tila, self.paikat_diskantti[67][0] - g_korjaus))
            f_avain = self.naytto.blit(f_avain,(self.naytto.get_width() / 2 - self.viivaston_leveys / 2 + self.merkkien_valinen_tila, self.paikat_basso[53][0] - f_korjaus))
            self.naytto.blit(savellaji, (g_avain.x + g_avain.width + self.merkkien_valinen_tila, self.paikat_diskantti[77][0] - savellaji_korjaus))
            savellaji = self.naytto.blit(savellaji, (g_avain.x + g_avain.width + self.merkkien_valinen_tila, self.paikat_basso[53][0] - savellaji_korjaus))

            raja_viiva = pygame.draw.line(self.naytto, (222,40,20), (g_avain.x + g_avain.width + 220, self.paikat_diskantti[90][0]), (g_avain.x + g_avain.width + 220, self.paikat_basso[32][0]), self.rajaviiva_paksuus)
            self.rajaviiva_x = raja_viiva.x

            # Apuviivat
            if self.diskantti:
                if self.nuotti_y <= self.paikat_diskantti[77][0]:
                    viiva_maara = int((self.paikat_diskantti[77][0] - self.nuotti_y) / self.viivasto_rivivali)
                    apuviivat = nuottikirjoitus.Luo_Apuviivat(60, self.viivasto_rivivali, viiva_maara, True)
                    self.naytto.blit(apuviivat,(self.nuotti_x - apuviivat.get_width() / 4, self.paikat_diskantti[77][0] - apuviivat.get_height()))
                elif self.nuotti_y >= self.paikat_diskantti[64][0]:
                    viiva_maara = int((self.nuotti_y - self.paikat_diskantti[64][0]) / self.viivasto_rivivali)
                    apuviivat = nuottikirjoitus.Luo_Apuviivat(60, self.viivasto_rivivali, viiva_maara)
                    self.naytto.blit(apuviivat,(self.nuotti_x - apuviivat.get_width() / 4, self.paikat_diskantti[64][0]))
            else:
                if self.nuotti_y <= self.paikat_basso[57][0]:
                    viiva_maara = int((self.paikat_basso[57][0] - self.nuotti_y) / self.viivasto_rivivali)
                    apuviivat = nuottikirjoitus.Luo_Apuviivat(60, self.viivasto_rivivali, viiva_maara, True)
                    self.naytto.blit(apuviivat,(self.nuotti_x - apuviivat.get_width() / 4, self.paikat_basso[57][0] - apuviivat.get_height()))
                elif self.nuotti_y >= self.paikat_basso[43][0]:
                    viiva_maara = int((self.nuotti_y - self.paikat_basso[43][0]) / self.viivasto_rivivali)
                    apuviivat = nuottikirjoitus.Luo_Apuviivat(60, self.viivasto_rivivali, viiva_maara)
                    self.naytto.blit(apuviivat,(self.nuotti_x - apuviivat.get_width() / 4, self.paikat_basso[43][0]))        

            # Ylennys, alennus ja palautus
            if self.piirra_ylennetty:
                ylennys, ylennys_korjaus = nuottikirjoitus.Luo_Ylennys()
                self.naytto.blit(ylennys, (self.nuotti_x - ylennys.get_width() - self.nuotin_ja_merkin_ero_x, self.nuotti_y - ylennys_korjaus))
            if self.piirra_alennettu:
                alennus, alennus_korjaus = nuottikirjoitus.Luo_Alennus()
                self.naytto.blit(alennus, (self.nuotti_x - alennus.get_width() - self.nuotin_ja_merkin_ero_x, self.nuotti_y - alennus_korjaus))
            if self.piirra_palautus:
                palautus, palautus_korjaus = nuottikirjoitus.Luo_Palautus()
                self.naytto.blit(palautus,(self.nuotti_x - palautus.get_width() - self.nuotin_ja_merkin_ero_x, self.nuotti_y - palautus_korjaus))

            # Nuotti
            nuotti, nuotti_korjaus = nuottikirjoitus.Luo_4_Osa_Nuotti(vari = self.nuotin_vari)
            self.naytto.blit(nuotti,(self.nuotti_x, self.nuotti_y - nuotti_korjaus))
           
           # Ylävalikko
            yla_valikko = ui_komponentit.Luo_ylavalikko_pelkistetty(leveys = self.naytto.get_width(), reunus=(20,0), taustavari="dark green", 
                                                                    teksti_vasen=f"Oikein: {self.oikein_maara}/10", teksti_keski=f"Taso: {self.taso}", 
                                                                    teksti_oikea=f"Virheet: {self.virhe_maara}/5", teksti_koko=40)
            self.naytto.blit(yla_valikko,(0,0))
            
            # Pisteet
            if self.pisteet < 0:
                self.pisteet = 0
            pisteet_teksti = ui_komponentit.Luo_Teksti(teksti=f"Pisteet: {self.pisteet}", koko=42, lihavoitu=True)
            self.naytto.blit(pisteet_teksti,(20,yla_valikko.get_height()))

            # Oikean vastaus
            if self.oikea_vastaus_ajastin > 0:
                oikea_vastaus = ui_komponentit.Luo_Teksti(teksti=self.edellinen_oikea_vastaus[0], koko=52, vari=self.edellinen_oikea_vastaus[1])
                self.naytto.blit(oikea_vastaus, (self.naytto.get_width() / 2 - oikea_vastaus.get_width() / 2, self.naytto.get_height() / 8))
            
            # Virhelaskurin ja oikein laskurin hallintaa
            self.__Virhelaskuri()
            
            if self.oikein_maara < 0:
                self.oikein_maara = 0

            pygame.display.flip()

            # Kellon ja ajastimien edistäminen.
            self.kello.tick(60)
            if self.oikea_vastaus_ajastin > 0:
                self.oikea_vastaus_ajastin -= 1
    
    def __Virhelaskuri(self):
        if self.virhe_maara >= 5:
            self.luo_nuotti = True
            self.virhe_maara = 0
            self.oikein_maara = 0
            self.taso -= 1
            if self.taso <= 0:
                self.taso = 1

    def __Luo_Nuotti(self):
        self.piirra_ylennetty = False
        self.piirra_alennettu = False
        self.piirra_palautus = False
        self.savellaji = "C"

        # Tason muokkaamat muutujat
        taso_vain_diskantti = False
        taso_vain_basso = False
        taso_vain_ylennykset = False
        taso_vain_alennukset = False
        taso_ylen_ja_alen = False
        taso_diskantti_alaraja = self.midi_diskantti_alaraja
        taso_diskantti_ylaraja = self.loppu_midi
        taso_basso_alaraja = self.alku_midi
        taso_basso_ylaraja = self.midi_basso_ylaraja
        taso_savellajit = [("Cb","ab"), ("Gb","eb"), ("Db","b"), ("Ab","f"), ("Eb","c"), ("B","g"), ("F","d"), 
                        ("C","a"), 
                        ("G","e"), ("D","h"), ("A","f#"), ("E","c#"), ("H","g#"), ("F#","d#"), ("C#","a#")]
        
        if self.oikein_maara >= 10:
            self.taso += 1
            self.virhe_maara = 0
            self.oikein_maara = 0

        # Tasokohtaiset muutokset
        if self.taso == 1:
            taso_vain_diskantti = True
            taso_diskantti_alaraja = 60
            taso_diskantti_ylaraja = 72
        elif self.taso == 2:
            taso_vain_diskantti = True
        elif self.taso == 3:
            taso_vain_basso = True
            taso_basso_alaraja = 48
            taso_basso_ylaraja = 60
        elif self.taso == 4:
            taso_vain_basso = True
        elif self.taso == 5:
            taso_vain_ylennykset = True
        elif self.taso == 6:
            taso_vain_alennukset = True
        elif self.taso == 7:
            taso_ylen_ja_alen = True
        elif self.taso == 8:
            if random.choice([True, False]):
                self.savellaji = taso_savellajit[len(taso_savellajit) // 2 - 1][random.randrange(0,2)]
            else:
                self.savellaji = taso_savellajit[len(taso_savellajit) // 2 + 1][random.randrange(0,2)]
        elif self.taso == 9:
            if random.choice([True, False]):
                self.savellaji = taso_savellajit[len(taso_savellajit) // 2 - 2][random.randrange(0,2)]
            else:
                self.savellaji = taso_savellajit[len(taso_savellajit) // 2 + 2][random.randrange(0,2)]
        elif self.taso == 10:
            if random.choice([True, False]):
                self.savellaji = taso_savellajit[len(taso_savellajit) // 2 - 3][random.randrange(0,2)]
            else:
                self.savellaji = taso_savellajit[len(taso_savellajit) // 2 + 3][random.randrange(0,2)]
        elif self.taso == 11:
            if random.choice([True, False]):
                self.savellaji = taso_savellajit[len(taso_savellajit) // 2 - 4][random.randrange(0,2)]
            else:
                self.savellaji = taso_savellajit[len(taso_savellajit) // 2 + 4][random.randrange(0,2)]
        elif self.taso == 12:
            if random.choice([True, False]):
                self.savellaji = taso_savellajit[len(taso_savellajit) // 2 - 5][random.randrange(0,2)]
            else:
                self.savellaji = taso_savellajit[len(taso_savellajit) // 2 + 5][random.randrange(0,2)]
        elif self.taso == 13:
            if random.choice([True, False]):
                self.savellaji = taso_savellajit[len(taso_savellajit) // 2 - 6][random.randrange(0,2)]
            else:
                self.savellaji = taso_savellajit[len(taso_savellajit) // 2 + 6][random.randrange(0,2)]
        elif self.taso == 14:
            if random.choice([True, False]):
                self.savellaji = taso_savellajit[len(taso_savellajit) // 2 - 7][random.randrange(0,2)]
            else:
                self.savellaji = taso_savellajit[len(taso_savellajit) // 2 + 7][random.randrange(0,2)]
        else:
            if random.choice([True, False]):
                self.savellaji = taso_savellajit[len(taso_savellajit) // 2 - random.randrange(0,8)][random.randrange(0,2)]
            else:
                self.savellaji = taso_savellajit[len(taso_savellajit) // 2 + random.randrange(0,8)][random.randrange(0,2)]
            taso_ylen_ja_alen = True
        
        # Arvotaan nuotin sävel diskantti- tai bassoviivastolta. (0 = diskantti, 1 = basso)
        if taso_vain_diskantti:
            diskantti_vai_basso = 0
        elif taso_vain_basso:
            diskantti_vai_basso = 1
        else:
            diskantti_vai_basso = random.randrange(0,2)

        if diskantti_vai_basso == 0:
            self.__Arvo_Nuotti(taso_diskantti_alaraja, taso_diskantti_ylaraja, self.paikat_diskantti)
            self.diskantti = True
        else:
            self.__Arvo_Nuotti(taso_basso_alaraja, taso_basso_ylaraja, self.paikat_basso)
            self.diskantti = False

        # Lisätään sävellajin vaikutus nuotteihin. Tarkistetaan myös että sävel ei mene asetettujen midi arvo rajojen yli
        savellaji_vaikutus = apufunktiot.Tarkista_Savellaji_Vaikutus(self.savellaji, self.nuotti_midi)
        
        if savellaji_vaikutus == "y":
            self.__Savellajin_Vaikutus_Ylennys(taso_diskantti_ylaraja, taso_basso_ylaraja)
        elif savellaji_vaikutus == "a":
            self.__Savellajin_Vaikutus_Alennus(taso_diskantti_alaraja, taso_basso_alaraja)

        # Nuotin ylennys tai alennus
        if self.piirra_palautus == False:
            
            # Arvotaan ylennetäänkö, alennetaanko vai pidetäänkö nuotti normaalina. (0 = normaali, 1 = ylennetty, 2 = alennettu)
            muutos = 0
            if taso_vain_ylennykset:
                if random.choice([True, False]):
                    muutos = 1
            elif taso_vain_alennukset:
                if random.choice([True, False]):
                    muutos = 2
            elif taso_ylen_ja_alen:
                muutos = random.randrange(0, 3)

            if muutos == 1:
                self.__Nuotti_Ylennys(savellaji_vaikutus, taso_diskantti_ylaraja, taso_basso_ylaraja)

            elif muutos == 2:
                self.__Nuotti_Alennus(savellaji_vaikutus, taso_diskantti_alaraja, taso_basso_alaraja)
        
        # nuotin luontietäisyyys x-akselilla
        self.nuotti_x = self.naytto.get_width() / 2 + self.viivaston_leveys / 2 - 20
        self.nuotti_alku_x = self.nuotti_x
        self.luo_nuotti = False

        # oikea vastaussävel tekstimuodossa talteen
        self.nykyinen_vastaus_teksti = self.savel_tekstina[0] + " " + str(self.savel_tekstina[1])

    def __Arvo_Nuotti(self, midi_alaraja, midi_ylaraja, paikat):
        self.nuotti_midi = random.randint(midi_alaraja, midi_ylaraja)
        kosketin_vari = paikat[self.nuotti_midi][1]
        if kosketin_vari == "m":
            self.nuotti_midi -= 1
        self.nuotti_y = paikat[self.nuotti_midi][0]
        self.savel_tekstina = apufunktiot.Savel_Tekstina(self.nuotti_midi)

    def __Savellajin_Vaikutus_Ylennys(self, midi_diskantti_ylaraja, midi_basso_ylaraja):
        if self.diskantti and self.nuotti_midi + 1 <= midi_diskantti_ylaraja:
            self.nuotti_midi += 1
            self.savel_tekstina = apufunktiot.Savel_Tekstina(self.nuotti_midi,"y")
        elif not self.diskantti and self.nuotti_midi + 1 <= midi_basso_ylaraja:
            self.nuotti_midi += 1
            self.savel_tekstina = apufunktiot.Savel_Tekstina(self.nuotti_midi,"y")
        else:
            self.piirra_palautus = True
            self.savel_tekstina = apufunktiot.Savel_Tekstina(self.nuotti_midi)
    
    def __Savellajin_Vaikutus_Alennus(self, midi_diskantti_alaraja, midi_basso_alaraja):
        if self.diskantti and self.nuotti_midi - 1 >= midi_diskantti_alaraja:
            self.nuotti_midi -= 1
            self.savel_tekstina = apufunktiot.Savel_Tekstina(self.nuotti_midi,"a")
        elif not self.diskantti and self.nuotti_midi - 1 >= midi_basso_alaraja:
            self.nuotti_midi -= 1
            self.savel_tekstina = apufunktiot.Savel_Tekstina(self.nuotti_midi,"a")
        else:
            self.piirra_palautus = True
            self.savel_tekstina = apufunktiot.Savel_Tekstina(self.nuotti_midi)

    def __Nuotti_Ylennys(self, savellaji_vaikutus, midi_diskantti_ylaraja, midi_basso_ylaraja):
        if self.diskantti and self.nuotti_midi + 1 <= midi_diskantti_ylaraja:
            self.nuotti_midi += 1
            if savellaji_vaikutus == "a":
                self.piirra_palautus = True
                self.savel_tekstina = apufunktiot.Savel_Tekstina(self.nuotti_midi)
            else:
                self.piirra_ylennetty = True
                self.savel_tekstina = apufunktiot.Savel_Tekstina(self.nuotti_midi,"y")
        elif not self.diskantti and self.nuotti_midi + 1 <= midi_basso_ylaraja:
            self.nuotti_midi += 1
            if savellaji_vaikutus == "a":
                self.piirra_palautus = True
                self.savel_tekstina = apufunktiot.Savel_Tekstina(self.nuotti_midi)
            else:
                self.piirra_ylennetty = True
                self.savel_tekstina = apufunktiot.Savel_Tekstina(self.nuotti_midi,"y")
    
    def __Nuotti_Alennus(self, savellaji_vaikutus, midi_diskantti_alaraja, midi_basso_alaraja):
        if self.diskantti and self.nuotti_midi - 1 >= midi_diskantti_alaraja:
            self.nuotti_midi -= 1
            if savellaji_vaikutus == "y":
                self.piirra_palautus = True
                self.savel_tekstina = apufunktiot.Savel_Tekstina(self.nuotti_midi)
            else:
                self.piirra_alennettu = True
                self.savel_tekstina = apufunktiot.Savel_Tekstina(self.nuotti_midi,"a")
        elif not self.diskantti and self.nuotti_midi - 1 >= midi_basso_alaraja:
            self.nuotti_midi -= 1
            if savellaji_vaikutus == "y":
                self.piirra_palautus = True
                self.savel_tekstina = apufunktiot.Savel_Tekstina(self.nuotti_midi)
            else:
                self.piirra_alennettu = True
                self.savel_tekstina = apufunktiot.Savel_Tekstina(self.nuotti_midi,"a")


# if __name__ == "__main__":
#     pygame.init()
#     pygame.midi.init()
#     soitin = pygame.midi.Output(0)
#     kuule_savel = Nuottiarvaus(soitin)
#     kuule_savel.Aloita()