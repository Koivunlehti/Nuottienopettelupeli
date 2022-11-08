# Nuottienopettelupeli
 Pygame harjoitusprojekti

1. Luo Python virtuaaliympäristö:

    py -m venv venv     Luo ympäristön uusimmalla asennetulla Python versiolla

    tai
    
    py -3.9 venv venv   Jos asennettuna on useita Python versioita ja haluat käyttää tiettyä vanhempaa versiota niistä.

2. Virtuaaliympäristön käyttö:
    
    2.1 Aktivoi virtuaaliympäristö:

        venv\scripts\activate.ps1

        tai

        venv\scripts\activate.bat
    
    2.2 Deaktivoi virtuaaliympäristö:

        deactivate

3. Kirjastojen Asennus:     (Varmista että mahdollinen virtuaaliympäristö on aktiivinen)

    3.1 Asenna tarvittavat kirjastot:

        pip install pygame    (pygame = kirjaston nimi)

    3.2 Asenna requirements -tiedoston luettelemat kirjastot:

        pip install -r requirements.txt

4. Requirements tiedoston luonti:

    pip freeze > requirements.txt
    