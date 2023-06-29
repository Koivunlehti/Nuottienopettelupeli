import pygame
import pygame.midi
from pygame.locals import *

class Kuule_Savel():
    def __init__(self, midi_soitin:pygame.midi.Output, resoluutio:tuple = (1000, 800)):
        # Näyttö
        pygame.display.set_caption("Kuule oikea sävel")
        self.naytto = pygame.display.set_mode((resoluutio[0], resoluutio[1]), RESIZABLE)

        # Midi
        self.soitin = midi_soitin
        self.soitin.set_instrument(0,1)
        self.midi = 0

        self.vastauspainikkeet = []
        self.vastauspainikkeet_hiiri_paalla = []
        self.vastauspainikkeet_vari_1 = (60,120,70)
        self.vastauspainikkeet_vari_2 = (60,170,70)

        self.uudelleen_painike_vari_1 = (60,120,70)
        self.uudelleen_painike_vari_2 = (60,170,70)
        self.uudelleen_painike_hiiri_paalla = False

        # Ajastimet
        self.kello = pygame.time.Clock()       
        self.laskuri = 0
        
    
    def Aloita(self):

        while True:
            # Muuttujien uudelleen alustus
            hiiri_x, hiiri_y = pygame.mouse.get_pos()
            self.vastauspainikkeet = []
            self.naytto.fill((0, 0, 0))

            # Luodaan ja päivitetään vastauspainikkeet
            savelet = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "H"]
            painike_leveys = 60
            painike_vali = 10
            painike_x = self.naytto.get_width() / 2 - 6 * (painike_leveys + painike_vali)
            for i in range(12):
                hiiri_paalla = False
                if i >= len(self.vastauspainikkeet_hiiri_paalla):
                    self.vastauspainikkeet_hiiri_paalla.append(False)

                if self.vastauspainikkeet_hiiri_paalla[i] == True:
                    hiiri_paalla = True

                painike = self.naytto.blit(self.__Luo_Painike(taustavari= self.vastauspainikkeet_vari_1, taustavari_hiiri_paalla=self.vastauspainikkeet_vari_2, 
                                                                hiiri_paalla=hiiri_paalla, teksti=savelet[i], reunus=30, leveys_x=painike_leveys), (painike_x, self.naytto.get_height() - 200))
                painike_x += painike.width + painike_vali
                self.vastauspainikkeet.append((painike, savelet[i]))
            
            otsikko = self.__Luo_Teksti(teksti="Mikä sävel?", teksti_koko=42)
            self.naytto.blit(otsikko,(self.naytto.get_width() / 2 -  otsikko.get_width() / 2, 100))

            uudelleen_painike = self.__Luo_Painike(taustavari=self.uudelleen_painike_vari_1, taustavari_hiiri_paalla=self.uudelleen_painike_vari_2, 
                                                   hiiri_paalla=self.uudelleen_painike_hiiri_paalla, teksti="Toista uudelleen", reunus=30)
            uudelleen_painike = self.naytto.blit(uudelleen_painike,(self.naytto.get_width() / 2 - uudelleen_painike.get_width() / 2, self.naytto.get_height() / 2 - uudelleen_painike.get_height() / 2))
            
            # Tapahtumat
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:   # Ikkunan yläkulman X painike
                    return
                
                if tapahtuma.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[0] == True:    # Vasen hiiren painike alas
                    for i in range(len(self.vastauspainikkeet)):
                        if self.vastauspainikkeet[i][0].collidepoint(tapahtuma.pos):
                            print(self.vastauspainikkeet[i][1])
                    if uudelleen_painike.collidepoint(tapahtuma.pos):
                        print("toista uudelleen")

            # Tunnistetaan onko hiiri painikkeen päällä
            for i in range(len(self.vastauspainikkeet)):
                if self.vastauspainikkeet[i][0].collidepoint((hiiri_x, hiiri_y)):
                    self.vastauspainikkeet_hiiri_paalla[i] = True
                else:
                    self.vastauspainikkeet_hiiri_paalla[i] = False

            if uudelleen_painike.collidepoint((hiiri_x, hiiri_y)):
                self.uudelleen_painike_hiiri_paalla = True
            else:
                self.uudelleen_painike_hiiri_paalla = False

            # if self.laskuri == 60:
            #     if self.midi -1 < 0:
            #         self.soitin.note_off(127,127,0)
            #     else: 
            #         self.soitin.note_off(self.midi - 1)
            #     self.soitin.note_on(self.midi,127,0)
            #     self.laskuri = 0
            #     self.midi += 1
                
                
            #     if self.midi == 128:
            #         self.midi = 0
                
            # else:
            #     self.laskuri += 1

            self.kello.tick(60)
            
            pygame.display.flip()  

    def __Luo_Painike(self, taustavari:str|tuple = None, taustavari_hiiri_paalla:str|tuple = None, hiiri_paalla:bool = False, leveys_x:float|None = None,
                      fontti:str = "Georgia", teksti:str = "", teksti_koko:int = 32, lihavoitu:bool = False, kursivoitu = False, 
                      teksti_vari:str|tuple = "white", reunus:float = 0) -> pygame.Surface:
        """ Luo painikkeena toimivan pygame.Surface olion johon lisätään valinnainen teksti.
    
        Parametrit
        ----------
        taustavari : str | tuple, valinnainen  
            Määrittää painikkeen värin. Voit käyttää str tai tuple arvoa. 

        taustavari_hiiri_paalla: str | tuple, valinnainen
            Määrittää painikkeen värin, jos hiiri on sen päällä. Voit käyttää str tai tuple arvoa.

        hiiri_paalla: bool, valinnainen
            Kertoo onko hiiri painikkeen päällä

        leveys_x: float | None, valinnainen
            Määrittää painikkeen leveyden, jos arvo on muu kuin None, Muuten käytössä on tekstin leveys + reunus

        fontti : str, valinnainen
            Käytettävän fontin nimi
        
        teksti : str, valinnainen
            Painikkeen teksti

        teksti_koko : int, valinnainen
            Painikkeen tekstin koko
        
        lihavoitu: bool, valinnainen
            Tekstin lihavointi
        
        kursivointi: bool, valinnainen
            Tekstin kursivointi

        teksti_vari: str | tuple, valinnainen
            Tekstin väri. Voit käyttää str tai tuple arvoa.
        
        reunus: float, valinnainen
            Tyhjän tilan määrä painikkeen reunan ja tekstin ympärillä.
            
        Palauttaa 
        ----------
        pygame.Surface
            Palauttaa pygame.Surface olion
        """

        # Painikkeen tekstit
        painike_fontti = pygame.font.SysFont(fontti, teksti_koko, bold=lihavoitu, italic=kursivoitu)
        painike_teksti = painike_fontti.render(teksti, True, teksti_vari)

        # Painikkeen koonti
        if leveys_x != None:
            leveys_x = leveys_x
        else:
            leveys_x = painike_teksti.get_width() + reunus
        painike = pygame.Surface((leveys_x, painike_teksti.get_height() + reunus), pygame.SRCALPHA)

        if hiiri_paalla:
            if taustavari_hiiri_paalla != None:
                painike.fill(taustavari_hiiri_paalla)
        else:
            if taustavari != None:
                painike.fill(taustavari)
        painike.blit(painike_teksti,(painike.get_width() / 2 - painike_teksti.get_width() / 2, painike.get_height() / 2 - painike_teksti.get_height() / 2))
        return painike

    def __Luo_Teksti(self, fontti:str = "Georgia", teksti:str = "", teksti_koko:int = 32, lihavoitu:bool = False, kursivoitu:bool = False, teksti_vari:str|tuple = "white") -> pygame.Surface:
        """ Luo tekstinä toimivan pygame.Surface olion ja palauttaa sen
    
        Parametrit
        ----------
        fontti : str, valinninen
            Käytettävän fontin nimi
        
        teksti : str, valinnainen
            Painikkeen teksti

        teksti_koko : int, valinnainen
            Painikkeen tekstin koko
        
        lihavoitu: bool, valinnainen
            Tekstin lihavointi
        
        kursivointi: bool, valinnainen
            Tekstin kursivointi

        teksti_vari: str | tuple, valinnainen
            Tekstin väri Voit käyttää str tai tuple arvoa.

        Palauttaa 
        ----------
        pygame.Surface
            Palauttaa pygame.Surface olion
        """
        fontti_valmis = pygame.font.SysFont(fontti, teksti_koko, bold=lihavoitu, italic=kursivoitu)
        teksti_valmis = fontti_valmis.render(teksti, True, teksti_vari)
        return teksti_valmis

if __name__ == "__main__":
    pygame.init()
    pygame.midi.init()
    soitin = pygame.midi.Output(0)
    kuule_savel = Kuule_Savel(soitin)
    kuule_savel.Aloita()