import pygame
import pygame.midi
import random
import piirto, koskettimet, apufunktiot

pygame.init()

# Midi soittimen alustus
pygame.midi.init()
soitin = pygame.midi.Output(0)
soitin.set_instrument(0,1)
soitin.set_instrument(127,5)

# Näytön alustus
pygame.display.set_caption("Nuottiarvaus")
naytto = pygame.display.set_mode((800, 600))

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
koskettimet_valkoinen, koskettimet_musta = koskettimet.Luo_Koskettimet(naytto, alku_midi, loppu_midi, kosk_korkeus)

# Haettavan nuotin muuttujat
paikat_diskantti = apufunktiot.Luo_Nuottien_Paikat(viivasto_paikat["diskantti"][0] + viivasto_rivivali, 10)
paikat_basso = apufunktiot.Luo_Nuottien_Paikat(viivasto_paikat["basso"][0] - viivasto_rivivali, 10)
luo_nuotti = True
piirra_ylennetty = False
piirra_alennettu = False
piirra_palautus = False
nuotti_x = 0
nuotti_y = 0
nuotti_midi = 0
midi_diskantti_alaraja = 57
midi_basso_ylaraja = 65
diskantti = True

# Rajaviivan sijainti
rajaviiva_x = 150
rajaviiva_y = 0
rajaviiva_pituus_y = 450
rajaviiva_paksuus = 4

# Arvausalue
arvausalue_x = rajaviiva_x + rajaviiva_paksuus
arvausalue_y = rajaviiva_y
arvausalue_leveys = 350
arvausalue_korkeus = rajaviiva_pituus_y - rajaviiva_y

# Pisteet
pisteet = 0

# Sävellaji
savellaji = "C"
savellajin_vaatima_tila_x = piirto.Piirra_Savellaji(naytto, 150, savellaji, paikat_diskantti, True, True)

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
                        if nuotti_x <= arvausalue_x + arvausalue_leveys + savellajin_vaatima_tila_x:
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
                            if nuotti_x <= arvausalue_x + arvausalue_leveys + savellajin_vaatima_tila_x:
                                luo_nuotti = True
                                pisteet += 1
                        break

    # Nuotin luominen ja liikutus
    if luo_nuotti:
        kosketin_vari = "v"
        piirra_ylennetty = False
        piirra_alennettu = False
        piirra_palautus = False

        if random.randrange(0,2) == 0:       # Arvotaan nuotin sävel diskantti- tai bassoviivastolta. (0 = diskantti, 1 = basso)
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

        savellaji_vaikutus = apufunktiot.Tarkista_Savellaji_Vaikutus(savellaji, nuotti_midi)

        # Lisätään sävellajin vaikutus nuotteihin. Tarkistetaan myös että sävel ei mene asetettujen midi arvo rajojen yli
        if savellaji_vaikutus == "y":
            if diskantti and nuotti_midi + 1 <= loppu_midi:
                nuotti_midi += 1
            elif not diskantti and nuotti_midi + 1 <= midi_basso_ylaraja:
                nuotti_midi += 1
            else:
                piirra_palautus = True
        elif savellaji_vaikutus == "a":
            if diskantti and nuotti_midi - 1 >= midi_diskantti_alaraja:
                nuotti_midi -= 1
            elif not diskantti and nuotti_midi - 1 >= alku_midi:
                nuotti_midi -= 1
            else:
                piirra_palautus = True

        if piirra_palautus == False:
            muutos = random.randrange(0, 3)      # Arvotaan ylennetäänkö, alennetaanko vai pidetäänkö nuotti normaalina. (0 = normaali, 1 = ylennetty, 2 = alennettu)
            if muutos == 1:
                if diskantti and nuotti_midi + 1 <= loppu_midi:
                    nuotti_midi += 1
                    if savellaji_vaikutus == "a":
                        piirra_palautus = True
                    else:
                        piirra_ylennetty = True
                elif not diskantti and nuotti_midi + 1 <= midi_basso_ylaraja:
                    nuotti_midi += 1
                    if savellaji_vaikutus == "a":
                        piirra_palautus = True
                    else:
                        piirra_ylennetty = True
            elif muutos == 2:
                if diskantti and nuotti_midi - 1 >= midi_diskantti_alaraja:
                    nuotti_midi -= 1
                    if savellaji_vaikutus == "y":
                        piirra_palautus = True
                    else:
                        piirra_alennettu = True
                elif not diskantti and nuotti_midi - 1 >= alku_midi:
                    nuotti_midi -= 1
                    if savellaji_vaikutus == "y":
                        piirra_palautus = True
                    else:
                        piirra_alennettu = True

        # nuotin luontietäisyyys x-akselilla
        nuotti_x = 150 + savellajin_vaatima_tila_x + arvausalue_leveys + 100
        luo_nuotti = False

    else:
        if nuotti_x > rajaviiva_x + savellajin_vaatima_tila_x:
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

    for kosketin in koskettimet_valkoinen:  # Piirretään valkoiset koskettimet ensin. Jos hiiri havaitaan koskettimen päällä, koskettimen väritystä muutetaan 
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

    savellajin_vaatima_tila_x = piirto.Piirra_Savellaji(naytto, 150, savellaji, paikat_diskantti, True, True)

    # Rajaviivan piirto
    pygame.draw.line(naytto, (222,40,20), (rajaviiva_x + savellajin_vaatima_tila_x, rajaviiva_y), (rajaviiva_x + savellajin_vaatima_tila_x ,rajaviiva_pituus_y), rajaviiva_paksuus)
    
    # Arvausalue piirto
    pygame.draw.rect(naytto, (6,148,3), [arvausalue_x + savellajin_vaatima_tila_x, arvausalue_y, arvausalue_leveys, arvausalue_korkeus])
    
    # Viivaston piirto
    piirto.Piirra_Viivasto(naytto, 0, diskantti_keski_c_y, viivasto_rivivali, True)
    piirto.Piirra_Viivasto(naytto, 0, basso_keski_c_y, viivasto_rivivali, False)

    # G-Nuottiavain piirto
    piirto.Piirra_G_Avain(naytto, 50, viivasto_paikat["diskantti"][1])

    # F-Nuottiavain piirto
    piirto.Piirra_F_Avain(naytto, 50, viivasto_paikat["basso"][1])

    # Sävellajin merkkien piirto
    piirto.Piirra_Savellaji(naytto,150, savellaji, paikat_diskantti, True)
    piirto.Piirra_Savellaji(naytto,150, savellaji, paikat_basso, False)

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
    if piirra_ylennetty:
        piirto.Piirra_Ylennys(naytto, nuotti_x, nuotti_y, -20)
    if piirra_alennettu:
        piirto.Piirra_Alennus(naytto, nuotti_x, nuotti_y, -20)
    if piirra_palautus:
        piirto.Piirra_Palautus(naytto, nuotti_x, nuotti_y, -20)

    # Nuotti piirto
    piirto.Piirra_4_Osa_Nuotti(naytto, nuotti_x, nuotti_y)

    # Pisteiden piirto
    pisteet_teksti = fontti.render(f"Pisteet: {pisteet}", True, "white")
    naytto.blit(pisteet_teksti, (0, naytto.get_height() - kosk_korkeus - pisteet_teksti.get_height()))

    pygame.display.flip()

    kello.tick(60)

