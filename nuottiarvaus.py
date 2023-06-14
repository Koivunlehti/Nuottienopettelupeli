import pygame
import pygame.midi
from pygame.locals import *
import random
import piirto, koskettimet, apufunktiot

class Nuottiarvaus():
    def __init__(self, resoluutio:tuple = (1000, 800)):
        pygame.init()

        # Midi soittimen alustus
        pygame.midi.init()
        self.soitin = pygame.midi.Output(0)
        self.soitin.set_instrument(0,1)
        self.soitin.set_instrument(127,5)

        # Näytön alustus
        pygame.display.set_caption("Nuottiarvaus")
        self.naytto = pygame.display.set_mode((resoluutio[0], resoluutio[1]), RESIZABLE)

        # Tekstit ja fontit
        self.fontti = pygame.font.SysFont("Georgia", 48, bold=True)
        self.fontti_2 = pygame.font.SysFont("Georgia", 18, bold=True)
        self.pisteet_teksti = self.fontti.render("Pisteet: 0", True, "white")
        self.edellinen_oikea_vastaus = self.fontti.render("", True, "white")
        self.nykyinen_vastaus_teksti = ""
        self.taso_teksti = self.fontti.render("Taso: 1 (0 / 10)", True, "white")
        self.virheet_teksti = self.fontti.render("Virheet: 0 / 5", True, "white")

        # Kello
        self.kello = pygame.time.Clock()
        self.oikea_vastaus_ajastin = 0

        # Viivasto
        self.diskantti_keski_c_y = self.naytto.get_height() / 2 - 30
        self.basso_keski_c_y = self.naytto.get_height() / 2 + 30
        self.viivasto_rivivali = 20
        self.viivaston_leveys = 700
        self.viivasto_paikat = self.__Viivaston_Paikat()

        # Koskettimet
        self.alku_midi = 36
        self.loppu_midi = 84
        self.kosk_korkeus = 100
        self.koskettimet_valkoinen, self.koskettimet_musta = koskettimet.Luo_Koskettimet(self.naytto, self.alku_midi, self.loppu_midi, self.kosk_korkeus)

        # Haettavan nuotin muuttujat
        self.paikat_diskantti, self.paikat_basso = self.__Nuottien_Paikat()
        self.luo_nuotti = True
        self.piirra_ylennetty = False
        self.piirra_alennettu = False
        self.piirra_palautus = False
        self.nuotti_x = 0
        self.nuotti_y = 0
        self.nuotti_midi = 0
        self.midi_diskantti_alaraja = 57
        self.midi_basso_ylaraja = 65
        self.diskantti = True

        # Rajaviivan sijainti
        self.rajaviiva_x = self.naytto.get_width() / 2 - self.viivaston_leveys / 2 + 150
        self.rajaviiva_y = self.naytto.get_height() / 2
        self.rajaviiva_pituus_y = 400
        self.rajaviiva_paksuus = 4

        # Arvausalue
        self.arvausalue_x = self.rajaviiva_x + self.rajaviiva_paksuus
        self.arvausalue_y = self.rajaviiva_y
        self.arvausalue_leveys = 350
        self.arvausalue_korkeus = self.rajaviiva_pituus_y

        # Pisteet
        self.pisteet = 0
        self.taso = 1
        self.virhe_maara = 0
        self.oikein_maara = 0

        # Sävellaji
        self.savellaji = "C"
        self.savellajin_vaatima_tila_x = piirto.Piirra_Savellaji(self.naytto, 150, self.savellaji, self.paikat_diskantti, True, True)

    def __Viivaston_Paikat(self) -> dict:
        return {"diskantti": piirto.Piirra_Viivasto(self.naytto, self.naytto.get_width() / 2, self.diskantti_keski_c_y, self.viivasto_rivivali, self.viivaston_leveys, True), 
                "basso": piirto.Piirra_Viivasto(self.naytto, self.naytto.get_width() / 2, self.basso_keski_c_y, self.viivasto_rivivali, self.viivaston_leveys, False)}
    
    def __Nuottien_Paikat(self) -> tuple:
        return (apufunktiot.Luo_Nuottien_Paikat(self.viivasto_paikat["diskantti"][0] + self.viivasto_rivivali, 10), 
                apufunktiot.Luo_Nuottien_Paikat(self.viivasto_paikat["basso"][0] - self.viivasto_rivivali, 10))

    # Pelisilmukka
    def Aloita(self):
        while True:
            self.naytto.fill((0,0,0))
            
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:   # Ikkunan yläkulman X painike
                    exit()

                if tapahtuma.type == pygame.VIDEORESIZE:    # Ikkunan koon muutos
                    
                    # Ruudun minimikoko
                    if pygame.display.get_window_size()[0] < 750:
                        self.naytto = pygame.display.set_mode((750, pygame.display.get_window_size()[1]), RESIZABLE)
                    if pygame.display.get_window_size()[1] < 700:
                        self.naytto = pygame.display.set_mode((pygame.display.get_window_size()[0], 700), RESIZABLE)
                    # Nuotin ero rajaviivaan x-akselilla ennen ikkunan koon muutosta
                    nuotti_x_ero = self.nuotti_x - self.rajaviiva_x

                    # Tärkeiden elementtien x- ja y-koordinaattien päivitys
                    self.diskantti_keski_c_y = self.naytto.get_height() / 2 - 30
                    self.basso_keski_c_y = self.naytto.get_height() / 2 + 30
                    self.viivasto_paikat = self.__Viivaston_Paikat()
                    self.paikat_diskantti, self.paikat_basso = self.__Nuottien_Paikat()
                    self.rajaviiva_x = self.naytto.get_width() / 2 - self.viivaston_leveys / 2 + 150
                    self.rajaviiva_y = self.naytto.get_height() / 2
                    self.arvausalue_x = self.rajaviiva_x + self.rajaviiva_paksuus
                    self.arvausalue_y = self.rajaviiva_y

                    # Nuotin uudet koordinaatit 
                    self.nuotti_x = self.rajaviiva_x + nuotti_x_ero
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
                            if self.nuotti_x <= self.arvausalue_x + self.arvausalue_leveys + self.savellajin_vaatima_tila_x:
                                self.luo_nuotti = True
                                self.pisteet += 5 * self.taso
                                self.oikein_maara += 1
                                self.edellinen_oikea_vastaus = self.fontti.render(self.nykyinen_vastaus_teksti, True, "green")
                                self.oikea_vastaus_ajastin = 200
                        else:
                            if self.nuotti_x <= self.arvausalue_x + self.arvausalue_leveys + self.savellajin_vaatima_tila_x:
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
                if self.nuotti_x > self.rajaviiva_x + self.savellajin_vaatima_tila_x:
                    self.nuotti_x -= 1
                else:
                    self.luo_nuotti = True
                    self.soitin.note_off(60, 127,5)
                    self.soitin.note_on(60, 127,5)
                    self.pisteet -= 10 * self.taso
                    self.edellinen_oikea_vastaus = self.fontti.render(self.nykyinen_vastaus_teksti, True, "red")
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
                    teksti = self.fontti_2.render("C", True, "black")
                    self.naytto.blit(teksti, (kosketin[0].x + kosketin[0].width / 2 - teksti.get_width() / 2, kosketin[0].y + kosketin[0].height / 2 + 20))

            for kosketin in self.koskettimet_musta:  # Piirretään mustat koskettimet. Jos hiiri havaitaan koskettimen päällä, koskettimen väritystä muutetaan
                if kosketin[0].x <= hiiri_x <= kosketin[0].x + kosketin[0].width and kosketin[0].y <= hiiri_y <= kosketin[0].y + kosketin[0].height:
                    pygame.draw.rect(self.naytto,(140,140,140),kosketin[0])
                else:
                    pygame.draw.rect(self.naytto,(50,50,50),kosketin[0])

            self.savellajin_vaatima_tila_x = piirto.Piirra_Savellaji(self.naytto, 150, self.savellaji, self.paikat_diskantti, True, True)

            # Rajaviivan piirto
            pygame.draw.line(self.naytto, (222,40,20), (self.rajaviiva_x + self.savellajin_vaatima_tila_x, self.rajaviiva_y - self.rajaviiva_pituus_y / 2), (self.rajaviiva_x + self.savellajin_vaatima_tila_x ,self.rajaviiva_y + self.rajaviiva_pituus_y / 2), self.rajaviiva_paksuus)
            
            # Arvausalue piirto
            pygame.draw.rect(self.naytto, (6,148,3), [self.arvausalue_x + self.savellajin_vaatima_tila_x, self.arvausalue_y - self.arvausalue_korkeus / 2, self.arvausalue_leveys, self.arvausalue_korkeus])
            
            # Viivaston piirto
            piirto.Piirra_Viivasto(self.naytto, self.naytto.get_width() / 2, self.diskantti_keski_c_y, self.viivasto_rivivali, self.viivaston_leveys + self.savellajin_vaatima_tila_x, True)
            piirto.Piirra_Viivasto(self.naytto, self.naytto.get_width() / 2, self.basso_keski_c_y, self.viivasto_rivivali, self.viivaston_leveys + self.savellajin_vaatima_tila_x, False)

            # G-Nuottiavain piirto
            piirto.Piirra_G_Avain(self.naytto, self.naytto.get_width() / 2 - (self.viivaston_leveys + self.savellajin_vaatima_tila_x) / 2 + 50, self.viivasto_paikat["diskantti"][1])

            # F-Nuottiavain piirto
            piirto.Piirra_F_Avain(self.naytto, self.naytto.get_width() / 2 - (self.viivaston_leveys + self.savellajin_vaatima_tila_x) / 2 + 50, self.viivasto_paikat["basso"][1])

            # Sävellajin merkkien piirto
            piirto.Piirra_Savellaji(self.naytto, self.naytto.get_width() / 2 - (self.viivaston_leveys + self.savellajin_vaatima_tila_x) / 2 + 150, self.savellaji, self.paikat_diskantti, True)
            piirto.Piirra_Savellaji(self.naytto, self.naytto.get_width() / 2 - (self.viivaston_leveys + self.savellajin_vaatima_tila_x) / 2 + 150, self.savellaji, self.paikat_basso, False)

            # Mahdollisten apuviivojen piirto
            if self.diskantti:
                if self.nuotti_y < self.viivasto_paikat["diskantti"][4] - self.viivasto_rivivali - self.viivasto_rivivali / 2:
                    piirto.Piirra_Apuviivat(self.naytto, self.nuotti_x - 10, self.viivasto_paikat["diskantti"][4] , 50, self.viivasto_rivivali, 2, False)
                elif self.nuotti_y < self.viivasto_paikat["diskantti"][4] - self.viivasto_rivivali / 2:
                    piirto.Piirra_Apuviivat(self.naytto, self.nuotti_x - 10, self.viivasto_paikat["diskantti"][4], 50, self.viivasto_rivivali, 1, False)
                elif self.nuotti_y > self.viivasto_paikat["diskantti"][0] + self.viivasto_rivivali:
                    piirto.Piirra_Apuviivat(self.naytto, self.nuotti_x - 10, self.viivasto_paikat["diskantti"][0], 50, self.viivasto_rivivali, 2, True)
                elif self.nuotti_y > self.viivasto_paikat["diskantti"][0]:
                    piirto.Piirra_Apuviivat(self.naytto, self.nuotti_x - 10, self.viivasto_paikat["diskantti"][0], 50, self.viivasto_rivivali, 1, True)
            else:
                if self.nuotti_y < self.viivasto_paikat["basso"][0] - self.viivasto_rivivali - self.viivasto_rivivali / 2:
                    piirto.Piirra_Apuviivat(self.naytto, self.nuotti_x - 10, self.viivasto_paikat["basso"][0], 50, self.viivasto_rivivali, 2, False)
                elif self.nuotti_y < self.viivasto_paikat["basso"][0] - self.viivasto_rivivali / 2:
                    piirto.Piirra_Apuviivat(self.naytto, self.nuotti_x - 10, self.viivasto_paikat["basso"][0], 50, self.viivasto_rivivali, 1, False)
                elif self.nuotti_y > self.viivasto_paikat["basso"][4] + self.viivasto_rivivali:
                    piirto.Piirra_Apuviivat(self.naytto, self.nuotti_x - 10, self.viivasto_paikat["basso"][4], 50, self.viivasto_rivivali, 2, True)
                elif self.nuotti_y > self.viivasto_paikat["basso"][4]:
                    piirto.Piirra_Apuviivat(self.naytto, self.nuotti_x - 10, self.viivasto_paikat["basso"][4], 50, self.viivasto_rivivali, 1, True)

            # Ylennysmerkin piirto
            if self.piirra_ylennetty:
                piirto.Piirra_Ylennys(self.naytto, self.nuotti_x, self.nuotti_y, -20)
            if self.piirra_alennettu:
                piirto.Piirra_Alennus(self.naytto, self.nuotti_x, self.nuotti_y, -20)
            if self.piirra_palautus:
                piirto.Piirra_Palautus(self.naytto, self.nuotti_x, self.nuotti_y, -20)

            # Nuotti piirto
            piirto.Piirra_4_Osa_Nuotti(self.naytto, self.nuotti_x, self.nuotti_y)

            # Pisteiden piirto
            if self.pisteet < 0:
                self.pisteet = 0
            self.pisteet_teksti = self.fontti.render(f"Pisteet: {self.pisteet}", True, "white")
            self.naytto.blit(self.pisteet_teksti, (0, self.naytto.get_height() - self.kosk_korkeus - self.pisteet_teksti.get_height()))

            # Oikean vastauksen piirto
            if self.oikea_vastaus_ajastin > 0:
                self.naytto.blit(self.edellinen_oikea_vastaus, (self.naytto.get_width() - self.edellinen_oikea_vastaus.get_width(), self.naytto.get_height() - self.kosk_korkeus - self.pisteet_teksti.get_height()))
            
            # Virhelaskurin ja oikein laskurin hallintaa
            if self.virhe_maara >= 5:
                self.luo_nuotti = True
                self.virhe_maara = 0
                self.oikein_maara = 0
                self.taso -= 1
                if self.taso <= 0:
                    self.taso = 1
            if self.oikein_maara < 0:
                self.oikein_maara = 0

            # Taso tekstin piirto
            self.taso_teksti = self.fontti.render(f"Taso: {self.taso} ({self.oikein_maara}/10)", True, "white")
            self.naytto.blit(self.taso_teksti, (0, 0))

            # Virheet tekstin piirto
            self.virheet_teksti = self.fontti.render(f"Virheet: {self.virhe_maara} / 5", True, "white")
            self.naytto.blit(self.virheet_teksti, (self.naytto.get_width() - self.virheet_teksti.get_width(), 0))

            #piirto.Piirra_Tahtiviiva(naytto, naytto.get_width() / 2 - (viivaston_leveys + savellajin_vaatima_tila_x) / 2, naytto.get_height() / 2, 10 * viivasto_rivivali + 60)
            piirto.Piirra_Akkoladi(self.naytto, self.naytto.get_width() / 2 - (self.viivaston_leveys + self.savellajin_vaatima_tila_x) / 2, self.naytto.get_height() / 2, 10 * self.viivasto_rivivali + 60)
            piirto.Piirra_Paatosviiva(self.naytto, self.naytto.get_width() / 2 + (self.viivaston_leveys + self.savellajin_vaatima_tila_x) / 2, self.naytto.get_height() / 2, 10 * self.viivasto_rivivali + 60)

            pygame.display.flip()

            # Kellon ja ajastimien edistäminen.
            self.kello.tick(60)
            if self.oikea_vastaus_ajastin > 0:
                self.oikea_vastaus_ajastin -= 1
    

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
        taso_savellajit = [("Cb","ab"), ("Db","eb"), ("Db","b"), ("Ab","f"), ("Eb","c"), ("B","g"), ("F","d"), 
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
        
        self.savel_tekstina = apufunktiot.Savel_Tekstina(self.nuotti_midi)

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
        self.nuotti_x = self.arvausalue_x + self.arvausalue_leveys + self.savellajin_vaatima_tila_x + 100
        self.luo_nuotti = False

        # oikea vastaussävel tekstimuodossa talteen
        self.nykyinen_vastaus_teksti = self.savel_tekstina[0] + " " + str(self.savel_tekstina[1])

    def __Arvo_Nuotti(self, midi_alaraja, midi_ylaraja, paikat):
        self.nuotti_midi = random.randrange(midi_alaraja, midi_ylaraja)
        kosketin_vari = paikat[self.nuotti_midi][1]
        if kosketin_vari == "m":
            self.nuotti_midi -= 1
        self.nuotti_y = paikat[self.nuotti_midi][0]

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