import pygame
import pygame.midi
from pygame.locals import *
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
naytto = pygame.display.set_mode((1000, 800), RESIZABLE)

# Tekstit ja fontit
fontti = pygame.font.SysFont("Georgia", 48, bold=True)
fontti_2 = pygame.font.SysFont("Georgia", 18, bold=True)
pisteet_teksti = fontti.render("Pisteet: 0", True, "white")
edellinen_oikea_vastaus = fontti.render("", True, "white")
nykyinen_vastaus_teksti = ""
taso_teksti = fontti.render("Taso: 1 (0 / 10)", True, "white")
virheet_teksti = fontti.render("Virheet: 0 / 5", True, "white")

# Kello
kello = pygame.time.Clock()
oikea_vastaus_ajastin = 0

# Viivasto
diskantti_keski_c_y = naytto.get_height() / 2 - 30
basso_keski_c_y = naytto.get_height() / 2 + 30
viivasto_rivivali = 20
viivaston_leveys = 700
viivasto_paikat = {"diskantti": piirto.Piirra_Viivasto(naytto, naytto.get_width() / 2, diskantti_keski_c_y, viivasto_rivivali, viivaston_leveys, True), "basso": piirto.Piirra_Viivasto(naytto, naytto.get_width() / 2, basso_keski_c_y, viivasto_rivivali, viivaston_leveys, False)}

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
rajaviiva_x = naytto.get_width() / 2 - viivaston_leveys / 2 + 150
rajaviiva_y = naytto.get_height() / 2
rajaviiva_pituus_y = 400
rajaviiva_paksuus = 4

# Arvausalue
arvausalue_x = rajaviiva_x + rajaviiva_paksuus
arvausalue_y = rajaviiva_y
arvausalue_leveys = 350
arvausalue_korkeus = rajaviiva_pituus_y

# Pisteet
pisteet = 0
taso = 1
virhe_maara = 0
oikein_maara = 0

# Sävellaji
savellaji = "C"
savellajin_vaatima_tila_x = piirto.Piirra_Savellaji(naytto, 150, savellaji, paikat_diskantti, True, True)

# Pelisilmukka
while True:
    naytto.fill((0,0,0))
    
    for tapahtuma in pygame.event.get():
        if tapahtuma.type == pygame.QUIT:   # Ikkunan yläkulman X painike
            exit()

        if tapahtuma.type == pygame.VIDEORESIZE:    # Ikkunan koon muutos
            
            # Ruudun minimikoko
            if pygame.display.get_window_size()[0] < 750:
               naytto = pygame.display.set_mode((750, pygame.display.get_window_size()[1]), RESIZABLE)
            if pygame.display.get_window_size()[1] < 700:
               naytto = pygame.display.set_mode((pygame.display.get_window_size()[0], 700), RESIZABLE)
            # Nuotin ero rajaviivaan x-akselilla ennen ikkunan koon muutosta
            nuotti_x_ero = nuotti_x - rajaviiva_x   

            # Tärkeiden elementtien x- ja y-koordinaattien päivitys
            diskantti_keski_c_y = naytto.get_height() / 2 - 30
            basso_keski_c_y = naytto.get_height() / 2 + 30
            viivasto_paikat = {"diskantti": piirto.Piirra_Viivasto(naytto, naytto.get_width() / 2, diskantti_keski_c_y, viivasto_rivivali, viivaston_leveys, True), "basso": piirto.Piirra_Viivasto(naytto, naytto.get_width() / 2, basso_keski_c_y, viivasto_rivivali, viivaston_leveys, False)}
            paikat_diskantti = apufunktiot.Luo_Nuottien_Paikat(viivasto_paikat["diskantti"][0] + viivasto_rivivali, 10)
            paikat_basso = apufunktiot.Luo_Nuottien_Paikat(viivasto_paikat["basso"][0] - viivasto_rivivali, 10)
            rajaviiva_x = naytto.get_width() / 2 - viivaston_leveys / 2 + 150
            rajaviiva_y = naytto.get_height() / 2
            arvausalue_x = rajaviiva_x + rajaviiva_paksuus
            arvausalue_y = rajaviiva_y

            # Nuotin uudet koordinaatit 
            nuotti_x = rajaviiva_x + nuotti_x_ero
            if diskantti:
                nuotti_y = paikat_diskantti[nuotti_midi][0]
            else:
                nuotti_y = paikat_basso[nuotti_midi][0]
            
            # Koskettimien uudet koordinaatit
            koskettimet_valkoinen, koskettimet_musta = koskettimet.Luo_Koskettimet(naytto, alku_midi, loppu_midi, kosk_korkeus)

        if tapahtuma.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[0] == True:    # Hiiren vasen painike alhaalla

            musta_klikattu = False
            for kosketin in koskettimet_musta:
                if kosketin[0].collidepoint(tapahtuma.pos):
                    musta_klikattu = True
                    soitin.note_off(kosketin[1], 127, 1)
                    soitin.note_on(kosketin[1], 127, 1)

                    # Painetun koskettimen vertaaminen haettavaan nuottiin
                    if kosketin[1] == nuotti_midi:
                        if nuotti_x <= arvausalue_x + arvausalue_leveys + savellajin_vaatima_tila_x:
                            luo_nuotti = True
                            pisteet += 5 * taso
                            oikein_maara += 1
                            edellinen_oikea_vastaus = fontti.render(nykyinen_vastaus_teksti, True, "green")
                            oikea_vastaus_ajastin = 200
                    else:
                        if nuotti_x <= arvausalue_x + arvausalue_leveys + savellajin_vaatima_tila_x:
                            pisteet -= 5 * taso
                            oikein_maara -= 1
                            virhe_maara += 1
                    break

            if musta_klikattu == False:
                for kosketin in koskettimet_valkoinen:
                    if kosketin[0].collidepoint(tapahtuma.pos):
                        soitin.note_off(kosketin[1], 127, 1)
                        soitin.note_on(kosketin[1], 127, 1)

                        # Painetun koskettimen vertaaminen haettavaan nuottiin
                        if kosketin[1] == nuotti_midi:
                            if nuotti_x <= arvausalue_x + arvausalue_leveys + savellajin_vaatima_tila_x:
                                luo_nuotti = True
                                pisteet += 5 * taso
                                oikein_maara += 1
                                edellinen_oikea_vastaus = fontti.render(nykyinen_vastaus_teksti, True, "green")
                                oikea_vastaus_ajastin = 200
                        else:
                            if nuotti_x <= arvausalue_x + arvausalue_leveys + savellajin_vaatima_tila_x:
                                pisteet -= 5 * taso
                                oikein_maara -= 1
                                virhe_maara += 1
                        break

    # Nuotin luominen ja liikutus
    if luo_nuotti:
        piirra_ylennetty = False
        piirra_alennettu = False
        piirra_palautus = False
        savellaji = "C"

        # Tason muokkaamat muutujat
        taso_vain_diskantti = False
        taso_vain_basso = False
        taso_vain_ylennykset = False
        taso_vain_alennukset = False
        taso_ylen_ja_alen = False
        taso_diskantti_alaraja = midi_diskantti_alaraja
        taso_diskantti_ylaraja = loppu_midi
        taso_basso_alaraja = alku_midi
        taso_basso_ylaraja = midi_basso_ylaraja
        taso_savellajit = [("Cb","ab"), ("Db","eb"), ("Db","b"), ("Ab","f"), ("Eb","c"), ("B","g"), ("F","d"), 
                           ("C","a"), 
                           ("G","e"), ("D","h"), ("A","f#"), ("E","c#"), ("H","g#"), ("F#","d#"), ("C#","a#")]
        if oikein_maara >= 10:
            taso += 1
            virhe_maara = 0
            oikein_maara = 0

        # Tasokohtaiset muutokset
        if taso == 1:
            taso_vain_diskantti = True
            taso_diskantti_alaraja = 60
            taso_diskantti_ylaraja = 72
        elif taso == 2:
            taso_vain_diskantti = True
        elif taso == 3:
            taso_vain_basso = True
            taso_basso_alaraja = 48
            taso_basso_ylaraja = 60
        elif taso == 4:
            taso_vain_basso = True
        elif taso == 5:
            taso_vain_ylennykset = True
        elif taso == 6:
            taso_vain_alennukset = True
        elif taso == 7:
            taso_ylen_ja_alen = True
        elif taso == 8:
            if random.choice([True, False]):
                savellaji = taso_savellajit[len(taso_savellajit) // 2 - 1][random.randrange(0,2)]
            else:
                savellaji = taso_savellajit[len(taso_savellajit) // 2 + 1][random.randrange(0,2)]
        elif taso == 9:
            if random.choice([True, False]):
                savellaji = taso_savellajit[len(taso_savellajit) // 2 - 2][random.randrange(0,2)]
            else:
                savellaji = taso_savellajit[len(taso_savellajit) // 2 + 2][random.randrange(0,2)]
        elif taso == 10:
            if random.choice([True, False]):
                savellaji = taso_savellajit[len(taso_savellajit) // 2 - 3][random.randrange(0,2)]
            else:
                savellaji = taso_savellajit[len(taso_savellajit) // 2 + 3][random.randrange(0,2)]
        elif taso == 11:
            if random.choice([True, False]):
                savellaji = taso_savellajit[len(taso_savellajit) // 2 - 4][random.randrange(0,2)]
            else:
                savellaji = taso_savellajit[len(taso_savellajit) // 2 + 4][random.randrange(0,2)]
        elif taso == 12:
            if random.choice([True, False]):
                savellaji = taso_savellajit[len(taso_savellajit) // 2 - 5][random.randrange(0,2)]
            else:
                savellaji = taso_savellajit[len(taso_savellajit) // 2 + 5][random.randrange(0,2)]
        elif taso == 13:
            if random.choice([True, False]):
                savellaji = taso_savellajit[len(taso_savellajit) // 2 - 6][random.randrange(0,2)]
            else:
                savellaji = taso_savellajit[len(taso_savellajit) // 2 + 6][random.randrange(0,2)]
        elif taso == 14:
            if random.choice([True, False]):
                savellaji = taso_savellajit[len(taso_savellajit) // 2 - 7][random.randrange(0,2)]
            else:
                savellaji = taso_savellajit[len(taso_savellajit) // 2 + 7][random.randrange(0,2)]
        else:
            if random.choice([True, False]):
                savellaji = taso_savellajit[len(taso_savellajit) // 2 - random.randrange(0,8)][random.randrange(0,2)]
            else:
                savellaji = taso_savellajit[len(taso_savellajit) // 2 + random.randrange(0,8)][random.randrange(0,2)]
            taso_ylen_ja_alen = True
        
        # Arvotaan nuotin sävel diskantti- tai bassoviivastolta. (0 = diskantti, 1 = basso)
        if taso_vain_diskantti:
            diskantti_vai_basso = 0
        elif taso_vain_basso:
            diskantti_vai_basso = 1
        else:
            diskantti_vai_basso = random.randrange(0,2)

        if diskantti_vai_basso == 0:
            nuotti_midi = random.randrange(taso_diskantti_alaraja, taso_diskantti_ylaraja)
            kosketin_vari = paikat_diskantti[nuotti_midi][1]
            if kosketin_vari == "m":
                nuotti_midi -= 1
            nuotti_y = paikat_diskantti[nuotti_midi][0]
            diskantti = True
        else:
            nuotti_midi = random.randrange(taso_basso_alaraja, taso_basso_ylaraja)
            kosketin_vari = paikat_basso[nuotti_midi][1]
            if kosketin_vari == "m":
                nuotti_midi -= 1
            nuotti_y = paikat_basso[nuotti_midi][0]
            diskantti = False
        
        savel_tekstina = apufunktiot.Savel_Tekstina(nuotti_midi)

        #Lisätään sävellajin vaikutus nuotteihin. Tarkistetaan myös että sävel ei mene asetettujen midi arvo rajojen yli
        savellaji_vaikutus = apufunktiot.Tarkista_Savellaji_Vaikutus(savellaji, nuotti_midi)
        
        if savellaji_vaikutus == "y":
            if diskantti and nuotti_midi + 1 <= taso_diskantti_ylaraja:
                nuotti_midi += 1
                savel_tekstina = apufunktiot.Savel_Tekstina(nuotti_midi,"y")
            elif not diskantti and nuotti_midi + 1 <= taso_basso_ylaraja:
                nuotti_midi += 1
                savel_tekstina = apufunktiot.Savel_Tekstina(nuotti_midi,"y")
            else:
                piirra_palautus = True
                savel_tekstina = apufunktiot.Savel_Tekstina(nuotti_midi)
        elif savellaji_vaikutus == "a":
            if diskantti and nuotti_midi - 1 >= taso_diskantti_alaraja:
                nuotti_midi -= 1
                savel_tekstina = apufunktiot.Savel_Tekstina(nuotti_midi,"a")
            elif not diskantti and nuotti_midi - 1 >= taso_basso_alaraja:
                nuotti_midi -= 1
                savel_tekstina = apufunktiot.Savel_Tekstina(nuotti_midi,"a")
            else:
                piirra_palautus = True
                savel_tekstina = apufunktiot.Savel_Tekstina(nuotti_midi)

        # Nuotin ylennys tai alennus
        if piirra_palautus == False:

             # Arvotaan ylennetäänkö, alennetaanko vai pidetäänkö nuotti normaalina. (0 = normaali, 1 = ylennetty, 2 = alennettu)
            if taso_vain_ylennykset:
                if random.choice([True, False]):
                    muutos = 1
            elif taso_vain_alennukset:
                if random.choice([True, False]):
                    muutos = 2
            elif taso_ylen_ja_alen:
                muutos = random.randrange(0, 3)     
            else:
                muutos = 0

            if muutos == 1:
                if diskantti and nuotti_midi + 1 <= taso_diskantti_ylaraja:
                    nuotti_midi += 1
                    if savellaji_vaikutus == "a":
                        piirra_palautus = True
                        savel_tekstina = apufunktiot.Savel_Tekstina(nuotti_midi)
                    else:
                        piirra_ylennetty = True
                        savel_tekstina = apufunktiot.Savel_Tekstina(nuotti_midi,"y")
                elif not diskantti and nuotti_midi + 1 <= taso_basso_ylaraja:
                    nuotti_midi += 1
                    if savellaji_vaikutus == "a":
                        piirra_palautus = True
                        savel_tekstina = apufunktiot.Savel_Tekstina(nuotti_midi)
                    else:
                        piirra_ylennetty = True
                        savel_tekstina = apufunktiot.Savel_Tekstina(nuotti_midi,"y")
            elif muutos == 2:
                if diskantti and nuotti_midi - 1 >= taso_diskantti_alaraja:
                    nuotti_midi -= 1
                    if savellaji_vaikutus == "y":
                        piirra_palautus = True
                        savel_tekstina = apufunktiot.Savel_Tekstina(nuotti_midi)
                    else:
                        piirra_alennettu = True
                        savel_tekstina = apufunktiot.Savel_Tekstina(nuotti_midi,"a")
                elif not diskantti and nuotti_midi - 1 >= taso_basso_alaraja:
                    nuotti_midi -= 1
                    if savellaji_vaikutus == "y":
                        piirra_palautus = True
                        savel_tekstina = apufunktiot.Savel_Tekstina(nuotti_midi)
                    else:
                        piirra_alennettu = True
                        savel_tekstina = apufunktiot.Savel_Tekstina(nuotti_midi,"a")
        
        # nuotin luontietäisyyys x-akselilla
        nuotti_x = arvausalue_x + arvausalue_leveys + savellajin_vaatima_tila_x + 100
        luo_nuotti = False

        # oikea vastaussävel tekstimuodossa talteen
        nykyinen_vastaus_teksti = savel_tekstina[0] + " " + str(savel_tekstina[1])

    else:
        if nuotti_x > rajaviiva_x + savellajin_vaatima_tila_x:
            nuotti_x -= 1
        else:
            luo_nuotti = True
            soitin.note_off(60, 127,5)
            soitin.note_on(60, 127,5)
            pisteet -= 10 * taso
            edellinen_oikea_vastaus = fontti.render(nykyinen_vastaus_teksti, True, "red")
            oikea_vastaus_ajastin = 200
            virhe_maara += 1
            oikein_maara -= 1

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
        if kosketin[1] == 60:   # Piirretään keski-C kirjain
            teksti = fontti_2.render("C", True, "black")
            naytto.blit(teksti, (kosketin[0].x + kosketin[0].width / 2 - teksti.get_width() / 2, kosketin[0].y + kosketin[0].height / 2 + 20))

    for kosketin in koskettimet_musta:  # Piirretään mustat koskettimet. Jos hiiri havaitaan koskettimen päällä, koskettimen väritystä muutetaan
        if kosketin[0].x <= hiiri_x <= kosketin[0].x + kosketin[0].width and kosketin[0].y <= hiiri_y <= kosketin[0].y + kosketin[0].height:
            pygame.draw.rect(naytto,(140,140,140),kosketin[0])
        else:
            pygame.draw.rect(naytto,(50,50,50),kosketin[0])

    savellajin_vaatima_tila_x = piirto.Piirra_Savellaji(naytto, 150, savellaji, paikat_diskantti, True, True)

    # Rajaviivan piirto
    pygame.draw.line(naytto, (222,40,20), (rajaviiva_x + savellajin_vaatima_tila_x, rajaviiva_y - rajaviiva_pituus_y / 2), (rajaviiva_x + savellajin_vaatima_tila_x ,rajaviiva_y + rajaviiva_pituus_y / 2), rajaviiva_paksuus)
    
    # Arvausalue piirto
    pygame.draw.rect(naytto, (6,148,3), [arvausalue_x + savellajin_vaatima_tila_x, arvausalue_y - arvausalue_korkeus / 2, arvausalue_leveys, arvausalue_korkeus])
    
    # Viivaston piirto
    piirto.Piirra_Viivasto(naytto, naytto.get_width() / 2, diskantti_keski_c_y, viivasto_rivivali, viivaston_leveys + savellajin_vaatima_tila_x, True)
    piirto.Piirra_Viivasto(naytto, naytto.get_width() / 2, basso_keski_c_y, viivasto_rivivali, viivaston_leveys + savellajin_vaatima_tila_x, False)

    # G-Nuottiavain piirto
    piirto.Piirra_G_Avain(naytto, naytto.get_width() / 2 - (viivaston_leveys + savellajin_vaatima_tila_x) / 2 + 50, viivasto_paikat["diskantti"][1])

    # F-Nuottiavain piirto
    piirto.Piirra_F_Avain(naytto, naytto.get_width() / 2 - (viivaston_leveys + savellajin_vaatima_tila_x) / 2 + 50, viivasto_paikat["basso"][1])

    # Sävellajin merkkien piirto
    piirto.Piirra_Savellaji(naytto, naytto.get_width() / 2 - (viivaston_leveys + savellajin_vaatima_tila_x) / 2 + 150, savellaji, paikat_diskantti, True)
    piirto.Piirra_Savellaji(naytto, naytto.get_width() / 2 - (viivaston_leveys + savellajin_vaatima_tila_x) / 2 + 150, savellaji, paikat_basso, False)

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
    if pisteet < 0:
        pisteet = 0
    pisteet_teksti = fontti.render(f"Pisteet: {pisteet}", True, "white")
    naytto.blit(pisteet_teksti, (0, naytto.get_height() - kosk_korkeus - pisteet_teksti.get_height()))

    # Oikean vastauksen piirto
    if oikea_vastaus_ajastin > 0:
        naytto.blit(edellinen_oikea_vastaus, (naytto.get_width() - edellinen_oikea_vastaus.get_width(), naytto.get_height() - kosk_korkeus - pisteet_teksti.get_height()))
    
    # Virhelaskurin ja oikein laskurin hallintaa
    if virhe_maara >= 5:
        luo_nuotti = True
        virhe_maara = 0
        oikein_maara = 0
        taso -= 1
        if taso <= 0:
            taso = 1
    if oikein_maara < 0:
        oikein_maara = 0

    # Taso tekstin piirto
    taso_teksti = fontti.render(f"Taso: {taso} ({oikein_maara}/10)", True, "white")
    naytto.blit(taso_teksti, (0, 0))

    # Virheet tekstin piirto
    virheet_teksti = fontti.render(f"Virheet: {virhe_maara} / 5", True, "white")
    naytto.blit(virheet_teksti, (naytto.get_width() - virheet_teksti.get_width(), 0))

    #piirto.Piirra_Tahtiviiva(naytto, naytto.get_width() / 2 - (viivaston_leveys + savellajin_vaatima_tila_x) / 2, naytto.get_height() / 2, 10 * viivasto_rivivali + 60)
    piirto.Piirra_Akkoladi(naytto, naytto.get_width() / 2 - (viivaston_leveys + savellajin_vaatima_tila_x) / 2, naytto.get_height() / 2, 10 * viivasto_rivivali + 60)
    piirto.Piirra_Paatosviiva(naytto, naytto.get_width() / 2 + (viivaston_leveys + savellajin_vaatima_tila_x) / 2, naytto.get_height() / 2, 10 * viivasto_rivivali + 60)

    pygame.display.flip()

    # Kellon ja ajastimien edistäminen.
    kello.tick(60)
    if oikea_vastaus_ajastin > 0:
        oikea_vastaus_ajastin -= 1

    
