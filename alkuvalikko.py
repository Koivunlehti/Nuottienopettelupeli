import pygame
import pygame.midi
from pygame.locals import *
from nuottiarvaus import Nuottiarvaus
from kuule_savel import Kuule_Savel
import ui_komponentit

pygame.init()

# Soitin
pygame.midi.init()
midi_soitin_id = pygame.midi.get_default_output_id()
soitin_tiedot = ()
if midi_soitin_id != -1:
    soitin = pygame.midi.Output(midi_soitin_id)
    soitin_tiedot = pygame.midi.get_device_info(midi_soitin_id)

# Näyttö
pygame.display.set_caption("Alkuvalikko")
naytto = pygame.display.set_mode((1000, 800), RESIZABLE)

# Painikkeet
painikkeet_hiiri_paalla = [False, False]

# Kello
kello = pygame.time.Clock()

# Pelisilmukka
while True:
    naytto.fill((0, 0, 0))
    
    # Käyttöliittymän luonti
    if midi_soitin_id != -1:
        painike_nuottiarvaus = ui_komponentit.Luo_Painike(taustavari=(110,110,110), taustavari_hiiri_paalla=(180,180,180), hiiri_paalla=painikkeet_hiiri_paalla[0], teksti="Nuottiarvaus", teksti_koko=48, reunus=20, lihavoitu=True)
        painike_nuottiarvaus = naytto.blit(painike_nuottiarvaus, (naytto.get_width() / 2 - painike_nuottiarvaus.get_width() / 2, naytto.get_height() / 2 - painike_nuottiarvaus.get_height() / 2))
        painike_kuule_savel = ui_komponentit.Luo_Painike(taustavari=(110,110,110), taustavari_hiiri_paalla=(180,180,180), hiiri_paalla=painikkeet_hiiri_paalla[1], teksti="Kuule sävel", teksti_koko=48, reunus=20, lihavoitu=True)
        painike_kuule_savel = naytto.blit(painike_kuule_savel, (naytto.get_width() / 2 - painike_kuule_savel.get_width() / 2, naytto.get_height() / 2 - painike_kuule_savel.get_height() / 2 + painike_nuottiarvaus.height + 20))

    teksti_otsikko = ui_komponentit.Luo_Teksti(teksti="Tervetuloa", koko=72, lihavoitu=True)
    naytto.blit(teksti_otsikko, (naytto.get_width() / 2 - teksti_otsikko.get_width() / 2, 100))
    if midi_soitin_id != -1:
        teksti_ohje = ui_komponentit.Luo_Teksti(teksti="Valitse peli...", koko=30)
        naytto.blit(teksti_ohje, (naytto.get_width() / 2 - teksti_ohje.get_width() / 2, 200))

        teksti_midi_soitin = ui_komponentit.Luo_Teksti(teksti=f"MIDI ulostulo: {soitin_tiedot[0].decode('ascii')}, {soitin_tiedot[1].decode('ascii')}", koko=20)
        naytto.blit(teksti_midi_soitin,(0,naytto.get_height() - teksti_midi_soitin.get_height()))
    else:
        teksti_ohje = ui_komponentit.Luo_Teksti(teksti="Käyttäjärjestelmääsi ei ole määritetty MIDI-soitinta!", koko=30, vari=(200,50,50))
        teksti_ohje_2 = ui_komponentit.Luo_Teksti(teksti="Peliä ei voi jatkaa!", koko=30, vari=(200,50,50))
        teksti_ohje = naytto.blit(teksti_ohje, (naytto.get_width() / 2 - teksti_ohje.get_width() / 2, 200))
        naytto.blit(teksti_ohje_2, (naytto.get_width() / 2 - teksti_ohje_2.get_width() / 2, teksti_ohje.y + teksti_ohje.height + 10))
    
    for tapahtuma in pygame.event.get():
        # Ikkunan yläkulman X painike
        if tapahtuma.type == pygame.QUIT:   
            exit()

        # Ikkunan koon muutos 
        if tapahtuma.type == pygame.VIDEORESIZE:    
            # Ruudun minimikoko
            if pygame.display.get_window_size()[0] < 750:
               naytto = pygame.display.set_mode((750, pygame.display.get_window_size()[1]), RESIZABLE)
            if pygame.display.get_window_size()[1] < 700:
               naytto = pygame.display.set_mode((pygame.display.get_window_size()[0], 700), RESIZABLE)
               
        # Hiiren vasen painike alhaalla
        if tapahtuma.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[0] == True:
            if painike_nuottiarvaus.collidepoint(tapahtuma.pos):
                peli = Nuottiarvaus(soitin, pygame.display.get_window_size())
                peli.Aloita()
            elif painike_kuule_savel.collidepoint(tapahtuma.pos):
                peli = Kuule_Savel(soitin, pygame.display.get_window_size())
                peli.Aloita()
 
    # Hiiri päällä
    hiiri_x, hiiri_y = pygame.mouse.get_pos()
    if midi_soitin_id != -1:
        if painike_nuottiarvaus.collidepoint(hiiri_x, hiiri_y):
            painikkeet_hiiri_paalla[0] = True
        else:
            painikkeet_hiiri_paalla[0] = False
        
        if painike_kuule_savel.collidepoint(hiiri_x, hiiri_y):
            painikkeet_hiiri_paalla[1] = True
        else:
            painikkeet_hiiri_paalla[1] = False

    pygame.display.flip()  

    # Kellon edistäminen.
    kello.tick(60)