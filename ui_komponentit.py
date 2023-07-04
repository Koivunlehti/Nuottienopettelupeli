import pygame

def Luo_ylavalikko_pelkistetty(leveys:float, korkeus:float = 0, reunus:tuple = (0, 0), taustavari:str | tuple = "black", 
                                teksti_vasen:str = "", teksti_keski:str = "", teksti_oikea:str = "", teksti_koko:int = 32, teksti_fontti:str = "Georgia", teksti_vari:str | tuple = "white"):
        """ Luo yksinkertaisen, maksimissaan kolmella tekstialueella varustetun, yläreunan valikon.
            
            Tekstit noudattavat kaikki samaa kokoa, fonttia ja väritystä.

        Parametrit
        ----------
        leveys : float  
            Valikon leveys

        korkeus: float, valinnainen
            Valikon korkeus. Jos annettu arvo on pienempi kuin tekstin korkeus, käytetään arvona tekstin korkeutta.

        reunus: tuple, valinnainen
            Paljonko tyhjää tilaa valikon reunojen ja tekstien väliin jätetään. (vasen / oikea, ylä / ala)

        taustavari: str| tuple, valinnainen
            Valikon taustaväri. Voit käyttää str tai tuple arvoa.

        teksti_vasen : str, valinnainen
            Vasemman reunan teksti
        
        teksti_keski : str, valinnainen
            Keskimmäinen teksti

        teksti_oikea : str, valinnainen
            Oikean reunan teksti
        
        teksti_koko: int, valinnainen
            Tekstien fonttikoko
        
        teksti_fontti: str, valinnainen
            Tekstien fontti

        teksti_vari: str | tuple, valinnainen
            Tekstin väri. Voit käyttää str tai tuple arvoa.

        Palauttaa 
        ----------
        pygame.Surface
            Palauttaa pygame.Surface olion


        """
        teksti_v = Luo_Teksti(teksti=teksti_vasen, koko=teksti_koko, fontti = teksti_fontti, vari=teksti_vari)
        teksti_k = Luo_Teksti(teksti=teksti_keski, koko=teksti_koko, fontti = teksti_fontti, vari=teksti_vari)
        teksti_o = Luo_Teksti(teksti=teksti_oikea, koko=teksti_koko, fontti = teksti_fontti, vari=teksti_vari)
        if korkeus < teksti_v.get_height():
            korkeus = teksti_v.get_height() + reunus[1] * 2
        valikko = pygame.Surface((leveys, korkeus), pygame.SRCALPHA)
        valikko.fill(taustavari)
        valikko.blit(teksti_v, (0 + reunus[0], 0 + reunus[1]))
        valikko.blit(teksti_k, (valikko.get_width() / 2 - teksti_k.get_width() / 2, 0 + reunus[1]))
        valikko.blit(teksti_o, (valikko.get_width() - teksti_o.get_width() - reunus[0], 0 + reunus[1]))
        return valikko

def Luo_Painike(taustavari:str|tuple = None, taustavari_hiiri_paalla:str|tuple = None, hiiri_paalla:bool = False, leveys_x:float|None = None,
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

def Luo_Teksti(fontti:str = "Georgia", teksti:str = "", koko:int = 32, lihavoitu:bool = False, kursivoitu:bool = False, vari:str|tuple = "white") -> pygame.Surface:
        """ Luo tekstinä toimivan pygame.Surface olion ja palauttaa sen
    
        Parametrit
        ----------
        fontti : str, valinninen
            Käytettävän fontin nimi
        
        teksti : str, valinnainen
            Tekstinä käytettävä merkkijono

        koko : int, valinnainen
            Tekstin koko
        
        lihavoitu: bool, valinnainen
            Tekstin lihavointi
        
        kursivointi: bool, valinnainen
            Tekstin kursivointi

        vari: str | tuple, valinnainen
            Tekstin väri. Voit käyttää str tai tuple arvoa.

        Palauttaa 
        ----------
        pygame.Surface
            Palauttaa pygame.Surface olion
        """
        fontti_valmis = pygame.font.SysFont(fontti, koko, bold=lihavoitu, italic=kursivoitu)
        teksti_valmis = fontti_valmis.render(teksti, True, vari)
        return teksti_valmis