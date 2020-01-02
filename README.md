**Project Fasten Your Seatbelts**
======

Welkom op de Gitlab pagina van ons Fasten Your Seatbelts project. Hieronder vindt u informatie over het project.

### Algemene informatie over het project:
---
**Opdrachtgever:** Corendon
**Klas:** IT102
**Team:** 5

**Teamleden:**
*    Raoul Ursum - teamleider
*    Jeffrey van Velzen - waarschuwer
*    Milo Broerse - afmaker
*    Jazzley Louisville - groepswerker
*    Stefan de Kraker - bedenker

### Intalleer de volgende libraries:
---
*    De volgende library zijn er nodig: 
*    RPi.GPIO
*    rpi_ws281x
*    smbus
*    math
*    sqlite3
*    SimpleMFRC522

*   Daarnaast moet NodeJS en ember worden geïnstalleerd  

### Zo run je de code:
---
*    Clone eerst de repository op de Raspberry Pi
*    Ga naar de repository toe via de command line
*    Voer hier dit commando uit: >> sudo python3 initDB.py
*    Navigeer naar de map /fys_project_team5/balldart-frontend en voer het volgende commando uit: >> sudo npm install
*    Vervolgens: >> sudo ember s
*    In dezelfde map kan server.py gevonden worden. Run deze: >> sudo python3 server.py
*    Spring één map terug en voer het volgende uit: >> sudo python3 main.py
*    Alles is nu up and running. De website kan gevonden op het ip adres van de pi, voorbeeld: 192.168.2.46:5000
