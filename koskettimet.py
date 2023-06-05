"""
Tämä moduuli vastaa koskettimiin liittyvistä toimista
"""

import pygame

def Luo_Koskettimet(naytto:pygame.Surface, alku_midi:int, loppu_midi:int, kosk_korkeus:int):
    """Luo koskettimiston

    Parametrit
    ----------
    naytto : pygame.Surface
        Näyttönä toimiva pygame.Surface olio 

    alku_midi : int
        Ensimmäisen koskettimen midi-arvo

    loppu_midi : int
        Viimeisen koskettimen midi-arvo
        
    kosk_korkeus : int
        Kuinka korkeat koskettimet ovat (y-akseli)
            
    Palauttaa
    ---------
    list, list
        Palautuksena annetaan kaksi erillistä list-tyypistä taulukkoa, joissa erikseen valkoiset ja mustat koskettimet.
        Taulukkojen sisältönä on pygame.Rect olioita

    """
    savelet = {}
    alku = alku_midi
    loppu = loppu_midi
    kosk_maara_v = 0
    kosk_maara_m = 0
    
    # Määritellään jokaisen midi-nuotin kohdalla minkä värinen kosketin se on
    laskuri = 0
    for i in range(128):
        if laskuri < 5:
            if laskuri % 2 == 0:
                savelet[i] = "v"
                if i >= alku and i <= loppu:
                    kosk_maara_v += 1
            else:
                savelet[i] = "m"
                if i >= alku and i <= loppu:
                    kosk_maara_m += 1
        else:
            if laskuri % 2 == 0:
                savelet[i] = "m"
                if i >= alku and i <= loppu:
                    kosk_maara_m += 1
            else:
                savelet[i] = "v"
                if i >= alku and i <= loppu:
                    kosk_maara_v += 1

        if laskuri + 1 == 12:
            laskuri = 0
        else:
            laskuri += 1

    # Varmistetaan ettei koskettimisto ala tai lopu mustaan koskettimeen
    if savelet[alku_midi] == "m":
        alku -= 1
        kosk_maara_v += 1
    if savelet[loppu_midi] == "m":
        loppu += 1
        kosk_maara_v += 1

    # Valkoisten koskettimien luominen 
    kosk_vali = 2
    kosk_leveys = (naytto.get_width() - (kosk_maara_v * kosk_vali)) / kosk_maara_v
    koskettimet_valkoinen = []

    laskuri = 0
    for i in range(alku, loppu + 1):
        
        if savelet[i] == "v":
            koskettimet_valkoinen.append((pygame.Rect(kosk_vali + laskuri * kosk_leveys, naytto.get_height() - kosk_korkeus, kosk_leveys, kosk_korkeus), i))
            kosk_vali += 2 
            laskuri += 1

    # Mustien koskettimien luominen
    kosk_vali = kosk_leveys / 1.5
    koskettimet_musta = []
    
    laskuri = 0
    valk_perakkain = 0

    for i in range(alku, loppu + 1):
        if savelet[i] == "v":
            valk_perakkain += 1
        if savelet[i] == "m":
            if valk_perakkain == 1:
                kosk_vali += 2
            else: 
                kosk_vali += 4 + kosk_leveys
            koskettimet_musta.append((pygame.Rect(kosk_vali + laskuri * kosk_leveys, naytto.get_height() -  2 * (kosk_korkeus / 2), kosk_leveys, kosk_korkeus / 2), i))
            laskuri += 1
            valk_perakkain = 0

    return koskettimet_valkoinen, koskettimet_musta