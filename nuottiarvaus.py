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

luo_nuotti = True
nuotti_x = 0
nuotti_y = 0
maaliviiva_x = 150
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
                    break
            if musta_klikattu == False:
                for kosketin in koskettimet_valkoinen:
                    if kosketin[0].collidepoint(tapahtuma.pos):
                        soitin.note_off(kosketin[1], 127,1)
                        soitin.note_on(kosketin[1], 127,1)
    
    # Nuotin luominen ja liikutus
    if luo_nuotti:
        nuotti_x = naytto_leveys
        nuotti_y = random.randrange(100, 200)
        luo_nuotti = False
    else:
        if nuotti_x > maaliviiva_x:
            nuotti_x -= 1
        else:
            luo_nuotti = True
            soitin.note_off(60, 127,5)
            soitin.note_on(60, 127,5)

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

    # Maalilinja piirto
    pygame.draw.line(naytto,(222,40,20),(maaliviiva_x,50), (maaliviiva_x ,400),4)
    
    # Arvausalue piirto
    pygame.draw.rect(naytto,(6,148,3),[maaliviiva_x + 4, 50, 350, 350])
    
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

    # Nuotti piirto
    pygame.draw.line(naytto,(200,200,200),(nuotti_x + 27,nuotti_y + 10), (nuotti_x + 27, nuotti_y + -50),4)
    pygame.draw.ellipse(naytto,(200,200,200), [nuotti_x, nuotti_y, 30, 20])

    pygame.display.flip()

    kello.tick(60)

