#importeert machine en tijd library
from machine import Pin, PWM
from time import sleep
import random
#Eindschakelaars worden gedefinieerd
limit1= Pin(15,Pin.IN, Pin.PULL_DOWN)  # Eindschakelaar voor calibratie
limit2 = Pin(16,Pin.IN, Pin.PULL_DOWN) #eindschakelaar y-as laag
limit3 = Pin(17,Pin.IN, Pin.PULL_DOWN) #eindschakelaar y-as hoog
limit4 = Pin(18,Pin.IN, Pin.PULL_DOWN) #eindschakelaar piston in
limit5 = Pin(19,Pin.IN, Pin.PULL_DOWN) #eindschakelaar piston uit
#knoppen definiëren
knop1 = Pin(10,Pin.IN)
knop2 = Pin(11,Pin.IN)
knop3 = Pin(12,Pin.IN)
knop4 = Pin(13,Pin.IN)
knop5 = Pin(14,Pin.IN)
#piston definiëren
piston = Pin(21, Pin.OUT)
#infrarood sensor wordt gedefinieerd
ir_sensor = Pin(20, Pin.IN, Pin.PULL_DOWN)
#pwm pin
motorcont_pwm = PWM(Pin(1))
motorcont_pwm.freq(1000)  # 1 kHz, pas aan indien nodig
motorcont_pwm.duty_u16(int(65535 * 0.8))  # 20% duty cycle
#motorfuncties
#motor x-as rechtsom draaien
def motorx_hoog():
     pin_1 = Pin(2,Pin.OUT)
     pin_1.value(1)
     pin_2 = Pin(3,Pin.OUT)
     pin_2.value(0)

#motor x-as linksom draaien
def motorx_laag():
     pin_3 = Pin(2,Pin.OUT)
     pin_3.value(0)
     pin_4 = Pin(3,Pin.OUT)
     pin_4.value(1)
     
#motor x-as uitzetten 
def motorx_uit():
     pin = Pin(2,Pin.OUT)
     pin.value(0)
     pin = Pin(3,Pin.OUT)
     pin.value(0)
     
#motor y-as rechtsom draaien
def motory_hoog():
     pin_1 = Pin(4,Pin.OUT)
     pin_1.value(1)
     pin_2 = Pin(5,Pin.OUT)
     pin_2.value(0)

#motor y-as linksom draaien
def motory_laag():
     pin_3 = Pin(4,Pin.OUT)
     pin_3.value(0)
     pin_4 = Pin(5,Pin.OUT)
     pin_4.value(1)
     
#motor y-as uitzetten 
def motory_uit():
     pin = Pin(4,Pin.OUT)
     pin.value(0)
     pin = Pin(5,Pin.OUT)
     pin.value(0)
#functie infrarood sensor
def ir(stappen):
    aantal = 1
    for aantal in range(stappen):
        while True:
            if ir_sensor.value() ==0:
                while True:
                    if ir_sensor.value() ==1:
                        sleep(0.1)
                        break
                break
        aantal +=1
        print(aantal)

def sequentieel():
    posities = [0, 1, 2, 3]  # Definieer de posities
    for positie in posities:
        positie(positie)


  
#functie kalibratie
def kalibratie():
    #zet piston op intrekken
    piston.value(0)
    for i in range(100):
        if limit3.value() == 0:
            print('piston ingetrokken')
            break
        else:
            sleep(0.1)
            
        
    #Kalibreer de Y-as door naar beneden te bewegen tot de eindschakelaar is bereikt
    while True:
        motory_hoog()
        if limit4.value() == 0:
            motory_uit()
            break
        sleep(0.1)
    print("motor y-as uit")
    #draai de motor linksom
    while True:
        print("motor x-as aan")
        motorx_laag()
        # wacht tot de eindschakelaar
        if limit1.value() == 0:
            motorx_uit()
            break
        sleep(0.1)
    while True:
        print("Draait naar start positie")
        #draai de motor rechtsom nadat de eindschakelaar is geactiveerd
        motorx_hoog()
        #Wacht totdat de ir sensor 2x is getriggered
        ir(1)
        #zet de motor uit
        motorx_uit()
        break

#knopmenu functie
def knopmenu():
    while True:
        #kies de automatische modus
        if knop1.value() == 1:
            #laat de gebruiker weten wat er gebeurd
            print("automatische modus")
            sleep(1)
            while True:
                if knop1.value() == 1:
                    print("Sequentiële modus")
                    #posities
                    sequentieel()
                    break
                elif knop2.value() == 1:
                    print("Random modus")
                    #posities
                    positie(random.randint(0, 3))
                elif knop3.value() == 1:
                    #ga terug
                    break
                else:
                    sleep(0.2)
        #handmatige modus 
        elif knop2.value() == True:
            print("handmatige modus")
            sleep(0.2)
            while True:
                    #De knop bepaald de positie
                if knop1.value() == 1:
                    #positie
                    positie(0)
                elif knop2.value() == 1:
                    #positie
                    positie(1)
                elif knop3.value() == 1:
                    #positie
                    positie(2)
                    pass
                elif knop4.value() == 1:
                    #positie
                    pass
                    positie(3)
                elif knop5.value() == 1:
                    #terug naar andere menu
                    break
                else:
                    sleep(0.2)

def positie(plaats):
    # Zet y-as naar beneden tot limit2
    while True:
        motory_laag()
        if limit2.value() == 0:
            motory_uit()
            break
        else:
            sleep(0.1)
    # Schuif piston uit tot limit5
    while True:
        piston.value(1)
        if limit5.value() == 0:
            break
        else:
            sleep(0.1)
    # Zet y-as naar boven tot limit3
    while True:
        motory_hoog()
        if limit3.value() == 0:
            motory_uit()
            break
        else:
            sleep(0.1)
    # Schuif piston in tot limit4
    while True:
        piston.value(0)
        if limit4.value() == 0:
            break
        else:
            sleep(0.1)
    # X-as positie bepalen
    while True:
        if plaats == 1:
            motorx_laag()
            ir(2)
            motorx_uit()
            break
        elif plaats == 3:
            motorx_hoog()
            ir(2)
            motorx_uit()
            break
        elif plaats == 2:
            motorx_hoog()
            ir(3)
            motorx_uit()
            break
        elif plaats == 0:
            motorx_hoog()
            ir(4)
            motorx_uit()
            break
    while True:
        
        piston.value(1)
        # wacht tot uitgeschoven, breek de loop en anders ga door
        if limit5.value() == 0:
            break
        else:
            sleep(0.1)
    # zet motor naar beneden tot limit2
    while True:
        motory_laag()
        # wacht tot beneden, breek de loop en anders ga door
        if limit2.value() == 0:
            motory_uit()
            break
        else:
            sleep(0.1)
    # schuif piston in tot limit4
    while True:
        piston.value(0)
        # wacht tot ingeschoven, breek de loop en anders ga door
        if limit4.value() == 0:
            break
        else:
            sleep(0.1)
    # zet motor naar boven tot limit3
    while True:
        motory_hoog()
        # wacht tot boven, breek de loop en anders ga door
        if limit3.value() == 0:
            motory_uit()
            break
        else:
            sleep(0.1)
    # Schuif piston in
    while True:
        piston.value(0)
        # wacht tot ingeschoven, breek de loop en anders ga door
        if limit5.value() == 0:
            break
        else:
            sleep(0.1)
    while True:
        motory_hoog()
        # wacht tot beneden, breek de loop en anders ga door
        if limit4.value() == 0:
            motory_uit()
            break
        else:
            sleep(0.1)
        #Schuif piston in
    while True:
        #als positie 1 is ga naar links tot correcte positie
        if plaats == 1:
            motorx_hoog()
            ir(2)
            motorx_uit()
            break
        #als positie 3 is ga naar rechts tot correcte positie
        elif plaats == 3:
            motorx_laag()
            ir(2)
            motorx_uit()
            break
        #als positie 2 is ga naar rechts tot correcte positie
        elif plaats == 2:
            motorx_laag()
            ir(3)
            motorx_uit()
            break
        #als positie 0 is ga naar rechts tot correcte positie
        elif plaats == 0:
            motorx_laag()
            ir(4)
            motorx_uit()
            break
    
kalibratie()
#while True:
 #   knopmenu()
 #   # wacht 3 seconden voor de volgende iteratie
  #  sleep(3)