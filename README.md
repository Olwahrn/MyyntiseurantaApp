# Myyntiseuranta

Käyttäjä voi luoda tunnuksen ja kirjautua sisään.
Käyttäjä voi lisätä, muokata ja poistaa omia työvuorojaan.
Jokaiselle työvuorolle voi valita yhden tai useamman luokituksen (esim. vuorotyyppi).
Käyttäjä voi lisätä muistiinpanoja omiin työvuoroihinsa.
Käyttäjä voi selata ja hakea työvuoroja hakusanan perusteella.
Käyttäjäsivu näyttää:
Käyttäjän omat vuorot
Tilastoja (vuorojen määrä ja kokonaistunnit)

Käyttöohjeet:

Jos flask puuttuu, komentorivillä: pip install flask

Tiedostossa schema.sql on taulujen määrrittelyt. 
SQLite3 käyttämällä saat tietokannan toimintaan komentorivillä repositoriossa: 
sqlite3 database.db < schema.sql

Käynnistä appi Flaskilla komentorivillä:

python3 -m venv venv
source venv/bin/activate
flask run

Avaa selaimessa osoite http://127.0.0.1:5000
