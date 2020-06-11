import threading 
import os

contadorConSemaforo = 0
contadorSinSemaforo = 0
incrementos = 100000
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
    #print("Cuenta: {}".format(contadorConSemaforo))
    #print("Proceso que se esta ejecutando: {}".format(os.getpid())) 
    semaforo.release()

def adderSinSemaforo():
    for i in range (incrementos):
        aumenta(1)


#se declaran los threads
threadsConSemaforo = []
threadsSinSemaforo = []

#solo se va a usar un semaforo, se detiene siempre que se entre a un proceso y se activa de nuevo antes de salir
semaforo = threading.Semaphore() 

#en vez de 5 probar con los 10,000 que se nos piden, pero si se piden loggear se tarda como 4 segundos en imprimir todo
print("Ejecutando 10000 procesos con semaforos")
for i in range(10000):
    threadsConSemaforo.append(threading.Thread(target=adderConSemaforo, args=(semaforo,)))

#se inician los threads
for thread in threadsConSemaforo:
    thread.start()

#se agrega .join para que el programa espere a que todos los procesos se ejecuten
for thread in threadsConSemaforo: 
    thread.join()


print("Contador con semaforos:", contadorConSemaforo, "con incrementos de:", incrementos)
print("Ejecutando 10000 procesos sin semaforos")


#en vez de 5 probar con los 10,000 que se nos piden, pero si se piden loggear se tarda como 4 segundos en imprimir todo
for i in range(10000):
    threadsSinSemaforo.append(threading.Thread(target=adderSinSemaforo))

#se inician los threads
for thread in threadsSinSemaforo:
    thread.start()

#se agrega .join para que esperen a que terminen en orden para ser ejecutados
for thread in threadsSinSemaforo: 
    thread.join()

print("Contador sin semaforos:",contadorSinSemaforo, "con incrementos de:", incrementos)