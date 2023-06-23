# Nuottienopettelupeli
Pygame harjoitusprojekti, jonka aiheena on musiikin teoriaan liittyviä erilaisia harjoituksia pienten minipelien muodossa.
<br>
Peli alkaa alkuvalikosta, jonka kautta eri minipelit on tarkoitus avata.

## Projektin hallintaa
1. Luo Python virtuaaliympäristö:

    1.1 Luominen uusimmalla asennetulla Python versiolla:

        py -m venv venv
    
    1.2 Luominen tietyllä Python versiolla, jos asennettuna on useita:
            
        py -3.9 venv venv

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