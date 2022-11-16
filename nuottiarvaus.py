import pygame
import pygame.midi
import random


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
pisteet_teksti = fontti.render("Pisteet: 0", True, "white")

# Kello
kello = pygame.time.Clock()

# Koskettimet
koskettimet_valkoinen = []
koskettimet_musta = []

# Valkoisten koskettimien alustus
midi = 36
kosk_maara = 36
kosk_vali = 2
kosk_leveys = (naytto_leveys - (kosk_maara * kosk_vali)) / kosk_maara
kosk_korkeus = 100
for i in range(kosk_maara):
    koskettimet_valkoinen.append((pygame.Rect(kosk_vali + i * kosk_leveys, naytto_korkeus - kosk_korkeus, kosk_leveys, kosk_korkeus),midi))
    kosk_vali += 2
    if i in [2,6,9,13,16,20,23,27,30,34]:
        midi += 1
    else:   
        midi += 2

# Mustien koskettimien alustus
midi = 37
kosk_maara = 25
kosk_vali = kosk_leveys / 1.5
kosk_korkeus_musta = 50
for i in range(kosk_maara):
    koskettimet_musta.append((pygame.Rect(kosk_vali + i * kosk_leveys, naytto_korkeus -  2 * kosk_korkeus_musta, kosk_leveys, kosk_korkeus_musta), midi))
    if i in [1,4,6,9,11,14,16,19,21,24]:
        kosk_vali += 4 + kosk_leveys
        midi += 3
    else:
        kosk_vali += 2
        midi += 2

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
                    soitin.note_off(kosketin[1], 127,1)
                    soitin.note_on(kosketin[1], 127,1)

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
        paikat_diskantti = [(60,190), (61,190,"#"), (62,180), (63,180,"#"), (64,170), (65,160), (66,160,"#"), (67,150), (68,150,"#"), (69,140), (70,140,"#"), (71,130), (72,120), (73,120,"#"), (74,110), (75,110,"#"), (76,100), (77,90), (78,90,"#"), (79,80), (80,80,"#"), (81,70), (82,70,"#"), (83,60), (84,50)] # (midi, y-koordinaatti)
        paikat_basso = [(36,370), (37,370,"#"), (38,360), (39,360,"#"), (40,350), (41,340), (42,340,"#"), (43,330), (44,330,"#"), (45,320), (46,320,"#"), (47,310), (48,300), (49,300,"#"), (50,290), (51,290,"#"), (52,280), (53,270), (54,270,"#"), (55,260), (56,260,"#"), (57,250), (58,250,"#"), (59,240), (60,230)] # (midi, y-koordinaatti)
        
        if random.randrange(0,2) == 0:  # Arvotaan diskantti ja bassorivin välillä. 0 = diskanttirivi, 1 = bassorivi  
            nuotti = paikat_diskantti[random.randrange(0,len(paikat_diskantti))]
            nuotti_midi = nuotti[0]
            nuotti_y = nuotti[1]
            
        else:
            nuotti = paikat_basso[random.randrange(0,len(paikat_basso))]
            nuotti_midi = nuotti[0]
            nuotti_y = nuotti[1]    
        
        # Jos nuotti on mustalla koskettimella, piirretään ylennysmerkki
        if len(nuotti) >= 3:
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
        if kosketin[0].x <= hiiri_x <= kosketin[0].x + kosk_leveys and kosketin[0].y <= hiiri_y <= kosketin[0].y + kosk_korkeus_musta:
            hiiri_mustan_paalla = True
            break

    for kosketin in koskettimet_valkoinen:  # Piirretään varkoiset koskettimet ensin. Jos hiiri havaitaan koskettimen päällä, koskettimen väritystä muutetaan 
        if kosketin[0].x <= hiiri_x <= kosketin[0].x + kosk_leveys and kosketin[0].y <= hiiri_y <= kosketin[0].y + kosk_korkeus and hiiri_mustan_paalla == False:
            pygame.draw.rect(naytto,(140,140,140),kosketin[0])
        else:
            pygame.draw.rect(naytto,(240,240,240),kosketin[0])
    
    for kosketin in koskettimet_musta:  # Piirretään mustat koskettimet. Jos hiiri havaitaan koskettimen päällä, koskettimen väritystä muutetaan
        if kosketin[0].x <= hiiri_x <= kosketin[0].x + kosk_leveys and kosketin[0].y <= hiiri_y <= kosketin[0].y + kosk_korkeus_musta:
            pygame.draw.rect(naytto,(140,140,140),kosketin[0])
        else:
            pygame.draw.rect(naytto,(50,50,50),kosketin[0])

    # Rajaviivan piirto
    pygame.draw.line(naytto,(222,40,20),(rajaviiva_x, rajaviiva_y), (rajaviiva_pituus_x ,rajaviiva_pituus_y),4)
    
    # Arvausalue piirto
    pygame.draw.rect(naytto,(6,148,3),[arvausalue_x, arvausalue_y, arvausalue_leveys, arvausalue_korkeus])
    
    # Viivaston piirto
    rivivali = 20    
    for i in range(5):
        pygame.draw.line(naytto,(200,200,200),(0,100 + i * rivivali), (naytto_leveys,100 + i * rivivali))

    for i in range(5):
        pygame.draw.line(naytto,(200,200,200),(0,260 + i * rivivali), (naytto_leveys,260 + i * rivivali))

    # G-Nuottiavain piirto
    g_alku_x = 50
    g_alku_y = 220
    mittakaava = 1
    pygame.draw.lines(naytto, (200,200,200), False, [
        (g_alku_x, g_alku_y), 
        (g_alku_x+15 * mittakaava, g_alku_y-10 * mittakaava), 
        (g_alku_x+5 * mittakaava, g_alku_y-20 * mittakaava), 
        (g_alku_x-(5 * mittakaava), g_alku_y-10 * mittakaava), 
        (g_alku_x, g_alku_y), 
        (g_alku_x+20 * mittakaava, g_alku_y), 
        (g_alku_x+30 * mittakaava, g_alku_y-20 * mittakaava), 
        (g_alku_x+5 * mittakaava, g_alku_y-130 * mittakaava), 
        (g_alku_x+20 * mittakaava, g_alku_y-155 * mittakaava), 
        (g_alku_x+30 * mittakaava, g_alku_y-135 * mittakaava), 
        (g_alku_x+20 * mittakaava, g_alku_y-120 * mittakaava), 
        (g_alku_x-(15 * mittakaava), g_alku_y-75 * mittakaava), 
        (g_alku_x-(10 * mittakaava), g_alku_y-45 * mittakaava), 
        (g_alku_x+10 * mittakaava, g_alku_y-35 * mittakaava), 
        (g_alku_x+35 * mittakaava, g_alku_y-40 * mittakaava), 
        (g_alku_x+40 * mittakaava, g_alku_y-60 * mittakaava), 
        (g_alku_x+30 * mittakaava, g_alku_y-75 * mittakaava), 
        (g_alku_x+10 * mittakaava, g_alku_y-70 * mittakaava), 
        (g_alku_x+5 * mittakaava, g_alku_y-55  * mittakaava), 
        (g_alku_x+15 * mittakaava, g_alku_y-45 * mittakaava), 
        (g_alku_x+25 * mittakaava, g_alku_y-55 * mittakaava)],4)

    pygame.draw.circle(naytto, (200,200,200), [g_alku_x + 5 * mittakaava, g_alku_y - 10 * mittakaava], 10)

    # F-Nuottiavain piirto
    f_alku_x = 50
    f_alku_y = 280
    pygame.draw.lines(naytto,(200,200,200), False, [
        (f_alku_x-10 * mittakaava,f_alku_y),
        (f_alku_x,f_alku_y-10 * mittakaava),
        (f_alku_x+10 * mittakaava,f_alku_y),
        (f_alku_x,f_alku_y+10 * mittakaava),
        (f_alku_x-10 * mittakaava,f_alku_y),
        (f_alku_x-10 * mittakaava,f_alku_y-20 * mittakaava),
        (f_alku_x+5 * mittakaava,f_alku_y-30 * mittakaava),
        (f_alku_x+20 * mittakaava,f_alku_y-35 * mittakaava),
        (f_alku_x+40 * mittakaava,f_alku_y-20 * mittakaava),
        (f_alku_x+45 * mittakaava,f_alku_y),
        (f_alku_x+40 * mittakaava,f_alku_y+20 * mittakaava),
        (f_alku_x+25 * mittakaava,f_alku_y+40 * mittakaava),
        (f_alku_x-15 * mittakaava,f_alku_y+70 * mittakaava)],4)
    pygame.draw.circle(naytto, (200,200,200), [f_alku_x * mittakaava,f_alku_y * mittakaava], 10)
    pygame.draw.circle(naytto, (200,200,200), [f_alku_x + 65 * mittakaava,f_alku_y + -10 * mittakaava], 5)
    pygame.draw.circle(naytto, (200,200,200), [f_alku_x + 65 * mittakaava,f_alku_y + 10 * mittakaava], 5)

    # Ylennysmerkin piirto
    if ylennetty:
        pygame.draw.line(naytto,(200,200,200),(nuotti_x - 25, nuotti_y - 5), (nuotti_x - 25, nuotti_y + 25), 3) # vasen pystyviiva
        pygame.draw.line(naytto,(200,200,200),(nuotti_x - 15, nuotti_y - 7), (nuotti_x - 15, nuotti_y + 23), 3) # oikea pystyviiva
        pygame.draw.line(naytto,(200,200,200),(nuotti_x - 35, nuotti_y + 5), (nuotti_x - 5, nuotti_y + 3), 4) # ylin vaakaviiva
        pygame.draw.line(naytto,(200,200,200),(nuotti_x - 35, nuotti_y + 15), (nuotti_x - 5, nuotti_y + 13), 4) # alin vaakaviiva
    
    # Nuotti piirto
    pygame.draw.line(naytto,(200,200,200),(nuotti_x + 27,nuotti_y + 10), (nuotti_x + 27, nuotti_y + -50),4)
    pygame.draw.ellipse(naytto,(200,200,200), [nuotti_x, nuotti_y, 30, 20])

    pisteet_teksti = fontti.render(f"Pisteet: {pisteet}", True, "white")
    naytto.blit(pisteet_teksti,(0,naytto_korkeus - kosk_korkeus - pisteet_teksti.get_height()))

    pygame.display.flip()

    kello.tick(60)

