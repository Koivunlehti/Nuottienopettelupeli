"""
Tämä moduuli vastaa grafiikan piirrosta näytölle.
"""

import pygame

def Piirra_Viivasto(naytto:pygame.Surface, x:int, keski_c_y:int, rivivali:int, diskantti:bool):
    """Piirtää viivaston näytölle

        Piirtää joko diskantti- tai bassoviivaston alkaen keski C:n koordinaateista

        Parametrit
        ----------
        naytto : pygame.Surface
            Näyttönä toimiva pygame.Surface objekti 

        x : int
            Alkukoordinaatti näytön x-akselilla. Tästä kohtaa viivastoa aletaan piirtämään oikealle päin
        
        keski_c_y : int
            Keski C:n koordinaatti näytön y-akselilla. Diskanttiviivasto piirretään tämän yläpuolelle ja bassoviivasto alapuolelle.

        rivivali : int
            Montako pikseliä viivojen väliin jätetään.
        
        diskantti : bool
            Piirretäänkö diskantti- vai bassoviivasto. True = diskantti, False = basso

            
        Palauttaa
        ---------
        list
            Viivaston viivojen y-koordinaatit kerätään tähän listaan
        """
    
    y = keski_c_y
    paikat = []

    if diskantti:   # Lasketaanko ylös vai alaspäin y-akselilla
        rivivali *= -1
    
    y += rivivali # Muutetaan y-arvoa yhden rivin verran koska keski_c on ensimmäinen "ei näkyvä" viiva

    for i in range(5):
        pygame.draw.line(naytto, (200,200,200), ( x, y + i * rivivali ), ( naytto.get_width(), y + i * rivivali ))
        paikat.append(y + i * rivivali)

    return paikat

def Piirra_F_Avain(naytto:pygame.Surface, x:int, y:int, mittakaava:float = 1):
    """Piirtää F-avaimen näytölle

        Parametrit
        ----------
        naytto : pygame.Surface
            Näyttönä toimiva pygame.Surface objekti 

        x : int
            Alkukoordinaatti näytön x-akselilla.
        
        y : int
            Alkukoordinaatti näytön y-akselilla

        mittakaava : float, valinnainen
            Määrittää kuinka suurena tai pienenä F-avain piirretään. (oletusarvo on 1)
        """
    
    m = mittakaava
    pygame.draw.lines(naytto,(200,200,200), False, [
        ( x - 10 * m, y ),
        ( x, y - 10 * m ),
        ( x + 10 * m, y ),
        ( x, y + 10 * m ),
        ( x - 10 * m, y ),
        ( x - 10 * m, y - 20 * m ),
        ( x + 5 * m, y - 30 * m ),
        ( x + 20 * m, y - 35 * m ),
        ( x + 40 * m, y - 20 * m),
        ( x + 45 * m, y ),
        ( x + 40 * m, y + 20 * m ),
        ( x + 25 * m, y + 40 * m),
        ( x - 15 * m, y + 70 * m)], 4)
    pygame.draw.circle(naytto, (200,200,200), [ x * m, y * m ], 10) # F-avaimen päätypallo
    pygame.draw.circle(naytto, (200,200,200), [ x + 65 * m, y - 10 * m ], 5) # Ylimmäinen pallo
    pygame.draw.circle(naytto, (200,200,200), [ x + 65 * m, y + 10 * m ], 5) # Alimmainen pallo

def Piirra_G_Avain(naytto:pygame.Surface, x:int, y:int, mittakaava:float = 1):
    """Piirtää G-avaimen näytölle

        Parametrit
        ----------
        naytto : pygame.Surface
            Näyttönä toimiva pygame.Surface objekti 

        x : int
            Alkukoordinaatti näytön x-akselilla.
        
        y : int
            Alkukoordinaatti näytön y-akselilla

        mittakaava : float, valinnainen
            Määrittää kuinka suurena tai pienenä G-avain piirretään. (oletusarvo on 1)
        """
    
    m = mittakaava
    pygame.draw.lines(naytto, (200,200,200), False, [
        ( x, y + 60 * m ), 
        ( x + 15 * m, y + 50 * m ), 
        ( x + 5 * m, y + 40 * m ), 
        ( x - 5 * m, y + 50 * m ), 
        ( x, y + 60 * m ), 
        ( x + 20 * m, y + 60 * m ), 
        ( x + 30 * m, y + 40 * m ), 
        ( x + 5 * m, y - 70 * m ), 
        ( x + 20 * m, y - 95 * m ), 
        ( x + 30 * m, y - 75 * m ), 
        ( x + 20 * m, y - 60 * m ), 
        ( x - 15 * m, y - 15 * m ), 
        ( x - 10 * m, y + 15 * m ), 
        ( x + 10 * m, y + 25 * m ), 
        ( x + 35 * m, y + 20 * m ), 
        ( x + 40 * m, y ), 
        ( x + 30 * m, y - 15 * m ), 
        ( x + 10 * m, y - 10 * m ), 
        ( x + 5 * m, y + 5  * m ), 
        ( x + 15 * m, y + 15 * m ), 
        ( x + 25 * m, y + 5 * m )], 4)

    pygame.draw.circle(naytto, (200,200,200), [ x + 5 * m, y + 50 * m ], 10) # G-avaimen päätypallo

def Piirra_Ylennys(naytto:pygame.Surface, x:int, y:int, x_korjaus:int = 0, mittakaava:float = 1):
    """Piirtää ylennysmerkin näytölle

        Parametrit
        ----------
        naytto : pygame.Surface
            Näyttönä toimiva pygame.Surface objekti 

        x : int
            Alkukoordinaatti näytön x-akselilla.
        
        y : int
            Alkukoordinaatti näytön y-akselilla
        
        x_korjaus : int, valinnainen
            Muuttaa aloituspaikkaa x-akselilla (oletusarvo on 0)    

        mittakaava : float, valinnainen
            Määrittää kuinka suurena tai pienenä ylennysmerkki piirretään. (oletusarvo on 1)
        """

    m = mittakaava
    x += x_korjaus * m
    pygame.draw.line(naytto, (200,200,200), ( x - 5 * m, y - 13 * m ), ( x - 5 * m, y + 17 * m ), 3) # Vasen pystyviiva
    pygame.draw.line(naytto, (200,200,200), ( x + 5 * m, y - 15 * m ), ( x + 5 * m, y + 15 * m ), 3) # Oikea pystyviiva
    pygame.draw.line(naytto, (200,200,200), ( x - 15 * m, y - 5 * m ), ( x + 15 * m, y - 7 * m ), 4) # Ylin vaakaviiva
    pygame.draw.line(naytto, (200,200,200), ( x - 15 * m, y + 7 * m ), ( x + 15 * m, y + 5 * m ), 4) # Alin vaakaviiva

def Piirra_Alennus(naytto:pygame.Surface, x:int, y:int, x_korjaus:int = 0, mittakaava:float = 1):
    """Piirtää alennusmerkin näytölle

        Parametrit
        ----------
        naytto : pygame.Surface
            Näyttönä toimiva pygame.Surface objekti 

        x : int
            Alkukoordinaatti näytön x-akselilla.
        
        y : int
            Alkukoordinaatti näytön y-akselilla
        
        x_korjaus : int, valinnainen
            Muuttaa aloituspaikkaa x-akselilla (oletusarvo on 0)    

        mittakaava : float, valinnainen
            Määrittää kuinka suurena tai pienenä alennusmerkki piirretään. (oletusarvo on 1)
        """
    
    m = mittakaava
    x += x_korjaus * m
    pygame.draw.lines(naytto, (200,200,200), False, [
        ( x - 10 * m, y ), 
        ( x, y - 10 * m ),
        ( x + 10 * m, y - 10 * m ),
        ( x, y + 10 * m ),
        ( x - 10 * m, y + 10 * m ),
        ( x - 10 * m, y - 40 * m )], 3)

def palautus(naytto:pygame.Surface, x:int, y:int, x_korjaus:int = 0 ,mittakaava:float = 1):
    """ Piirtää palautusmerkin näytölle.

        Palautusmerkki kumoaa nuotin ylennyksen tai alennuksen aiheuttaman muutoksen.

        Parametrit
        ----------
        naytto : pygame.Surface
            Näyttönä toimiva pygame.Surface objekti 

        x : int
            Alkukoordinaatti näytön x-akselilla.
        
        y : int
            Alkukoordinaatti näytön y-akselilla
        
        x_korjaus : int, valinnainen
            Muuttaa aloituspaikkaa x-akselilla (oletusarvo on 0)    

        mittakaava : float, valinnainen
            Määrittää kuinka suurena tai pienenä palautusmerkki piirretään. (oletusarvo on 1)
    """
    m = mittakaava
    x += x_korjaus * m

    pygame.draw.line(naytto, (200,200,200), (x - 5 * m, y + 10 * m), (x - 5 * m, y - 30 * m), 2) # vasen pystyviiva
    pygame.draw.line(naytto, (200,200,200), (x + 5 * m, y - 10 * m), (x + 5 * m, y + 30 * m), 2) # oikea pystyviiva
    pygame.draw.line(naytto, (200,200,200), (x - 10 * m, y - 5 * m), (x + 10 * m, y - 9 * m), 4) # ylin vaakaviiva
    pygame.draw.line(naytto, (200,200,200), (x - 10 * m, y + 9 * m), (x + 10 * m, y + 5 * m), 4) # alin vaakaviiva

def Piirra_4_Osa_Nuotti(naytto:pygame.Surface, x:int, y:int, mittakaava:float = 1):
    """Piirtää neljäsosanuotin näytölle

        Parametrit
        ----------
        naytto : pygame.Surface
            Näyttönä toimiva pygame.Surface objekti 

        x : int
            Alkukoordinaatti näytön x-akselilla.
        
        y : int
            Alkukoordinaatti näytön y-akselilla

        mittakaava : float, valinnainen
            Määrittää kuinka suurena tai pienenä nuotti piirretään. (oletusarvo on 1)
        """
    m = mittakaava
    pygame.draw.line(naytto, (200,200,200), ( x + 27 * m, y ), ( x + 27 * m, y + -50 * m ), 4) # Varsiosa
    pygame.draw.ellipse(naytto, (200,200,200), [ x, y - 10 * m, 30 * m, 20 * m ]) # Pääosa

def Piirra_Apuviivat(naytto:pygame.Surface, x:int , y:int, pituus:int, rivivali:int, maara:int, alaspain:bool):
    """Piirtää apuviivat näytölle

        Apuviivoja käytetään kun nuotti on varsinaisen viivaston viivojen ylä tai alapuolella
    
        Parametrit
        ----------
        naytto : pygame.Surface
            Näyttönä toimiva pygame.Surface objekti 

        x : int
            Alkukoordinaatti näytön x-akselilla.
        
        y : int
            Alkukoordinaatti näytön y-akselilla

        pituus : int
            Määrittää kuinka pitkä viiva piirretään
        
        rivivali: int
            Määrittää apuviivojen rivivälin. Kannattaa käyttää samaa arvoa kuin viivaston rivivälinä on.
        
        maara : int
            Montako apuviivaa piirretään päällekkäin. Jos nuotti on kaukana viivaston ulkopuolella, tarvitaan useampi viiva.
        
        alaspain : bool
            Piirretäänkö apuviivoja alaspäin annetuista x ja y koordinaateista. 
            
        """
    for i in range(maara):
        if alaspain:
            y += i + 1 * rivivali
        else:
            y -= i + 1 * rivivali
        pygame.draw.line(naytto, (200,200,200), ( x, y ), ( x + pituus, y ))

def Piirra_Savellaji(naytto:pygame.Surface, x:int, savellaji:str, paikat:dict, diskantti:bool = True, mittakaava:float = 1):
    """Piirtää sävellajin näytölle

        Sävellaji koostuu maksimissaan 7:stä ylennys- tai alennusmerkistä, jotka piirretään muodostelmaan tietyssä järjestyksessä.
    
        Parametrit
        ----------
        naytto : pygame.Surface
            Näyttönä toimiva pygame.Surface objekti 

        x : int
            Alkukoordinaatti näytön x-akselilla.
        
        savellaji : str
            Halutun sävellajin kirjain

        paikat : dict
            Sanakirja-tyyppinen taulukko nuottien paikoista viivastolla. 
            Sanakirjan avaimena toimii Midi-arvo (0-127), arvona list[koordinaatti y-akselilla, koskettimen väri]
        
        diskantti: bool, valinnainen
            Määrittää onko kyseessä diskantti vai basso viivasto. (oletusarvo on True)
        
        mittakaava : float, valinnainen
            Määrittää kuinka suurena tai pienenä sävellajin merkit piirretään. (oletusarvo on 1)

        Palauttaa 
        ----------

        int
            Sävellajin piirtoon tarvittu tila x-akselilla
        """
    #                       F#  C#  G#  D#  A#  E#  H#                        
    ylennykset_diskantti = [77, 72, 79, 74, 69, 76, 71]
    ylennykset_basso =     [53, 48, 55, 50, 45, 52, 47]

    #                       B   Eb  Ab  Db  Gb  Cb  Fb
    alennukset_diskantti = [71, 76, 69, 74, 67, 72, 65]
    alennukset_basso =     [47, 52, 45, 50, 43, 48, 41]

    duurit = {"Cb":-7, "Gb":-6, "Db":-5, "Ab":-4, "Eb":-3, "B":-2 , "F":-1 , "C":0, "G":1, "D":2, "A":3 , "E":4 , "H":5 , "F#":6, "C#":7}
    mollit = {"ab":-7, "eb":-6, "b":-5, "f":-4, "c":-3, "g":-2 , "d":-1 , "a":0, "e":1, "h":2, "f#":3 , "c#":4 , "g#":5 , "d#":6, "a#":7}
    
    taso = 0
    if savellaji in duurit:
        taso = duurit[savellaji]
    elif savellaji in mollit:
        taso = mollit[savellaji]
    
    tila_x = x

    if taso > 0:
        for i in range(0,taso):
            if diskantti:
                Piirra_Ylennys(naytto, x, paikat[ylennykset_diskantti[i]][0], 0, mittakaava)
            else:
                Piirra_Ylennys(naytto, x, paikat[ylennykset_basso[i]][0], 0, mittakaava)
            x += 20 * mittakaava
    elif taso < 0:
        taso = taso * -1
        for i in range(0,taso):
            if diskantti:
                Piirra_Alennus(naytto, x, paikat[alennukset_diskantti[i]][0], 0, mittakaava)
            else:
                Piirra_Alennus(naytto, x, paikat[alennukset_basso[i]][0], 0, mittakaava)
            x += 20 * mittakaava

    return x - tila_x