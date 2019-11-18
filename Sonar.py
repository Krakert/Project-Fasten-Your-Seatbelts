import RPi.GPIO as GPIO                             # Maak gebruik van de RPI.GPIO bibliotheek
import time                                         # En de Time bibliotheek
 
GPIO.setmode(GPIO.BCM)                              # Maak gebruik van de layout van de Broadcom SOC
 
GPIO_TRIGGER = 13                                   # Geef posities van de pinnen op
GPIO_ECHO = 26
MAX_MESURE_DISTANCE = 400                           # Voor langer dan 400 cm is de sonar niet geschikt
 
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)                  # De trigger is een output, geeft een pulse
GPIO.setup(GPIO_ECHO, GPIO.IN)                      # En de echo zal deze ontvangen, dus input
 
def distance():                                     # De fucntie die de afstand terug geeft
    GPIO.output(GPIO_TRIGGER, True)                 # Stuur een pulse van 0.01 ms lang
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    while GPIO.input(GPIO_ECHO) == 0:               # Als er nog een singaal is bij de Echo zet de start tijd op nu
        StartTime = time.time()
 
    while GPIO.input(GPIO_ECHO) == 1:               # En als het singaal binnen komt stopt de Start tijd en de stoptijd
        StopTime = time.time()                      # word ook opgeslagen
 
    TimeElapsed = StopTime - StartTime              # haal die twee van elkaar af
    distance = (TimeElapsed * 34300) / 2            # De afstand kan als volgt worden berekend, de 34300 is het aantal M/S
                                                    # dat sonar aflegt, en natuurlijk delen door 2, anders hebben we de totale afstand
    if distance > MAX_MESURE_DISTANCE:              # Is dit buiten de 400 cm, dan hebben we een kleine fout, 
        distance = 0                                #en geven we 0 terug
 
    return distance                                 # Geef de data aan de rest van het programma
 
