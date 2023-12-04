# Nuottienopettelupeli
Pygame harjoitusprojekti, jonka aiheena on musiikin teoriaan liittyviä erilaisia harjoituksia pienten minipelien muodossa.

Pelissä on tällä hetkellä 2 minipeliä: 
- Nuottiarvaus
- Kuule sävel

Peli alkaa alkuvalikosta, jonka kautta eri minipelit on tarkoitus avata.

Pääset takaisin alkuvalikkoon minipelistä ESC-näppäimellä

## Nuottiarvaus
Tämän minipelin ideana on lukea viivastoa ja nuotin ilmaisemaa sävelkorkeutta.
Pelaajan pitää painaa vastaukseksi oikeaa kosketinta. Peli vaikeutuu tason noustessa. Taso nousee jokaisen 20 oikean vastauksen jälkeen.

## Kuule sävel
Tämän minipelin ideana on tunnistaa sävelen korkeus kuulemalla. Peli vaikeutuu tason noustessa. Tarvitset 20 oikeaa vastausta noustaksesi seuraavalle tasolle.

## Projektin käynnistäminen
Projektin voi käynnistää seuraavasti:
1. Tarkista että Python 3.11 on asennettu.
2. Luo virtuaaliympäristö: `py -m venv venv` tai `py -3.11 venv venv`, jos asennettuna on myös muita Python versioita.
3. Aktivoi virtuaaliympäristö `venv\scripts\activate.ps1` tai `venv\scripts\activate.bat`.
4. Asenna kirjastot: `pip install -r requirements.txt`
5. Käynnistä peli: `py alkuvalikko.py`

## Huomioita

- Pelin toiminta vaatii, että järjestelmään on määritetty oletus MIDI-soitin.  
Ainakin Windows 10:ssä tämän pitäisi olla valmiina.

# Muistilista 
## Projektin hallinta
Projektissa on käytetty Python 3.11 versiota

1. Luo Python virtuaaliympäristö:

    1.1 Luominen uusimmalla asennetulla Python versiolla:

        py -m venv venv
    
    1.2 Luominen tietyllä Python versiolla, jos asennettuna on useita:
            
        py -3.11 venv venv

2. Virtuaaliympäristön käyttö:
    
    2.1 Aktivoi virtuaaliympäristö:

        venv\scripts\activate.ps1

        tai

        venv\scripts\activate.bat
    
    2.2 Deaktivoi virtuaaliympäristö:

        deactivate

3. Kirjastojen Asennus (HUOM! Varmista ensin, että mahdollinen virtuaaliympäristö on aktiivinen):     

    3.1 Asenna tarvittavat kirjastot:

        pip install pygame    (pygame = kirjaston nimi)

    3.2 Asenna "requirements" -tiedoston luettelemat kirjastot:

        pip install -r requirements.txt

4. Projektin "requirements" tiedoston luonti:

        pip freeze > requirements.txt

## Testien ajaminen

Suorita kaikki testit: 

`python -m unittest`

Suorita yksi tests kansion tiedostoista: 

`python -m unittest testit\tiedostonimi.py`

Suorita yksi vain yksi testi luokka tiedostosta: 

`python -m unittest testit.tiedostonimi.Testi_Luokka_Nimi`

Suorita yksi vain yksi testi case tiedostosta: 

`python -m unittest testit.tiedostonimi.Testi_Luokka_Nimi.testi_case_nimi`

Lisätietoa testeistä -v lipulla: 

`python -m unittest -v`