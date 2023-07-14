"""
Tämä moduuli vastaa nuottikirjoituksen merkkien luomisesta.
"""

import pygame

def Kuvion_Mitat(koordinaatit:list):
    """Laskee annetusta koordinaattitaulkosta kuvion leveyden ja korkeuden

    Parametrit
    ----------
    koordinaatit : list
        Lista koordinaateista. Listan alkioiden pitää olla x ja y koordinaattipareja joko lista tai tuple muodossa. 
        Esim: [ ( x, y ), ... ] tai [ [ x, y ], ... ]

    Palauttaa
    ---------
        tuple
            Palauttaa kokonaisleveyden ja kokonaiskorkeuden. ( leveys, korkeus )
    """
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    for i in range(len(koordinaatit)):
        if min_x > koordinaatit[i][0]:
            min_x = koordinaatit[i][0]
        if max_x < koordinaatit[i][0]:
            max_x = koordinaatit[i][0]
        if min_y > koordinaatit[i][1]:
            min_y = koordinaatit[i][1]
        if max_y < koordinaatit[i][1]:
            max_y = koordinaatit[i][1]
    return (max_x - min_x, max_y - min_y)
        


def Luo_Viivasto(leveys:float, rivivali:float, paksuus:int = 1, vari:str|tuple = (200, 200, 200), mittakaava:float = 1):
    """Luo viivaston.

        Parametrit
        ----------
        leveys : float
            Viivaston leveys.

        rivivali : float
            Viivojen väliin jäävä tila.

        paksuus : int, valinnainen
            Viivojen paksuus.
            
        vari : str | tuple, valinnainen
            Viivaston piirtoon käytettävä väri.

        mittakaava : float, valinnainen
            Muuttaa viivaston mittasuhteita, myös leveyttä.
            
        Palauttaa
        ---------
        pygame.Surface
            Palauttaa pygame.Surface olion.
        """
    leveys = leveys * mittakaava
    rivivali = rivivali * mittakaava
    paksuus = int(paksuus * mittakaava)

    viivasto = pygame.Surface((leveys, 5 * rivivali), pygame.SRCALPHA)

    for i in range(5):
        pygame.draw.line(viivasto, vari, (0, 0 + i * rivivali), (leveys, 0 + i * rivivali), paksuus)

    return viivasto

def Luo_Tahtiviiva(korkeus:float, paksuus:int = 2, vari:str|tuple = (200,200,200), mittakaava:float = 1):
    """Luo viivaston tahtiviivan.

        Tahtiviivalla merkataan missä kohtaa tahti vaihtuu seuraavaan.
    
        Parametrit
        ----------
        korkeus : float
            Tahtiviivan pituus.
        
        paksuus : float
            Tahtiviivan paksuus.

        vari : str | tuple, valinnainen
            Tahtiviivan piirtoon käytettävä väri.

        mittakaava : float, valinnainen
            Muuttaa tahtiviivan mittasuhteita mutta ei korkeutta.    
        
        Palauttaa
        ---------
        pygame.Surface
            Palauttaa pygame.Surface olion.
        """
    paksuus = int(paksuus * mittakaava)
    tahtiviiva = pygame.Surface((paksuus, korkeus), pygame.SRCALPHA)
    pygame.draw.line(tahtiviiva, vari, (0, 0), ( 0, korkeus), paksuus)
    return tahtiviiva

def Luo_Paatosviiva(korkeus:float, paksuus_ohut_viiva:int = 2, paksuus_paksu_viiva:int = 4, vari:str|tuple = (200,200,200), mittakaava:float = 1):
    """Luo viivaston päätösviivan.

        Tämä on koko viivaston päättävä päätyviiva.
    
        Parametrit
        ----------
        korkeus : float
            Määrittää viivan korkeuden y-akselilla.

        paksuus_ohut_viiva : int, valinnainen
            Määrittää ohuen viivan paksuuden.
        
        paksuus_paksu_viiva : int, valinnainen
            Määrittää paksun pystyviivan paksuuden.

        vari : str | tuple, valinnainen
            Päätösviivan piirtoon käytettävä väri.

        mittakaava : float, valinnainen
            Muuttaa paatosviivan mittasuhteita, mutta ei korkeutta.
                
        Palauttaa
        ---------
        pygame.Surface
            Palauttaa pygame.Surface olion.
            
        """
    ohut_viiva = Luo_Tahtiviiva(korkeus, int(paksuus_ohut_viiva * mittakaava), vari)
    paksu_viiva = Luo_Tahtiviiva(korkeus, int(paksuus_paksu_viiva * mittakaava), vari)

    paatosviiva = pygame.Surface((ohut_viiva.get_width() + paksu_viiva.get_width() + 6, korkeus), pygame.SRCALPHA)
    paatosviiva.blit(ohut_viiva, (0,0))
    paatosviiva.blit(paksu_viiva, (ohut_viiva.get_width() + 6, 0))

    return paatosviiva
    
def Luo_Akkoladi(korkeus:float, paksuus_kaariviiva:int = 4, paksuus_pystyviiva:int = 2, vari:str|tuple = (200,200,200), mittakaava:float = 1):
    """Luo viivaston Akkoladin.

        Akkoladi on pianoviivastolla käytettävä diskantti- ja bassorivin yhdistäjä.
        Se piirretään heti viivaston alkuun.
    
        Parametrit
        ----------
        korkeus : float
            Määrittää viivan korkeuden y-akselilla.

        paksuus_kaariviiva : int, valinnainen
            Määrittää kaarevan viivan paksuuden.
        
        paksuus_pystyviiva : int, valinnainen
            Määrittää suoran pystyviivan paksuuden.

        vari : str | tuple, valinnainen
            Akkoladin piirtoon käytettävä väri.

        mittakaava : float, valinnainen
            Muuttaa akkoladin mittasuhteita, mutta ei korkeutta.
                
        Palauttaa
        ---------
        pygame.Surface
            Palauttaa pygame.Surface olion.
        """
    m = mittakaava
    x = 0
    y = korkeus / 2
    y_osa = korkeus / 20
    paksuus_kaariviiva = int(paksuus_kaariviiva * m)
    paksuus_pystyviiva = int(paksuus_pystyviiva * m)
    tila_valissa = 4 * m
    muoto = [
        (x + 16 * m, y - korkeus / 2), 
        (x + 8 * m, y - y_osa * 9), 
        (x + 5 * m, y - y_osa * 8), 
        (x + 10 * m, y - y_osa * 2), 
        (x + 8 * m, y - y_osa * 1), 
        (x, y),  # keskikohta
        (x + 8 * m, y + y_osa * 1), 
        (x + 10 * m, y + y_osa * 2), 
        (x + 5 * m, y + y_osa * 8), 
        (x + 8 * m, y + y_osa * 9), 
        (x + 16 * m, y + korkeus / 2)]
    
    mitat = Kuvion_Mitat(muoto)
    tahtiviiva = Luo_Tahtiviiva(korkeus, paksuus_pystyviiva, vari)
    akkoladi = pygame.Surface((mitat[0] + tila_valissa + tahtiviiva.get_width(), korkeus), pygame.SRCALPHA)

    pygame.draw.lines(akkoladi, vari, False, muoto, paksuus_kaariviiva)
    akkoladi.blit(tahtiviiva,(20,0))

    return akkoladi

def Luo_F_Avain(vari:str|tuple = (200,200,200), mittakaava:float = 1):
    """Luo F-avaimen.

        Parametrit
        ----------
        vari : str | tuple, valinnainen
            F-avaimen piirtoon käytettävä väri.

        mittakaava : float, valinnainen
            Muuttaa F-avaimen mittasuhteita.

        Palauttaa
        ---------
        pygame.Surface
            Palauttaa pygame.Surface olion.

        float
            Keskitykseen tarvittava y_koordinaatin korjaus.
        """
    
    m = mittakaava 
    x = 0
    y = 0
    viivan_paksuus = int(4 * m)
    muoto = [
        ( x, y + 20 * m), # yläpään pallo
        ( x + 3 * m, y + 6 * m ),
        ( x + 5 * m, y + 4 * m ),
        ( x + 10 * m, y + 2 * m ),
        ( x + 20 * m, y * m ), # kaaren huippu
        ( x + 25 * m, y + 3 * m ),
        ( x + 30 * m, y + 10 * m ),
        ( x + 30 * m, y + 20 * m),  # nuotillinen keskusta
        ( x + 25 * m, y + 30 * m),
        ( x + 20 * m, y + 40 * m ),
        ( x + 10 * m, y + 50 * m),
        ( x, y + 60 * m)]   # alapää
    
    lihavointi = [
        ( x + 20 * m, y * m ), # kaaren huippu
        ( x + 27 * m, y + 2 * m ),
        ( x + 34 * m, y + 11 * m ),
        ( x + 34 * m, y + 20 * m),
        ( x + 27 * m, y + 32 * m),
        ( x + 22 * m, y + 41 * m ),
        ( x + 10 * m, y + 50 * m),]
    
    mitat = Kuvion_Mitat(muoto)
    f_keskusta = y + 20 * m
    f_avain = pygame.Surface((mitat[0] * 2 + viivan_paksuus / 2, mitat[1] + viivan_paksuus / 2), pygame.SRCALPHA)

    pygame.draw.lines(f_avain, vari, False, muoto, viivan_paksuus)
    pygame.draw.lines(f_avain, vari, False, lihavointi, viivan_paksuus)
    pygame.draw.circle(f_avain, vari, [ x + 9 * m, y + 20 * m ], 9 * m ) # F-avaimen päätypallo
    pygame.draw.circle(f_avain, vari, [ f_avain.get_width() - 5 * m, y + 10 * m ], 5 * m ) # Ylimmäinen pallo
    pygame.draw.circle(f_avain, vari, [ f_avain.get_width() - 5 * m, y + 30 * m ], 5 * m ) # Alimmainen pallo

    return f_avain, f_keskusta

def Luo_G_Avain(vari:str|tuple = (200,200,200), mittakaava:float = 1):
    """Luo G-avaimen.

        Parametrit
        ----------
        vari : str | tuple, valinnainen
            G-avaimen piirtoon käytettävä väri.
            
        mittakaava : float, valinnainen
            Muuttaa G-avaimen mittasuhteita.

        Palauttaa
        ---------
        pygame.Surface
            Palauttaa pygame.Surface olion.
        
        float
           Keskitykseen tarvittava y_koordinaatin korjaus.
        """
    
    m = mittakaava
    x = 0
    y = 0
    viivan_paksuus = int(4 * m)
    muoto = [
        ( x + 10 * m, y + 125 * m ), 
        ( x + 15 * m, y + 135 * m ), 
        ( x + 35 * m, y + 135 * m ), 
        ( x + 45 * m, y + 115 * m ), 
        ( x + 20 * m, y + 15 * m ), 
        ( x + 35 * m, y ),  # ylälenkki
        ( x + 45 * m, y + 15 * m ), 
        ( x + 35 * m, y + 25 * m ), 
        ( x, y + 60 * m ), 
        ( x + 5 * m, y + 90 * m ), 
        ( x + 25 * m, y + 100 * m ), 
        ( x + 50 * m, y + 95 * m ), 
        ( x + 55 * m, y + 75 * m ), 
        ( x + 45 * m, y + 60 * m ), 
        ( x + 25 * m, y + 65 * m ), 
        ( x + 20 * m, y + 80  * m ), 
        ( x + 30 * m, y + 90 * m ), 
        ( x + 40 * m, y + 80 * m ) # kierukan keskusta, nuotillinen keskusta
        ]
    g_keskus = y + 80 * m
    mitat = Kuvion_Mitat(muoto)
    g_avain = pygame.Surface((mitat[0] + viivan_paksuus / 2, mitat[1] + viivan_paksuus / 2), pygame.SRCALPHA)
    
    pygame.draw.lines(g_avain, vari, False, muoto , viivan_paksuus)
    pygame.draw.circle(g_avain, vari, [ x + 20 * m, y + 125 * m ], 10 * m) # G-avaimen päätypallo
    
    return g_avain, g_keskus

def Luo_Ylennys(vari:str|tuple = (200,200,200), mittakaava:float = 1):
    """Luo ylennysmerkin.

        Parametrit
        ----------
        vari : str | tuple, valinnainen
           Ylennysmerkin piirtoon käytettävä väri.
            
        mittakaava : float, valinnainen
            Muuttaa ylennysmerkin mittasuhteita.

        Palauttaa
        ---------
        pygame.Surface
            Palauttaa pygame.Surface olion.
        
        float
            Keskitykseen tarvittava y_koordinaatin korjaus.
        """

    m = mittakaava
    x = 0
    y = 0
    paksuus_vaakaviiva = int(5 * m)
    paksuus_pystyviiva = int(3 * m)
    ylennys_keskus = 30 * m
    
    ylennys = pygame.Surface((25 * m + paksuus_pystyviiva, 60 * m + paksuus_vaakaviiva), pygame.SRCALPHA)
    pygame.draw.line(ylennys, vari, ( x + 7.5 * m, y + 5 * m ), ( x + 7.5 * m, y + 60 * m ), paksuus_pystyviiva) # Vasen pystyviiva
    pygame.draw.line(ylennys, vari, ( x + 17.5 * m, y ), ( x + 17.5 * m, y + 55 * m ), paksuus_pystyviiva) # Oikea pystyviiva
    pygame.draw.line(ylennys, vari, ( x, y + 22 * m), ( x + 25 * m, y + 18 * m), paksuus_vaakaviiva) # Ylin vaakaviiva
    pygame.draw.line(ylennys, vari, ( x, y + 42 * m ), ( x + 25 * m, y + 38 * m ), paksuus_vaakaviiva) # Alin vaakaviiva

    return ylennys, ylennys_keskus

def Luo_Alennus(vari:str|tuple = (200,200,200), mittakaava:float = 1):
    """Luo alennusmerkin.

        Parametrit
        ----------
        vari : str | tuple, valinnainen
           Alennusmerkin piirtoon käytettävä väri.
            
        mittakaava : float, valinnainen
            Muuttaa alennusmerkin mittasuhteita.

        Palauttaa
        ---------
        pygame.Surface
            Palauttaa pygame.Surface olion.
        
        float
            Keskitykseen tarvittava y_koordinaatin korjaus.
        """
    
    m = mittakaava
    x = 0
    y = 0
    viivan_paksuus = int(3 * m)
    alennus_keskus = 40 * m
    muoto = [
        ( x + viivan_paksuus / 2 * m, y + 40 * m), 
        ( x + 10 * m, y + 30 * m ),
        ( x + 20 * m, y + 30 * m ),
        ( x + 10 * m, y + 50 * m ),
        ( x + viivan_paksuus / 2 * m, y + 50 * m ),
        ( x + viivan_paksuus / 2 * m, y ) # varren yläpää
        ]
    mitat = Kuvion_Mitat(muoto)
    alennus = pygame.Surface((mitat[0] + viivan_paksuus, mitat[1] + viivan_paksuus), pygame.SRCALPHA)

    pygame.draw.lines(alennus, vari, False, muoto, 3)
    
    return alennus, alennus_keskus

def Luo_Palautus(vari:str|tuple = (200,200,200), mittakaava:float = 1):
    """Luo palautusmerkin.

        Parametrit
        ----------
        vari : str | tuple, valinnainen
           Palautusmerkin piirtoon käytettävä väri.
            
        mittakaava : float, valinnainen
            Muuttaa palautusmerkin mittasuhteita.

        Palauttaa
        ---------
        pygame.Surface
            Palauttaa pygame.Surface olion.
        
        float
            Keskitykseen tarvittava y_koordinaatin korjaus.
        """
    
    m = mittakaava
    x = 0
    y = 0
    paksuus_vaakaviiva = int(4 * m)
    paksuus_pystyviiva = int(2 * m)
    palautus_keskus = 30 * m
    palautus = pygame.Surface((25 * m + paksuus_pystyviiva, 60 * m), pygame.SRCALPHA)

    pygame.draw.line(palautus, vari, (x, y), (x, y + 40 * m), paksuus_pystyviiva) # vasen pystyviiva
    pygame.draw.line(palautus, vari, (x + 25 * m, y + 20 * m), (x + 25 * m, y + 60 * m), paksuus_pystyviiva) # oikea pystyviiva
    pygame.draw.line(palautus, vari, (x, y + 22 * m), (x + 25 * m, y + 18 * m), paksuus_vaakaviiva) # ylin vaakaviiva
    pygame.draw.line(palautus, vari, (x, y + 42 * m), (x + 25 * m, y + 38 * m), paksuus_vaakaviiva) # alin vaakaviiva

    return palautus, palautus_keskus

def Luo_4_Osa_Nuotti(kaannetty:bool = False, vari:str|tuple = (200,200,200), mittakaava:float = 1):
    """Luo palautusmerkin.

        Parametrit
        ----------
        kaannetty : bool, valinnainen
            Kääntää nuotin varren alaspäin.

        vari : str | tuple, valinnainen
           Nuotin piirtoon käytettävä väri.
            
        mittakaava : float, valinnainen
            Muuttaa nuotin mittasuhteita.

        Palauttaa
        ---------
        pygame.Surface
            Palauttaa pygame.Surface olion.
        
        float
            Keskitykseen tarvittava y_koordinaatin korjaus.
        """
    
    m = mittakaava
    x = 0
    y = 0
    paksuus_pystyviiva = int(4 * m)
    nuotti = pygame.Surface((30 * m + paksuus_pystyviiva, 80 * m), pygame.SRCALPHA)
    
    if kaannetty:
        nuotti_keskus = 10 * m
        pygame.draw.line(nuotti, vari, ( x, y + 10 * m), ( x, y + 80 * m ), paksuus_pystyviiva) # Varsiosa
        pygame.draw.ellipse(nuotti, vari, [ x, y, 30 * m + paksuus_pystyviiva, 20 * m ]) # Pääosa
    else:
        nuotti_keskus = 70 * m
        pygame.draw.line(nuotti, vari, ( x + 30 * m, y ), ( x + 30 * m, y + 70 * m ), paksuus_pystyviiva) # Varsiosa
        pygame.draw.ellipse(nuotti, vari, [ x, y + 60 * m, 30 * m + paksuus_pystyviiva, 20 * m ]) # Pääosa

    return nuotti, nuotti_keskus

def Luo_Apuviivat(leveys:int, rivivali:int, maara:int = 1, ylospain:bool = False, paksuus:int = 1, vari:str|tuple = (200,200,200), mittakaava:float = 1):
    """Luo apuviivat.

        Apuviivoja käytetään kun nuotti on varsinaisen viivaston viivojen ylä tai alapuolella.
    
        Parametrit
        ----------
        pituus : int
            Apuviivan leveys.

        rivivali : int
            Viivojen väliin jäävä tila.
        
        maara : int, valinnainen
            Kuinka monta apuviivaa tarvitaan. 

        ylospain : bool, valinnainen
            Luodaanko viivoja viivastolta ylöspäin vai alaspäin.
        
        paksuus : int, valinnainen
            Viivojen paksuus.
        
        vari : str | tuple, valinnainen
           Viivan piirtoon käytettävä väri.
        
        mittakaava : float, valinnainen
            Muuttaa viivan mittasuhteita, myös leveyttä.
        
        Palauttaa
        ---------
        pygame.Surface
            Palauttaa pygame.Surface olion.
        """
    
    m = mittakaava 
    x = 0
    paksuus = int(paksuus * m)
    viivat = pygame.Surface((leveys * m, (rivivali + paksuus) * maara ), pygame.SRCALPHA)

    for i in range(maara):
        if ylospain:
            pygame.draw.line(viivat, vari, ( x, (i + 1) * rivivali - rivivali ), ( x + leveys, (i + 1) * rivivali - rivivali ), paksuus)
        else:
            pygame.draw.line(viivat, vari, ( x, (i + 1) * rivivali ), ( x + leveys, (i + 1) * rivivali ), paksuus)

    return viivat

def Luo_Savellaji(savellaji:str, rivivali:float, vari:str|tuple = (200,200,200), mittakaava:float = 1):
    """Luo sävellajin 

        Sävellaji koostuu maksimissaan 7:stä ylennys- tai alennusmerkistä, 
        jotka piirretään muodostelmaan tietyille sävelille tietyssä järjestyksessä.
    
        Parametrit
        ----------
        
        savellaji : str
            Halutun sävellajin tunniste.
        
        rivivali : float
            Viivaston riviväli.
        
        vari : str | tuple, valinnainen
           Sävellajin piirtoon käytettävä väri.
        
        mittakaava : float, valinnainen
            Muuttaa sävellajin mittasuhteita.

        Palauttaa
        ---------
        pygame.Surface
            Palauttaa pygame.Surface olion.
        
        float
            Keskitykseen tarvittava y_koordinaatin korjaus.
        """
    
    # Sävellajit
    duurit = {"Cb":-7, "Gb":-6, "Db":-5, "Ab":-4, "Eb":-3, "B":-2 , "F":-1 , "C":0, "G":1, "D":2, "A":3 , "E":4 , "H":5 , "F#":6, "C#":7}
    mollit = {"ab":-7, "eb":-6, "b":-5, "f":-4, "c":-3, "g":-2 , "d":-1 , "a":0, "e":1, "h":2, "f#":3 , "c#":4 , "g#":5 , "d#":6, "a#":7}
    
    taso = 0
    x = 0
    m = mittakaava

    # Montako merkkiä sävellajiin luodaan
    if savellaji in duurit:
        taso = duurit[savellaji]
    elif savellaji in mollit:
        taso = mollit[savellaji]

    if taso > 0: # Ylennykset 
        ylennykset = []
        ylennykset_paikat_y = [10 * m, 40 * m, 0 * m, 30 * m, 60 * m, 20 * m, 50 * m]

        for i in range(0, taso): # Luodaan tarvittava määrä merkkejä
            ylennykset.append(Luo_Ylennys(vari, mittakaava))

        luotu_savellaji = pygame.Surface((ylennykset[0][0].get_width() * len(ylennykset), 7 * rivivali * m), pygame.SRCALPHA)

        for i in range(len(ylennykset)): # Sijoitetaan luodut merkit
            luotu_savellaji.blit(ylennykset[i][0],(x, ylennykset_paikat_y[i]))
            x += ylennykset[i][0].get_width()

        savellaji_keskus = 2 * rivivali * m

    elif taso < 0: # Alennukset
        taso = taso * -1
        alennukset = []
        alennukset_paikat_y = [40 * m, 10 * m, 50 * m, 20 * m, 60 * m, 30 * m, 70 * m]

        for i in range(0, taso): # Luodaan tarvittava määrä merkkejä
            alennukset.append(Luo_Alennus(vari, mittakaava))

        luotu_savellaji = pygame.Surface((alennukset[0][0].get_width() * len(alennukset), 7 * rivivali * m), pygame.SRCALPHA)

        for i in range(len(alennukset)): # Sijoitetaan luodut merkit
            luotu_savellaji.blit(alennukset[i][0],(x, alennukset_paikat_y[i]))
            x += alennukset[i][0].get_width()

        savellaji_keskus = 2 * rivivali * m

    else: # Jos ei sävellajia löytynyt
        luotu_savellaji = pygame.Surface((0,0), pygame.SRCALPHA)
        savellaji_keskus = 0

    return luotu_savellaji, savellaji_keskus