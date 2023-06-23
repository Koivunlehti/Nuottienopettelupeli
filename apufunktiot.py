""" Tämä moduuli sisältää sekalaisia funktioita
"""

def Luo_Nuottien_Paikat(keski_c_y:float, vali:float):
    """Luo ja määrittelee koordinaatit eri sävelille viivastolla

    Parametrit
    ----------
    keski_c_y : float
        Keski-C:n koordinaatti y-akselilla viivastolla 

    vali : float
        Sävelien väliin jätettävä tila y-akselilla
            
    Palauttaa
    ---------
    dict
        Palauttaa sanakirja muotoisen taulukon jossa on sävelen y-koordinaatti ja sävelen koskettimen väri.
        Avain: sävelen midi-arvo, Arvo: (sävelen y-koordinaatti, koskettimen väri)

    """
    paikat = {}
    valkeat_keski_c_alla = 35
    y = keski_c_y + valkeat_keski_c_alla * vali   # Lasketaan y-koordinaatin aloitusarvo perustuen annettuun keski_c y-koordinaattiin.
    
    laskuri = 0 # Tätä laskuria käytetään reagoimaan 2 mustan ja 3 mustan koskettimen vaihtoon
    for i in range(128):
        if laskuri < 5:
            if laskuri % 2 == 0:    # valkoiset
                    paikat[i] = (y,"v")
                    if laskuri + 1 == 5:
                        y -= vali
            else:                   # mustat
                    paikat[i] = (y,"m")
                    y -= vali
        else:
            if laskuri % 2 == 0:    # mustat
                    paikat[i] = (y,"m")
                    y -= vali
            else:                   # valkoiset 
                    paikat[i] = (y,"v")
                    if laskuri + 1 == 12:
                        y -= vali
            
        if laskuri + 1 == 12:
            laskuri = 0
        else:
            laskuri += 1
            
    return paikat

def Tarkista_Savellaji_Vaikutus(savellaji, midi_savel):
    """ Tarkistaa miten sävellaji vaikuttaa annettuun säveleen.

    Parametrit
    ----------
    savellaji : str
        Sävellaji jota käytetään. Annetaan kirjallisessa muodossa, esim: "C", "A", "eb" jne. 

    midi_savel : int
        Sen sävelen midi-arvo jota ollaan tarkistamassa
            
    Palauttaa
    ---------
    str
        Palauttaa merkin, joka kertoo sävellajin vaikutuksen.
        "y": sävel on ylennetty, "a": sävel on alennettu, "": ei vaikutusta

    """
    savelet = []
    duurit = {"Cb":-7, "Gb":-6, "Db":-5, "Ab":-4, "Eb":-3, "B":-2 , "F":-1 , "C":0, "G":1, "D":2, "A":3 , "E":4 , "H":5 , "F#":6, "C#":7}
    mollit = {"ab":-7, "eb":-6, "b":-5, "f":-4, "c":-3, "g":-2 , "d":-1 , "a":0, "e":1, "h":2, "f#":3 , "c#":4 , "g#":5 , "d#":6, "a#":7}

    # Tarkistetaan onko annettu savellaji olemassa ja montako ylennys tai alennusmerkkiä sillä on
    taso = 0
    if savellaji in duurit:
        taso = duurit[savellaji]
    elif savellaji in mollit:
        taso = mollit[savellaji]

    # Apufunktio sävelien hakuun
    def Luo_Savelet(savel, taulukko):
        while savel < 128:
            taulukko.append(savel)
            savel += 12
        return taulukko

    # Kerätään midisäveliä vertaustaulukkoon riippuen siitä, kuinka montaa säveltä sävellaji ylentää tai alentaa
    if taso > 0:
        for i in range(taso):
            if i + 1 == 1:
                savelet = Luo_Savelet(5, savelet) # F
            elif i + 1 == 2:
                savelet = Luo_Savelet(0, savelet) # C
            elif i + 1 == 3:
                savelet = Luo_Savelet(7, savelet) # G
            elif i + 1 == 4:
                savelet = Luo_Savelet(2, savelet) # D
            elif i + 1 == 5:
                savelet = Luo_Savelet(9, savelet) # A
            elif i + 1 == 6:
                savelet = Luo_Savelet(4, savelet) # E
            elif i + 1 == 7:
                savelet = Luo_Savelet(11, savelet) # H

        if midi_savel in savelet:   # Löytyykö haettu midisävel ylennettyjen sävelten joukosta
            return "y"

    elif taso < 0:
        for i in range(0, taso, -1):
            if i - 1 == -1:
                savelet = Luo_Savelet(11, savelet) # H
            elif i - 1 == -2:
                savelet = Luo_Savelet(4, savelet) # E
            elif i - 1 == -3:
                savelet = Luo_Savelet(9, savelet) # A
            elif i - 1 == -4:
                savelet = Luo_Savelet(2, savelet) # D
            elif i - 1 == -5:
                savelet = Luo_Savelet(7, savelet) # G
            elif i - 1 == -6:
                savelet = Luo_Savelet(0, savelet) # C
            elif i - 1 == -7:
                savelet = Luo_Savelet(5, savelet) # F

        if midi_savel in savelet:   # Löytyykö haettu midisävel alennettujen sävelten joukosta
            return "a"
    
    return ""

def Savel_Tekstina(midi_arvo, savelen_tila = ""):
    """ Palauttaa pyydetyn sävelen tekstimuodossa

    Parametrit
    ----------
    midi_arvo : int
        Sävelen midiarvo

    savelen_tila : str
        Sävelen tila. Tämä vaikuttaa siihen, miten sävel nimetään.
        "y" = ylennetty, "a" = alennettu, "" = normaali
            
    Palauttaa
    ---------
    tuple
        Palauttaa sävelen nimen ja oktaavin muodossa (sävelen nimi, oktaavi)
    """
    savelet = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","H"]
    savelet_ylen = ["H#","C#","D","D#","E","E#","F#","G","G#","A","A#","H"]
    savelet_alen = ["C","Db","D","Eb","Fb","F","Gb","G","Ab","A","Hb","Cb"]

    laskuri = 0
    oktaavi = -1
    savel = ""
    for i in range(0,128):
        if i == midi_arvo:
            if savelen_tila == "y":
                savel = savelet_ylen[laskuri]
            elif savelen_tila == "a":
                savel = savelet_alen[laskuri]
            else:
                savel = savelet[laskuri]
            break
        if laskuri >= 11:
            laskuri = 0
            oktaavi += 1
        else:
            laskuri += 1
    
    return savel, oktaavi