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

kosk_maara = 36
kosk_vali = 2
kosk_leveys = (naytto_leveys - (kosk_maara * kosk_vali)) / kosk_maara
kosk_korkeus = 100
for i in range(kosk_maara):
    koskettimet_valkoinen.append(pygame.Rect(kosk_vali + i * kosk_leveys, naytto_korkeus - kosk_korkeus, kosk_leveys, kosk_korkeus))
    kosk_vali += 2

kosk_maara = 25
kosk_vali = kosk_leveys / 1.5
kosk_korkeus = 50
for i in range(kosk_maara):
    koskettimet_musta.append(pygame.Rect(kosk_vali + i * kosk_leveys, naytto_korkeus -  2 * kosk_korkeus, kosk_leveys, kosk_korkeus))
    if i in [1,4,6,9,11,14,16,19,21,24]:
        kosk_vali += 4 + kosk_leveys
    else:
        kosk_vali += 2

while True:
    naytto.fill((0,0,0))

    for tapahtuma in pygame.event.get():
        if tapahtuma.type == pygame.QUIT:   # Ikkunan yläkulman X painike
            exit()
    
    for kosketin in koskettimet_valkoinen:
        pygame.draw.rect(naytto,(240,240,240),kosketin)
    
    for kosketin in koskettimet_musta:
        pygame.draw.rect(naytto,(50,50,50),kosketin)

    pygame.display.flip()

    kello.tick(60)

