import pygame
import pygame.midi

pygame.init()

# Midi soittimen alustus
pygame.midi.init()
soitin = pygame.midi.Output(0)
soitin.set_instrument(0,1)

# Näytön alustus
pygame.display.set_caption("Testi")
naytto_leveys = 640
naytto_korkeus = 480
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
                    soitin.note_on(kosketin[1], 127,1)
                    break
            if musta_klikattu == False:
                for kosketin in koskettimet_valkoinen:
                    if kosketin[0].collidepoint(tapahtuma.pos):
                        soitin.note_on(kosketin[1], 127,1)

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
        
    pygame.display.flip()

    kello.tick(60)

