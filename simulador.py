"""
Proyecto Final Sistemas Operativos
Pablo César Ruíz Hernández A01197044
Uriel Fuentes A00820592
Humberto Tello A01196965
Alexis Ruiz Bernadac A00819813
"""

def FIFO(comandos): 
    cuantoTiempo = 0
    print("FIFO")
    queue = []
    pageFaults = {}
    memoriaVirtual = []
    M = 2048 #Bytes disponibles en memoria
    S = 4096 #Bytes disponibles en memoria swapping
    for comand in comandos:
        #print(comand)
        cuantoTiempo += 1
        if comand[0] == 'P': # se entra al comando P
            if M - comand[1] > 0:
                start = cuantoTiempo #Toma cuenta del tiempo en el que entro
                pair = []
                M -= comand[1]
                pair.append(comand) #Guarda la informacion del proceso y lo introduce en la fila de cargados
                pair.append(start)
                queue.append(pair)
                if comand[2] in pageFaults: #Incrementa el numero de page faults si es necesario
                    pageFaults[comand[2]] += 1 
                else:
                    pageFaults[comand[2]] = 1
            else:
                while M - comand[1] < 0 and  pair in queue: #Si no hay memoria suficiente, hace el algoritmo FIFO hasta que haya suficiente memoria
                        temp = pair[0]
                        M += temp[1]
                        memoriaVirtual.append(queue[0]) #Introduce el programa en memoria de swapping 
                        queue.pop(0) 
                        if comand[2] in pageFaults: #Incrementa el numero de page faults
                            pageFaults[comand[2]] += 1
                        else:
                            pageFaults[comand[2]] = 1
        if comand[0] == 'L': #se entra al comando L
            for pair in queue: #Borra el proceso de memoria, dependiendo de donde este
                temp = (pair[0])
                if temp[2] == comand[1]: 
                    end = cuantoTiempo
                    start = pair[1]
                    pair.pop()
                    pair.append(end-start)
                    memoriaVirtual.append(pair) 
                    S -= pair[1] #Libera el espacio de memoria
                    M += pair[1]
                    queue.remove(pair) #Borra el proceso de la fila
                    print(pair)
                    print('se libera el marco #',pair[0][1])
        if comand[0] == 'A': #se entra al comando A para leer o modificar proceso
            print(comand)
            if comand[3] == 0: 
                for pair in queue: #Busca el proceso dado
                    temp = pair[0]
                    if temp[2] == comand[2]:
                        print('lectura del proceso : ' + str(temp))
                for pair in memoriaVirtual:
                    temp = pair[0]
                    if temp[2] == comand[2]: # si no esta en la memoria se marca el error y se genera el pagefault
                        print(str(temp) + ' no está en la memoria')
                        if comand[2] in pageFaults:
                            pageFaults[comand[2]] += 1
                        else:
                            pageFaults[comand[2]] = 1            
            if comand[3] == 1: #Modifica la posicion de memoria dada
                for pair in queue:
                    temp = pair[0]
                    if temp[2] == comand[2]: 
                        print('direccion real: ',pageFaults[temp[2]])
                        pair = []
                        aux = temp[2]
                        temp.remove(temp[1])
                        temp.remove(temp[1])
                        temp.append(comand[1])
                        temp.append(aux)
                    else:
                        if comand[2] in pageFaults:
                            pageFaults[comand[2]] += 1
                        else:
                            pageFaults[comand[2]] = 1
        if comand[0] == 'F': #Fin de las instrucciones, hace la cuenta de los fallos de pagina
            cuentaPageFaults = 0
            totalTurn = 0
            totalPro = 0
            for f in pageFaults:
                cuentaPageFaults += pageFaults[f]

            #Hace el formato de impresion
            print('Total page faults: ' + str(cuentaPageFaults) )
            print('Page Faults por id de proceso: ')
            for f in pageFaults:
                print( 'en el marco #' + str(f) + ' con el proceso: ' + str(pageFaults[f]))
            
            print('Turnaround de FIFO') #Imprime el turnaround para el algoritmo de FIFO
            for mem in memoriaVirtual:
                temp = mem[0]
                totalTurn += mem[1]
                totalPro += 1
                print('el proceso #' + str(temp[2]) + ' tarda: ' + str(mem[1]))
            for mem in queue:
                temp = mem[0]
                totalTurn += mem[1]
                totalPro += 1
                print('el proceso #' + str(temp[2]) + ' tarda: ' + str(mem[1]))

            if totalPro != 0:
                print('Average turnaround = ' + str(totalTurn/totalPro))
        if comand[0] == 'C':
            for c in range(len(comand)):
                if(c!=0):
                    for count in range(len(comand[c])):
                        print(comand[c][count],end=' ')
            print('')

def LRU(comandos): #Algoritmo de LRU
    print("LRU")
    cuantoTiempo = 0
    queue = []
    pageFaults = {}
    memoriaVirtual = []
    M = 2048 #Bytes disponibles en memoria
    S = 4096 #Bytes disponibles en memoria de sweeping
    for comand in comandos: #Carga el proceso a memoria
        cuantoTiempo += 1 #Contador de tiempo 
        if comand[0] == 'P':
            if M - comand[1] > 0: #Introduce el proceso a memoria si hay suficiente espacio
                start = cuantoTiempo
                terna = []
                M -= comand[1]
                terna.append(comand)
                terna.append(start)
                terna.append(start)
                queue.append(terna)
                if comand[2] in pageFaults: #Contabiliza el numero de fallos de pagina
                    pageFaults[comand[2]] += 1
                else:
                    pageFaults[comand[2]] = 1
            else:
                while M - comand[1] < 0 and  terna in queue: #Si no hay memoria suficiente, desaloja un proceso
                        temp = terna[0]
                        M += temp[1]
                        memoriaVirtual.append(queue[0])
                        queue.pop(0)

                        if comand[2] in pageFaults: 
                            pageFaults[comand[2]] += 1
                        else:
                            pageFaults[comand[2]] = 1
        if comand[0] == 'L': #Hace el algortimo de LRU para desalojar un proceso
            oldestPro = -1
            popId = -1
            proTemp = []
            for terna in queue:
                temp = terna[0]
                end = cuantoTiempo
                start = terna[1]
                terna.pop()
                terna.append(end-start)
            for terna in queue:
                temp = terna[2]
                if temp > oldestPro:
                    oldestPro = temp
                    proTemp = terna[0]
                    popId = proTemp[2]
            for terna in queue:
                temp = (terna[0])
                if temp[2] == popId:
                    end = cuantoTiempo
                    start = terna[1]
                    aux = terna[2]
                    terna.pop()
                    terna.pop()
                    terna.append(end-start)
                    terna.append(aux)
                    memoriaVirtual.append(terna)
                    S -= terna[1]
                    M += terna[1]
                    queue.remove(terna)
                    print(terna)
                    print('se libera el marco #',terna[0][1])

        if comand[0] == 'A': #Hacer el comando de A para ver o modificar direcciones en memoria
            if comand[3] == 0: #Comando para ver direccion en memoria
                for terna in queue: 
                    temp = terna[0]
                    
                    if temp[2] == comand[2]:
                        print('lectura del proceso : ' + str(temp))
                        start = cuantoTiempo
                        terna.pop()
                        terna.append(start)
                for terna in memoriaVirtual:
                    temp = terna[0]
                    if temp[2] == comand[2]:
                        print(str(temp) + ' no está en la memoria')

                        if comand[2] in pageFaults:
                            pageFaults[comand[2]] += 1
                        else:
                            pageFaults[comand[2]] = 1            
            if comand[3] == 1: #Comando para verificar direccion en memoria
                for terna in queue:
                    temp = terna[0]
                    if temp[2] == comand[2]: 
                        print('direccion real: ',pageFaults[temp[2]])
                        terna = []
                        aux = temp[2]
                        temp.remove(temp[1])
                        temp.remove(temp[1])
                        temp.append(comand[1])
                        temp.append(aux)
                    else:
                        if comand[2] in pageFaults:
                            pageFaults[comand[2]] += 1
                        else:
                            pageFaults[comand[2]] = 1
        if comand[0] == 'F': #Comando para finalizar y guardar los fallos de pagina
            cuentaPageFaults = 0
            totalTurn = 0
            totalPro = 0
            for fallas in pageFaults:
                cuentaPageFaults += pageFaults[fallas]

            print('Total page faults: ' + str(cuentaPageFaults) )
            

            
            print('Page Faults por id de proceso: ')

            
            for fallas in pageFaults:
                print( 'en el marco #' + str(fallas) + ' con el proceso: ' + str(pageFaults[fallas]))

            print('Turnaround de LRU') #Imprimir el tiempo de turnaround 
            
            for mem in memoriaVirtual:
                temp = mem[0]
                totalTurn += mem[1]
                totalPro += 1
                print('el proceso #' + str(temp[2]) + ' tarda: ' + str(mem[1]))


            for m in queue:
                temp = mem[0]
                totalTurn += mem[1]
                totalPro += 1
                print('el proceso #' + str(temp[2]) + ' tarda: ' + str(mem[1]))
             
            
            if totalPro != 0:
                print('Average turnaround = ' + str(totalTurn / totalPro))
        if comand[0] == 'C': #Hacer clear
            for c in range(len(comand)):
                if(c!=0):
                    for count in range(len(comand[c])):
                        print(comand[c][count],end=' ')
            print('')



f = open("./entrada.txt", "r") #Abre el archivo con la entrada
lines = f.read().splitlines()
comandos = []
for i, linea in enumerate(lines): #Da formato al archivo para procesar los procesos
    words = linea.rstrip()
    words = words.lstrip()
    words =' '.join(words.split())

    """
    existen varios tipos de instrucciones que se enlistan a continuacion
    C sirve para iniciar un comentario en el programa, todo lo del a derecha se ignora
    P sirve para cargar un proceso y lleva dos parametros, el numero de bytes del proceso y el identificador del proceso
    L sirve para liberar las paginas del proceso p, donde p es el identificador del proceso
    A sirve para accesar a una direccion virtual, tiene tres parametros, d, p, y m, se accesa a la dirección d del proceso p y dependiendo de si m es 0 o 1, se lee o se modifica
    F sirve para indicar la ultima linea de un conjunto de solicitudes
    E sirve para indicar que se acaba el archivo
    """ 
    listaLineas = words.split()
    instruccion = []
    #Hace un arreglo que contiene toda la información de cada proceso y los parametros 
    if words[0] == 'A':
        instruccion.append(listaLineas[0])
        instruccion.append(int(listaLineas[1]))
        instruccion.append(int(listaLineas[2]))
        instruccion.append(int(listaLineas[3]))

    if words[0] == 'P':
        instruccion.append(listaLineas[0])
        instruccion.append(int(listaLineas[1]))
        instruccion.append(int(listaLineas[2]))
    
    if words[0] == 'L':
        instruccion.append(listaLineas[0])
        instruccion.append(int(listaLineas[1]))

    if words[0] == 'C':
        instruccion.append(listaLineas[0])
        instruccion.append(listaLineas[1:])
    
    if words[0] == 'E':
        instruccion.append(listaLineas[0])

    if words[0] == 'F':
        instruccion.append(listaLineas[0])
    comandos.append(instruccion)    

#print(comandos) 
FIFO(comandos)  #Ejecuta ambos algoritmos 
LRU(comandos)