import threading 
import os

"""
Proyecto Final Sistemas Operativos - puntos extras
Pablo César Ruíz Hernández A01197044
Uriel Fuentes A00820592
Humberto Tello A01196965
Alexis Ruiz Bernadac A00819813
"""

contadorConSemaforo = 0
contadorSinSemaforo = 0
print("se nota mas el cambio en el conteo de los semaforos cuando el incremento es mas grande, ej 100,000, pero si se prueba con 10,000 procesos, se tarda aproximadamente 5 minutos en correr")
incrementos = int(input("De cuanto quiere que sean los incrementos de los procesos? "))

def aumenta(identificador):
    global contadorConSemaforo, contadorSinSemaforo
    '''
    identificador = 0 : con semaforo
    identificador = 1 : sin semaforo
    '''
    if(identificador == 0):
        contadorConSemaforo += 1
    elif(identificador == 1):
        contadorSinSemaforo += 1


def adderConSemaforo(semaforo): 
    semaforo.acquire()
    for i in range (incrementos):
        aumenta(0)
    semaforo.release()

def adderSinSemaforo():
    for i in range (incrementos):
        aumenta(1)


#se declaran los threads
threadsConSemaforo = []
threadsSinSemaforo = []

#solo se va a usar un semaforo, se detiene siempre que se entre a un proceso y se activa de nuevo antes de salir
semaforo = threading.Semaphore() 
numeroDeProcesos = int(input('Cuantos procesos desea ejecutar en paralelo? '))
print("Ejecutando", numeroDeProcesos ,"procesos con semaforos")
for i in range(numeroDeProcesos):
    threadsConSemaforo.append(threading.Thread(target=adderConSemaforo, args=(semaforo,)))

#se inician los threads
for thread in threadsConSemaforo:
    thread.start()

#se agrega .join para que el programa espere a que todos los procesos se ejecuten
for thread in threadsConSemaforo: 
    thread.join()

print("Contador con semaforos:", contadorConSemaforo, "con incrementos de:", incrementos)
print("Ejecutando", numeroDeProcesos ,"procesos con semaforos")

for i in range(numeroDeProcesos):
    threadsSinSemaforo.append(threading.Thread(target=adderSinSemaforo))

#se inician los threads
for thread in threadsSinSemaforo:
    thread.start()

#se agrega .join para que esperen a que terminen en orden para ser ejecutados
for thread in threadsSinSemaforo: 
    thread.join()

print("Contador sin semaforos:",contadorSinSemaforo, "con incrementos de:", incrementos)