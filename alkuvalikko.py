import pygame
import pygame.midi
from pygame.locals import *
from nuottiarvaus import Nuottiarvaus

pygame.init()

# Näyttö
pygame.display.set_caption("Alkuvalikko")
naytto = pygame.display.set_mode((1000, 800), RESIZABLE)

# Fontit
fontti_otsikko = pygame.font.SysFont("Georgia", 72, bold=True)
fontti_painike = pygame.font.SysFont("Georgia", 48, bold=True)
fontti_normaali = pygame.font.SysFont("Georgia", 30)

# Tekstit
teksti_otsikko = fontti_otsikko.render("Tervetuloa", True, "white")
teksti_painike = fontti_painike.render("Nuottiarvaus", True, "white")
teksti_ohje = fontti_normaali.render("Valitse peli...", True, "white")

# Painikkeet
painike = pygame.Rect(naytto.get_width() / 2 - teksti_painike.get_width() / 2, 
                      naytto.get_height() / 2 - teksti_painike.get_height() / 2, 
                      teksti_painike.get_width() + 10, 
                      teksti_painike.get_height() + 10)

# Kello
kello = pygame.time.Clock()

# Pelisilmukka
while True:
    naytto.fill((0, 0, 0))
    
    for tapahtuma in pygame.event.get():
        if tapahtuma.type == pygame.QUIT:   # Ikkunan yläkulman X painike
            exit()
    
        if tapahtuma.type == pygame.VIDEORESIZE:    # Ikkunan koon muutos 
            # Ruudun minimikoko
            if pygame.display.get_window_size()[0] < 750:
               naytto = pygame.display.set_mode((750, pygame.display.get_window_size()[1]), RESIZABLE)
            if pygame.display.get_window_size()[1] < 700:
               naytto = pygame.display.set_mode((pygame.display.get_window_size()[0], 700), RESIZABLE)
            
            # Päivitetään koordinaatit
            painike = pygame.Rect(naytto.get_width() / 2 - teksti_painike.get_width() / 2, 
                      naytto.get_height() / 2 - teksti_painike.get_height() / 2, 
                      teksti_painike.get_width() + 10, 
                      teksti_painike.get_height() + 10)

        if tapahtuma.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[0] == True:    # Hiiren vasen painike alhaalla
            if painike.collidepoint(tapahtuma.pos):
                peli = Nuottiarvaus(pygame.display.get_window_size())
                peli.Aloita()
                

    naytto.blit(teksti_otsikko, (naytto.get_width() / 2 - teksti_otsikko.get_width() / 2, 100))
    naytto.blit(teksti_ohje, (naytto.get_width() / 2 - teksti_ohje.get_width() / 2, 200))
 
    # Tarkistetaan onko hiiren kursori painikkeen päällä. Vaihdetaan väriä jos on
    hiiri_x, hiiri_y = pygame.mouse.get_pos()
    if painike.x <= hiiri_x and hiiri_x <= painike.x + painike.width and painike.y <= hiiri_y and hiiri_y <= painike.y + painike.height:  
        pygame.draw.rect(naytto, (180,180,180), painike) 
    else:
        pygame.draw.rect(naytto, (110,110,110), painike)

    # Lisätään teksti painikkeen päälle
    naytto.blit(teksti_painike, (painike.x + 5, painike.y + 5))

    pygame.display.flip()  

    # Kellon edistäminen.
    kello.tick(60)