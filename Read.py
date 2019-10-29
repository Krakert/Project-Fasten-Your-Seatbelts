# RFID scanner voor het inlezen van een RFID TAG
# Gebruik gemaakt van een Velleman405

import RPi.GPIO as GPIO
import MFRC522
import signal

continue_reading = True


# Vang (capture) de SIGINT voor opschoning wannee de script afgebroken is
def end_read(signal, frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()


# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Creeerd een object van de class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welkom bericht, wanneer het programma is opgestart
print "Welcome to the MFRC522(VelleMan405) data read "
print "Press Ctrl-C to stop."

# Deze code checked als er een RFID tag in de buurt zit. als het in de buurt is krijgt het de UID and authenticatie
while continue_reading:

    # Scanned naar tags(cards)
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # wordt uitgevoerd als er een tag(card) in de buurt is
    if status == MIFAREReader.MI_OK:
        print "Card detected"

    # krijgt de  UID vanuit card(krijgt de informatie uit de tag(card))
    (status, uid) = MIFAREReader.MFRC522_Anticoll()

    # als we de  UID hebben dan , continued hij
    if status == MIFAREReader.MI_OK:

        # Print UID
        print "Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3])

        # default key voor voor authenticatie
        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

        # Selecteerd de gescande tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticatie
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # Check als het al authenticated is
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()
        else:
            print "Authentication error"
