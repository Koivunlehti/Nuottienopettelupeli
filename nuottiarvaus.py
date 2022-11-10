import pygame

pygame.init()
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
kosk_maara = 36
kosk_vali = 2
kosk_leveys = (naytto_leveys - (kosk_maara * kosk_vali)) / kosk_maara
kosk_korkeus = 100
for i in range(kosk_maara):
    koskettimet_valkoinen.append(pygame.Rect(kosk_vali + i * kosk_leveys, naytto_korkeus - kosk_korkeus, kosk_leveys, kosk_korkeus))
    kosk_vali += 2

# Mustien koskettimien alustus
kosk_maara = 25
kosk_vali = kosk_leveys / 1.5
kosk_korkeus_musta = 50
for i in range(kosk_maara):
    koskettimet_musta.append(pygame.Rect(kosk_vali + i * kosk_leveys, naytto_korkeus -  2 * kosk_korkeus_musta, kosk_leveys, kosk_korkeus_musta))
    if i in [1,4,6,9,11,14,16,19,21,24]:
        kosk_vali += 4 + kosk_leveys
    else:
        kosk_vali += 2

while True:
    naytto.fill((0,0,0))

    for tapahtuma in pygame.event.get():
        if tapahtuma.type == pygame.QUIT:   # Ikkunan yläkulman X painike
            exit()
        if tapahtuma.type == pygame.MOUSEBUTTONDOWN:    # Hiiren painike alas

            musta_klikattu = False
            for kosketin in koskettimet_musta:
                if kosketin.collidepoint(tapahtuma.pos):
                    musta_klikattu = True
                    print("musta")
                    break
            if musta_klikattu == False:
                for kosketin in koskettimet_valkoinen:
                    if kosketin.collidepoint(tapahtuma.pos):
                        print("valkoinen")

    # Koskettimien piirto
    hiiri_x, hiiri_y = pygame.mouse.get_pos()
    hiiri_mustan_paalla = False
    for kosketin in koskettimet_musta:
        if kosketin.x <= hiiri_x <= kosketin.x + kosk_leveys and kosketin.y <= hiiri_y <= kosketin.y + kosk_korkeus_musta:
            hiiri_mustan_paalla = True
            break

    for kosketin in koskettimet_valkoinen:
        if kosketin.x <= hiiri_x <= kosketin.x + kosk_leveys and kosketin.y <= hiiri_y <= kosketin.y + kosk_korkeus and hiiri_mustan_paalla == False:
            pygame.draw.rect(naytto,(140,140,140),kosketin)
        else:
            pygame.draw.rect(naytto,(240,240,240),kosketin)
    
    for kosketin in koskettimet_musta:
        if kosketin.x <= hiiri_x <= kosketin.x + kosk_leveys and kosketin.y <= hiiri_y <= kosketin.y + kosk_korkeus_musta:
            pygame.draw.rect(naytto,(140,140,140),kosketin)
        else:
            pygame.draw.rect(naytto,(50,50,50),kosketin)
        

    pygame.display.flip()

    kello.tick(60)

