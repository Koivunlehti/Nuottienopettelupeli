import pygame
import pygame.midi
import random
import piirto

def Luo_Koskettimet(alku_midi, loppu_midi, kosk_korkeus, naytto_leveys, naytto_korkeus):
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
    kosk_leveys = (naytto_leveys - (kosk_maara_v * kosk_vali)) / kosk_maara_v
    koskettimet_valkoinen = []

    laskuri = 0
    for i in range(alku, loppu + 1):
        
        if savelet[i] == "v":
            koskettimet_valkoinen.append((pygame.Rect(kosk_vali + laskuri * kosk_leveys, naytto_korkeus - kosk_korkeus, kosk_leveys, kosk_korkeus), i))
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
            koskettimet_musta.append((pygame.Rect(kosk_vali + laskuri * kosk_leveys, naytto_korkeus -  2 * (kosk_korkeus / 2), kosk_leveys, kosk_korkeus / 2), i))
            laskuri += 1
            valk_perakkain = 0

    return koskettimet_valkoinen, koskettimet_musta
    
def Luo_Nuottien_Paikat(keski_c_y, vali):
    paikat = {}
    y = keski_c_y + 35 * vali   # lasketaan y-koordinaatin aloitusarvo perustuen annettuun keski_c y-koordinaattiin
    
    laskuri = 0
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
    savelet = []
    duurit = {"Cb":-7, "Gb":-6, "Db":-5, "Ab":-4, "Eb":-3, "B":-2 , "F":-1 , "C":0, "G":1, "D":2, "A":3 , "E":4 , "H":5 , "F#":6, "C#":7}
    mollit = {"ab":-7, "eb":-6, "b":-5, "f":-4, "c":-3, "g":-2 , "d":-1 , "a":0, "e":1, "h":2, "f#":3 , "c#":4 , "g#":5 , "d#":6, "a#":7}

    # Tarkistetaan onko annettu savellaji olemassa ja montako ylennys tai alennusmerkkiä sillä on
    taso = 0
    if savellaji in duurit:
        taso = duurit[savellaji]
    elif savellaji in mollit:
        taso = mollit[savellaji]

    # Apumetodi
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

pygame.init()

# Midi soittimen alustus
pygame.midi.init()
soitin = pygame.midi.Output(0)
soitin.set_instrument(0,1)
soitin.set_instrument(127,5)

# Näytön alustus
pygame.display.set_caption("Nuottiarvaus")
naytto_leveys = 640
naytto_korkeus = 600
naytto = pygame.display.set_mode((naytto_leveys, naytto_korkeus))

# Tekstit ja fontit
fontti = pygame.font.SysFont("Georgia", 48, bold=True)
fontti_2 = pygame.font.SysFont("Georgia", 18, bold=True)
pisteet_teksti = fontti.render("Pisteet: 0", True, "white")

# Kello
kello = pygame.time.Clock()

# Viivasto
diskantti_keski_c_y = 200
basso_keski_c_y =  260
viivasto_rivivali = 20
viivasto_paikat = {"diskantti": piirto.Piirra_Viivasto(naytto, 0, diskantti_keski_c_y, viivasto_rivivali, True), "basso": piirto.Piirra_Viivasto(naytto, 0, basso_keski_c_y, viivasto_rivivali, False)}

# Koskettimet
alku_midi = 36
loppu_midi = 84
kosk_korkeus = 100
koskettimet_valkoinen, koskettimet_musta = Luo_Koskettimet(alku_midi, loppu_midi, kosk_korkeus, naytto_leveys, naytto_korkeus)

# Haettavan nuotin muuttujat
paikat_diskantti = Luo_Nuottien_Paikat(viivasto_paikat["diskantti"][0] + viivasto_rivivali, 10)
paikat_basso = Luo_Nuottien_Paikat(viivasto_paikat["basso"][0] - viivasto_rivivali, 10)
luo_nuotti = True
ylennetty = False
alennettu = False
nuotti_x = 0
nuotti_y = 0
nuotti_midi = 0
diskantti = True

# Rajaviivan sijainti
rajaviiva_x = 150
rajaviiva_y = 0
rajaviiva_pituus_x = rajaviiva_x
rajaviiva_pituus_y = 450
rajaviiva_paksuus = 4

# Arvausalue
arvausalue_x = rajaviiva_x + rajaviiva_paksuus
arvausalue_y = rajaviiva_y
arvausalue_leveys = 350
arvausalue_korkeus = rajaviiva_pituus_y - rajaviiva_y

# Pisteet
pisteet = 0

# Pelisilmukka
while True:
    naytto.fill((0,0,0))
    
    for tapahtuma in pygame.event.get():
        if tapahtuma.type == pygame.QUIT:   # Ikkunan yläkulman X painike
            exit()

        if tapahtuma.type == pygame.MOUSEBUTTONDOWN:    # Hiiren painike alas
            musta_klikattu = False
            for kosketin in koskettimet_musta:
                if kosketin[0].collidepoint(tapahtuma.pos):
                    musta_klikattu = True
                    soitin.note_off(kosketin[1], 127, 1)
                    soitin.note_on(kosketin[1], 127, 1)

                    #Painetun koskettimen vertaaminen haettavaan nuottiin
                    if kosketin[1] == nuotti_midi:
                        if nuotti_x <= arvausalue_x + arvausalue_leveys:
                            luo_nuotti = True
                            pisteet += 1
                    break

            if musta_klikattu == False:
                for kosketin in koskettimet_valkoinen:
                    if kosketin[0].collidepoint(tapahtuma.pos):
                        soitin.note_off(kosketin[1], 127,1)
                        soitin.note_on(kosketin[1], 127,1)

                        # Painetun koskettimen vertaaminen haettavaan nuottiin
                        if kosketin[1] == nuotti_midi:
                            if nuotti_x <= arvausalue_x + arvausalue_leveys:
                                luo_nuotti = True
                                pisteet += 1
                        break

    # Nuotin luominen ja liikutus
    if luo_nuotti:
        kosketin_vari = "v"
        ylennetty = False
        alennettu = False
    
        if random.randrange(0,2) == 0:       # Arvotaan nuotin sävel diskantti- tai bassoviivastolta
            nuotti_midi = random.randrange(57,loppu_midi)
            kosketin_vari = paikat_diskantti[nuotti_midi][1]
            if kosketin_vari == "m":
                nuotti_midi -= 1
                kosketin_vari = paikat_diskantti[nuotti_midi][1]
            nuotti_y = paikat_diskantti[nuotti_midi][0]
            diskantti = True
        else:
            nuotti_midi = random.randrange(alku_midi,65)
            kosketin_vari = paikat_basso[nuotti_midi][1]
            if kosketin_vari == "m":
                nuotti_midi -= 1
                kosketin_vari = paikat_basso[nuotti_midi][1]
            nuotti_y = paikat_basso[nuotti_midi][0]
            diskantti = False

        muutos = random.randrange(0,3)      # Arvotaan ylennetäänkö, alennetaanko vai pidetäänkö nuotti normaalina
        if muutos == 1:
            if diskantti and nuotti_midi + 1 <= loppu_midi:
                nuotti_midi += 1
                ylennetty = True
            elif not diskantti and nuotti_midi + 1 <= 65:
                nuotti_midi += 1
                ylennetty = True
        elif muutos == 2:
            if diskantti and nuotti_midi - 1 >= 57:
                nuotti_midi -= 1
                alennettu = True
            elif not diskantti and nuotti_midi - 1 >= alku_midi:
                nuotti_midi -= 1
                alennettu = True

        nuotti_x = naytto_leveys
        luo_nuotti = False

    else:
        if nuotti_x > rajaviiva_x:
            nuotti_x -= 1
        else:
            luo_nuotti = True
            soitin.note_off(60, 127,5)
            soitin.note_on(60, 127,5)
            pisteet -= 10

    # Koskettimien piirto 
    hiiri_x, hiiri_y = pygame.mouse.get_pos()
    hiiri_mustan_paalla = False 

    for kosketin in koskettimet_musta:  # Tarkistetaan onko hiiri mustan koskettimen päällä. Tämä pitää huomioida koska mustat ja valkoiset koskettimet ovat päällekkäin
        if kosketin[0].x <= hiiri_x <= kosketin[0].x + kosketin[0].width and kosketin[0].y <= hiiri_y <= kosketin[0].y + kosketin[0].height:
            hiiri_mustan_paalla = True
            break

    for kosketin in koskettimet_valkoinen:  # Piirretään varkoiset koskettimet ensin. Jos hiiri havaitaan koskettimen päällä, koskettimen väritystä muutetaan 
        if kosketin[0].x <= hiiri_x <= kosketin[0].x + kosketin[0].width and kosketin[0].y <= hiiri_y <= kosketin[0].y + kosketin[0].height and hiiri_mustan_paalla == False:
            pygame.draw.rect(naytto,(140,140,140),kosketin[0])
        else:
            pygame.draw.rect(naytto,(240,240,240),kosketin[0])
        if kosketin[1] == 60:
            teksti = fontti_2.render("C", True, "black")
            naytto.blit(teksti, (kosketin[0].x, kosketin[0].y + 80))

    for kosketin in koskettimet_musta:  # Piirretään mustat koskettimet. Jos hiiri havaitaan koskettimen päällä, koskettimen väritystä muutetaan
        if kosketin[0].x <= hiiri_x <= kosketin[0].x + kosketin[0].width and kosketin[0].y <= hiiri_y <= kosketin[0].y + kosketin[0].height:
            pygame.draw.rect(naytto,(140,140,140),kosketin[0])
        else:
            pygame.draw.rect(naytto,(50,50,50),kosketin[0])

    # Rajaviivan piirto
    pygame.draw.line(naytto, (222,40,20), (rajaviiva_x, rajaviiva_y), (rajaviiva_pituus_x ,rajaviiva_pituus_y), rajaviiva_paksuus)
    
    # Arvausalue piirto
    pygame.draw.rect(naytto, (6,148,3), [arvausalue_x, arvausalue_y, arvausalue_leveys, arvausalue_korkeus])
    
    # Viivaston piirto
    piirto.Piirra_Viivasto(naytto, 0, diskantti_keski_c_y, viivasto_rivivali, True)
    piirto.Piirra_Viivasto(naytto, 0, basso_keski_c_y, viivasto_rivivali, False)

    # G-Nuottiavain piirto
    piirto.Piirra_G_Avain(naytto, 50, viivasto_paikat["diskantti"][1])

    # F-Nuottiavain piirto
    piirto.Piirra_F_Avain(naytto, 50, viivasto_paikat["basso"][1])

    # Sävellajin merkkien piirto
    piirto.Piirra_Savellaji(naytto,150, "C", paikat_diskantti, True)
    piirto.Piirra_Savellaji(naytto,150, "C", paikat_basso, False)

    # Mahdollisten apuviivojen piirto
    if diskantti:
        if nuotti_y < viivasto_paikat["diskantti"][4] - viivasto_rivivali - viivasto_rivivali / 2:
            piirto.Piirra_Apuviivat(naytto, nuotti_x - 10, viivasto_paikat["diskantti"][4] , 50, viivasto_rivivali, 2, False)
        elif nuotti_y < viivasto_paikat["diskantti"][4] - viivasto_rivivali / 2:
            piirto.Piirra_Apuviivat(naytto, nuotti_x - 10, viivasto_paikat["diskantti"][4], 50, viivasto_rivivali, 1, False)
        elif nuotti_y > viivasto_paikat["diskantti"][0] + viivasto_rivivali:
            piirto.Piirra_Apuviivat(naytto, nuotti_x - 10, viivasto_paikat["diskantti"][0], 50, viivasto_rivivali, 2, True)
        elif nuotti_y > viivasto_paikat["diskantti"][0]:
            piirto.Piirra_Apuviivat(naytto, nuotti_x - 10, viivasto_paikat["diskantti"][0], 50, viivasto_rivivali, 1, True)
    else:
        if nuotti_y < viivasto_paikat["basso"][0] - viivasto_rivivali - viivasto_rivivali / 2:
            piirto.Piirra_Apuviivat(naytto, nuotti_x - 10, viivasto_paikat["basso"][0], 50, viivasto_rivivali, 2, False)
        elif nuotti_y < viivasto_paikat["basso"][0] - viivasto_rivivali / 2:
            piirto.Piirra_Apuviivat(naytto, nuotti_x - 10, viivasto_paikat["basso"][0], 50, viivasto_rivivali, 1, False)
        elif nuotti_y > viivasto_paikat["basso"][4] + viivasto_rivivali:
            piirto.Piirra_Apuviivat(naytto, nuotti_x - 10, viivasto_paikat["basso"][4], 50, viivasto_rivivali, 2, True)
        elif nuotti_y > viivasto_paikat["basso"][4]:
            piirto.Piirra_Apuviivat(naytto, nuotti_x - 10, viivasto_paikat["basso"][4], 50, viivasto_rivivali, 1, True)

    # Ylennysmerkin piirto
    if ylennetty:
        piirto.Piirra_Ylennys(naytto, nuotti_x, nuotti_y, -20)
    if alennettu:
        piirto.Piirra_Alennus(naytto, nuotti_x, nuotti_y, -20)

    # Nuotti piirto
    piirto.Piirra_4_Osa_Nuotti(naytto, nuotti_x, nuotti_y)

    # Pisteiden piirto
    pisteet_teksti = fontti.render(f"Pisteet: {pisteet}", True, "white")
    naytto.blit(pisteet_teksti, (0, naytto_korkeus - kosk_korkeus - pisteet_teksti.get_height()))

    pygame.display.flip()

    kello.tick(60)

