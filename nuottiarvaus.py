import pygame
import pygame.midi
import random

def Piirra_Viivasto(x, y, rivivali, viivastojen_vali):
    for i in range(5):
        pygame.draw.line(naytto, (200,200,200), ( x, y + i * rivivali ), ( naytto_leveys, y + i * rivivali ))

    for i in range(5):
        pygame.draw.line(naytto, (200,200,200), ( x, y + viivastojen_vali + i * rivivali ), ( naytto_leveys, y + viivastojen_vali + i * rivivali ))

def Piirra_F_Avain(x, y, mittakaava = 1):
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

def Piirra_G_Avain(x, y, mittakaava = 1):
    m = mittakaava
    pygame.draw.lines(naytto, (200,200,200), False, [
        ( x, y ), 
        ( x + 15 * m, y - 10 * m ), 
        ( x + 5 * m, y - 20 * m ), 
        ( x - 5 * m, y - 10 * m ), 
        ( x, y ), 
        ( x + 20 * m, y ), 
        ( x + 30 * m, y - 20 * m ), 
        ( x + 5 * m, y - 130 * m ), 
        ( x + 20 * m, y - 155 * m ), 
        ( x + 30 * m, y - 135 * m ), 
        ( x + 20 * m, y - 120 * m ), 
        ( x - 15 * m, y - 75 * m ), 
        ( x - 10 * m, y - 45 * m ), 
        ( x + 10 * m, y - 35 * m ), 
        ( x + 35 * m, y - 40 * m ), 
        ( x + 40 * m, y - 60 * m ), 
        ( x + 30 * m, y - 75 * m ), 
        ( x + 10 * m, y - 70 * m ), 
        ( x + 5 * m, y - 55  * m ), 
        ( x + 15 * m, y - 45 * m ), 
        ( x + 25 * m, y - 55 * m )], 4)

    pygame.draw.circle(naytto, (200,200,200), [ x + 5 * m, y - 10 * m ], 10) # G-avaimen päätypallo

def Piirra_Ylennys(x, y, mittakaava = 1):
    m = mittakaava
    pygame.draw.line(naytto, (200,200,200), ( x - 25 * m, y - 5 * m ), ( x - 25 * m, y + 25 * m ), 3) # Vasen pystyviiva
    pygame.draw.line(naytto, (200,200,200), ( x - 15 * m, y - 7 * m ), ( x - 15 * m, y + 23 * m ), 3) # Oikea pystyviiva
    pygame.draw.line(naytto, (200,200,200), ( x - 35 * m, y + 5 * m ), ( x - 5 * m, y + 3 * m ), 4) # Ylin vaakaviiva
    pygame.draw.line(naytto, (200,200,200), ( x - 35 * m, y + 15 * m ), ( x - 5 * m, y + 13 * m ), 4) # Alin vaakaviiva

def Piirra_4_Osa_Nuotti(x, y, mittakaava = 1):
    m = mittakaava
    pygame.draw.line(naytto, (200,200,200), ( x + 27 * m, y + 10 * m ), ( x + 27 * m, y + -50 * m ), 4) # Varsiosa
    pygame.draw.ellipse(naytto, (200,200,200), [ x, y, 30 * m, 20 * m ]) # Pääosa

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

    # Varmistetaan ettei koskettimisto lopu mustaan koskettimeen
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

# Koskettimet
alku_midi = 36
loppu_midi = 84
kosk_korkeus = 100
koskettimet_valkoinen, koskettimet_musta = Luo_Koskettimet(alku_midi, loppu_midi, kosk_korkeus, naytto_leveys, naytto_korkeus)

# Haettavan nuotin muuttujat
luo_nuotti = True
ylennetty = False
nuotti_x = 0
nuotti_y = 0
nuotti_midi = 0

# Rajaviivan sijainti
rajaviiva_x = 150
rajaviiva_y = 50
rajaviiva_pituus_x = rajaviiva_x
rajaviiva_pituus_y = 400

# Arvausalue
arvausalue_x = rajaviiva_x + 4
arvausalue_y = 50
arvausalue_leveys = 350
arvausalue_korkeus = 350

# Pisteet
pisteet = 0

# pelisilmukka
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
        paikat_diskantti = Luo_Nuottien_Paikat(190, 10)
        paikat_basso = Luo_Nuottien_Paikat(230,10)
        kosketin_vari = "v"

        if random.randrange(0,2) == 0:  # Arvotaan diskantti ja bassorivin välillä. 0 = diskanttirivi, 1 = bassorivi  
            nuotti_midi = random.randrange(60,loppu_midi)
            nuotti_y = paikat_diskantti[nuotti_midi][0]
            kosketin_vari = paikat_diskantti[nuotti_midi][1]
        else:
            nuotti_midi = random.randrange(alku_midi,60)
            nuotti_y = paikat_basso[nuotti_midi][0]
            kosketin_vari = paikat_diskantti[nuotti_midi][1]

        # Jos nuotti on mustalla koskettimella, piirretään ylennysmerkki
        if kosketin_vari == "m":
            ylennetty = True
        else:
            ylennetty = False

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
    pygame.draw.line(naytto, (222,40,20), (rajaviiva_x, rajaviiva_y), (rajaviiva_pituus_x ,rajaviiva_pituus_y), 4)
    
    # Arvausalue piirto
    pygame.draw.rect(naytto, (6,148,3), [arvausalue_x, arvausalue_y, arvausalue_leveys, arvausalue_korkeus])
    
    # Viivaston piirto
    Piirra_Viivasto(0, 100, 20, 160)

    # G-Nuottiavain piirto
    Piirra_G_Avain(50, 220)

    # F-Nuottiavain piirto
    Piirra_F_Avain(50, 280)
    
    # Ylennysmerkin piirto
    if ylennetty:
        Piirra_Ylennys(nuotti_x, nuotti_y)
    
    # Nuotti piirto
    Piirra_4_Osa_Nuotti(nuotti_x, nuotti_y)

    pisteet_teksti = fontti.render(f"Pisteet: {pisteet}", True, "white")
    naytto.blit(pisteet_teksti, (0, naytto_korkeus - kosk_korkeus - pisteet_teksti.get_height()))

    pygame.display.flip()

    kello.tick(60)

