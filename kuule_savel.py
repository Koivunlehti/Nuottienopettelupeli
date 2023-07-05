import pygame
import pygame.midi
import random
import apufunktiot
import ui_komponentit
from pygame.locals import *

class Kuule_Savel():
    def __init__(self, midi_soitin:pygame.midi.Output, resoluutio:tuple = (1000, 800)):
        # Näyttö
        pygame.display.set_caption("Kuule oikea sävel")
        self.naytto = pygame.display.set_mode((resoluutio[0], resoluutio[1]), RESIZABLE)

        # Midi
        self.soitin = midi_soitin
        self.soitin.set_instrument(0,1)
        self.midi_alue = (60,71)
        self.midi = self.midi_alue[0]
        self.ilman_korotusta = False

        # Otsikkoteksti
        self.otsikkoteksti = "Mikä sävel?"
        self.aliteksti = ""

        # Painikkeet
        self.vastauspainikkeet = []
        self.vastauspainikkeet_hiiri_paalla = []
        self.vastauspainikkeet_vari_1 = (60,120,70)
        self.vastauspainikkeet_vari_2 = (60,170,70)
        self.vastauspainikkeet_vari_vaarin_1 = (200,50,50)
        self.vastauspainikkeet_vari_vaarin_2 = (150,50,50)
        self.vastauspainikkeet_vaarin = []
        self.savelet = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "H"]


        self.uudelleen_painike_vari_1 = (60,120,70)
        self.uudelleen_painike_vari_2 = (60,170,70)
        self.uudelleen_painike_hiiri_paalla = False

        # Oikein ja väärin
        self.oikein_vaarin_teksti = ""
        self.oikein_maara = 0
        self.vaarin_maara = 0

        # Pisteet
        self.pisteet = 0
        self.arvausmaara = 3

        # Pelitaso
        self.pelitaso = 1
        self.pelitaso_oikein_talla_tasolla = 0
        self.pelitaso_vaihda = False
        self.pelitaso_vaadittu_oikein_maara = 20

        # Sävelten soitto
        self.soita_savelet = True
        

        # Valmistaudu vaihe
        self.valmistaudu = False
        self.valmistaudu_laskuri = 3

        # Ajastimet
        self.kello = pygame.time.Clock()
        self.ajastin = 0
        self.oikein_vaarin_ajastin = 0
        
    
    def Aloita(self):
        
        self.__Tarkista_Taso()

        while True:
            # Muuttujien uudelleen alustus
            hiiri_x, hiiri_y = pygame.mouse.get_pos()
            self.naytto.fill((0, 0, 0))

            # Luodaan ylävalikkorivi
            valikko = ui_komponentit.Luo_ylavalikko_pelkistetty(self.naytto.get_width(), 1, (50,0), (60,120,70), f"Oikein: {self.oikein_maara}", f"Pisteet: {self.pisteet}", f"Väärin: {self.vaarin_maara}")
            self.naytto.blit(valikko,(0, 0))
            
            # Luodaan otsikkoteksti
            otsikko = ui_komponentit.Luo_Teksti(teksti=self.otsikkoteksti, koko=42)
            self.naytto.blit(otsikko,(self.naytto.get_width() / 2 -  otsikko.get_width() / 2, 100))
            
            # Luodaan keskialueen muuttuvia sisältöjä
            if self.valmistaudu == False and self.soita_savelet == False and self.pelitaso_vaihda == False:
                uudelleen_painike = ui_komponentit.Luo_Painike(taustavari=self.uudelleen_painike_vari_1, taustavari_hiiri_paalla=self.uudelleen_painike_vari_2, 
                                                   hiiri_paalla=self.uudelleen_painike_hiiri_paalla, teksti="Toista uudelleen", reunus=30)
                uudelleen_painike = self.naytto.blit(uudelleen_painike,(self.naytto.get_width() / 2 - uudelleen_painike.get_width() / 2, self.naytto.get_height() / 2 - uudelleen_painike.get_height() / 2))
            else:
                if self.soita_savelet == True or self.pelitaso_vaihda == True:
                    laskuri_teksti = ui_komponentit.Luo_Teksti(teksti=f"{self.aliteksti}", koko=52)
                    self.naytto.blit(laskuri_teksti,(self.naytto.get_width() / 2 -  laskuri_teksti.get_width() / 2, 200))
                elif self.valmistaudu == True:    
                    laskuri_teksti = ui_komponentit.Luo_Teksti(teksti=f"Valmistaudu ... {str(self.valmistaudu_laskuri)}", koko=42)
                    self.naytto.blit(laskuri_teksti,(self.naytto.get_width() / 2 -  laskuri_teksti.get_width() / 2, 200))

            # Luodaan Oikein ja väärin tekstit
            if self.oikein_vaarin_ajastin > 0:
                    if self.oikein_vaarin_teksti == "Oikein":
                        teksti_vari = "Green"
                    else:
                        teksti_vari = "Red"
                    oikein_vaarin_teksti = ui_komponentit.Luo_Teksti(teksti=self.oikein_vaarin_teksti, koko=42, vari=teksti_vari)
                    self.naytto.blit(oikein_vaarin_teksti,(self.naytto.get_width() / 2 - oikein_vaarin_teksti.get_width() / 2, self.naytto.get_height() - 260))

            # Luodaan vastauspainikkeet
            self.__Luo_Vastauspainikkeet()

            # Tapahtumat
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:   # Ikkunan yläkulman X painike
                    exit()

                if tapahtuma.type == pygame.KEYDOWN:    
                    if tapahtuma.key == pygame.K_ESCAPE:    # ESC-näppäin
                        return
                
                if tapahtuma.type == pygame.VIDEORESIZE:    # Ikkunan koon muutos 
                    # Ruudun minimikoko
                    if pygame.display.get_window_size()[0] < 750:
                        self.naytto = pygame.display.set_mode((750, pygame.display.get_window_size()[1]), RESIZABLE)
                    if pygame.display.get_window_size()[1] < 700:
                        self.naytto = pygame.display.set_mode((pygame.display.get_window_size()[0], 700), RESIZABLE)

                if tapahtuma.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[0] == True:    # Vasen hiiren painike alas
                    if self.valmistaudu == False and self.soita_savelet == False:
                        for i in range(len(self.vastauspainikkeet)):
                            if self.vastauspainikkeet[i][0].collidepoint(tapahtuma.pos):
                                if apufunktiot.Savel_Tekstina(self.midi)[0] == self.vastauspainikkeet[i][1]:
                                    self.valmistaudu = True
                                    self.vastauspainikkeet_vaarin = []
                                    self.otsikkoteksti = f"Sävel oli {apufunktiot.Savel_Tekstina(self.midi)[0]}"
                                    self.oikein_vaarin_teksti = "Oikein"
                                    self.oikein_vaarin_ajastin = 60
                                    self.oikein_maara += 1
                                    self.pelitaso_oikein_talla_tasolla += 1
                                    self.pisteet += self.arvausmaara * 10
                                    if self.pisteet < 0:
                                        self.pisteet = 0
                                    self.arvausmaara = 3
                                else:
                                    if self.vastauspainikkeet[i][1] not in self.vastauspainikkeet_vaarin:
                                        self.vastauspainikkeet_vaarin.append(self.vastauspainikkeet[i][1])
                                    self.oikein_vaarin_teksti = "Väärin"
                                    self.oikein_vaarin_ajastin = 60
                                    self.vaarin_maara += 1
                                    self.arvausmaara -= 1                                    

                        if uudelleen_painike.collidepoint(tapahtuma.pos):
                            self.soitin.note_off(self.midi,127,0)
                            self.soitin.note_on(self.midi,127,0)

            # Tunnistetaan onko hiiri painikkeen päällä
            for i in range(len(self.vastauspainikkeet)):
                if self.vastauspainikkeet[i][0].collidepoint((hiiri_x, hiiri_y)):
                    self.vastauspainikkeet_hiiri_paalla[i] = True
                else:
                    self.vastauspainikkeet_hiiri_paalla[i] = False

            if self.valmistaudu == False and self.soita_savelet == False:
                if uudelleen_painike.collidepoint((hiiri_x, hiiri_y)):
                    self.uudelleen_painike_hiiri_paalla = True
                else:
                    self.uudelleen_painike_hiiri_paalla = False

            # Tason vaihto
            if self.pelitaso_vaihda:
                if self.pelitaso == 1:
                    self.otsikkoteksti = f"Aloitetaan peli"
                else:
                    pass
                    #self.otsikkoteksti = f"Saavutit tason: {self.pelitaso}!"
                self.aliteksti = f"Taso {self.pelitaso}"
                if self.ajastin >= 180: 
                    self.ajastin = 0
                    self.soita_savelet = True
                    self.pelitaso_vaihda = False
                    self.midi = 60
                    self.aliteksti = ""
                else:
                    self.ajastin += 1

            # Sävelten läpisoitto 
            elif self.soita_savelet:
                self.otsikkoteksti = "Sävelten läpikäynti..."
                if self.ajastin == 60:
                    if self.midi > self.midi_alue[0]:
                        self.soitin.note_off(self.midi - 1, 127, 0)

                    if self.midi > self.midi_alue[1]:
                        self.valmistaudu = True
                        self.ajastin = 0
                        self.midi = self.midi_alue[0]
                        self.soita_savelet = False
                        self.otsikkoteksti = ""
                        
                    else:
                        self.soitin.note_on(self.midi, 127, 0)
                        self.ajastin = 0
                        self.aliteksti = apufunktiot.Savel_Tekstina(self.midi)[0]
                        self.midi += 1
                        if self.ilman_korotusta and "#" in apufunktiot.Savel_Tekstina(self.midi)[0]:
                            self.midi += 1
                else:
                    self.ajastin += 1

            # Valmistautumisvaihe
            elif self.valmistaudu:
                if self.ajastin >= 180:
                    self.valmistaudu = False
                    self.ajastin = 0
                    self.valmistaudu_laskuri = 3
                    self.__Arvo_Midi()
                    self.soitin.note_on(self.midi,127,0)
                    self.otsikkoteksti = "Mikä sävel?"
                else:
                    self.ajastin += 1
                    if self.ajastin % 60 == 0:
                        self.valmistaudu_laskuri -= 1
            else:
                pass
            
            # Tarkistetaan onko tason vaihto ajankohtainen
            if self.pelitaso_oikein_talla_tasolla >= self.pelitaso_vaadittu_oikein_maara:
                self.pelitaso += 1
                self.pelitaso_oikein_talla_tasolla = 0
                self.__Tarkista_Taso()

            # Oikein / Väärin tekstin ajastin
            if self.oikein_vaarin_ajastin > 0:
                self.oikein_vaarin_ajastin -= 1

            self.kello.tick(60)
            
            pygame.display.flip()  

    def __Arvo_Midi(self):
        if self.ilman_korotusta:
            while True:
                self.midi = random.randint(self.midi_alue[0], self.midi_alue[1])
                if "#" not in apufunktiot.Savel_Tekstina(self.midi)[0]:
                    break
        else:
            self.midi = random.randint(self.midi_alue[0], self.midi_alue[1])

    def __Luo_Vastauspainikkeet(self):
        # Muuttujien alustus
        self.vastauspainikkeet = []
        painike_vali = 10
        painike_leveys = self.naytto.get_width() / len(self.savelet) - painike_vali
        
        painike_x = self.naytto.get_width() / 2 - (len(self.savelet) / 2) * (painike_leveys + painike_vali) + (painike_vali / 2)
        
        for i in range(len(self.savelet)):
            hiiri_paalla = False

            # Jos vastauspainikkeiden "hiiri_päällä" lista on tyhjä, alustetaan se tässä False arvoilla.
            if i >= len(self.vastauspainikkeet_hiiri_paalla):    
                self.vastauspainikkeet_hiiri_paalla.append(False)

            # Havaitaan, onko hiiri luotavan painikkeen päällä
            if self.vastauspainikkeet_hiiri_paalla[i] == True:
                hiiri_paalla = True

            # Vastauspainikkeiden värimuutoksia
            if self.savelet[i] in self.vastauspainikkeet_vaarin:
                taustavari = self.vastauspainikkeet_vari_vaarin_1
                taustavari_hiiri_paalla = self.vastauspainikkeet_vari_vaarin_2
            else:
                taustavari = self.vastauspainikkeet_vari_1
                taustavari_hiiri_paalla = self.vastauspainikkeet_vari_2

            # Luodaan painike   
            painike = self.naytto.blit(ui_komponentit.Luo_Painike(taustavari=taustavari, taustavari_hiiri_paalla=taustavari_hiiri_paalla, 
                                                            hiiri_paalla=hiiri_paalla, teksti=self.savelet[i], reunus=30, leveys_x=painike_leveys), (painike_x, self.naytto.get_height() - 200))
            painike_x += painike.width + painike_vali
            self.vastauspainikkeet.append((painike, self.savelet[i]))

    def __Vastauspainikkeiden_Savelet(self, savelet:list):
        self.savelet = savelet
        self.vastauspainikkeet_hiiri_paalla = []

    def __Tarkista_Taso(self):
        if self.pelitaso == 1:
            self.pelitaso_vaihda = True
            self.__Vastauspainikkeiden_Savelet(["C", "D"])
            self.midi_alue = (60, 62)
            self.ilman_korotusta = True

        elif self.pelitaso == 2:
            self.pelitaso_vaihda = True
            self.__Vastauspainikkeiden_Savelet(["C", "D", "E"])
            self.midi_alue = (60, 64)
            self.ilman_korotusta = True
            self.valmistaudu = False
            self.soita_savelet = False

        elif self.pelitaso == 3:
            self.pelitaso_vaihda = True
            self.__Vastauspainikkeiden_Savelet(["C", "D", "E", "F"])
            self.midi_alue = (60, 65)
            self.ilman_korotusta = True
            self.valmistaudu = False
            self.soita_savelet = False

        elif self.pelitaso == 4:
            self.pelitaso_vaihda = True
            self.__Vastauspainikkeiden_Savelet(["C", "D", "E", "F", "G"])
            self.midi_alue = (60, 67)
            self.ilman_korotusta = True
            self.valmistaudu = False
            self.soita_savelet = False
        
        elif self.pelitaso == 5:
            self.pelitaso_vaihda = True
            self.__Vastauspainikkeiden_Savelet(["C", "D", "E", "F", "G", "A"])
            self.midi_alue = (60, 69)
            self.ilman_korotusta = True
            self.valmistaudu = False
            self.soita_savelet = False

        elif self.pelitaso == 6:
            self.pelitaso_vaihda = True
            self.__Vastauspainikkeiden_Savelet(["C", "D", "E", "F", "G", "A", "H"])
            self.midi_alue = (60, 71)
            self.ilman_korotusta = True
            self.valmistaudu = False
            self.soita_savelet = False

        elif self.pelitaso == 7:
            self.pelitaso_vaihda = True
            self.__Vastauspainikkeiden_Savelet(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "H"])
            self.midi_alue = (60, 71)
            self.ilman_korotusta = False
            self.valmistaudu = False
            self.soita_savelet = False

if __name__ == "__main__":
    pygame.init()
    pygame.midi.init()
    soitin = pygame.midi.Output(0)
    kuule_savel = Kuule_Savel(soitin)
    kuule_savel.Aloita()