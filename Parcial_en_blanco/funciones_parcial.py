import os
import re


def parcial_app():
    """Ejecuta el programa del parcial"""
    bandera_votos_cargados = False
    bandera_ballotage = False
    
    while True:
        os.system('cls')
        opcion = menu_parcial()
        os.system('cls')
        
        
        match opcion:
            case 1:
                matriz_votos = inicializar_matriz(5, 3, 0)
                carga_exitosa = cargar_votos(matriz_votos)
                votos_totales = contar_total_votos(matriz_votos)
                calcular_porcentaje_matriz(matriz_votos, votos_totales)
                asignar_numero_lista(matriz_votos)
                if carga_exitosa:
                    bandera_votos_cargados = True
                    
                    
            case 2:
                if bandera_votos_cargados:
                    imprimir_matriz_votos(matriz_votos)
                else: 
                    print("Debe cargar los votos primero")
                
                    
            case 3:
                if bandera_votos_cargados:
                    ordenar_matriz_por_indice(matriz_votos, 1, False)
                    print("Matriz ordenada por votos TM")
                    print("------------------------------------------")
                else: 
                    print("Debe cargar los votos primero")
                       
                    
            case 4:
                if bandera_votos_cargados:
                    lista_inferiores = encontrar_inferior(matriz_votos)
                    if lista_inferiores:
                        print("Listas con menos del 5%")
                        print("-----------------------------------------------------")
                        imprimir_matriz_votos(lista_inferiores)
                    else:
                        print("No se encontraron listas con esa cantidad de votos")
                else: 
                    print("Debe cargar los votos primero")     
                
                
            case 5:
                if bandera_votos_cargados:
                    print("El turno que mas voto fue:")
                    print("--------------------------")
                    votos_turno_mañana = contar_total_por_indice(matriz_votos, 1)
                    votos_turno_tarde = contar_total_por_indice(matriz_votos, 2)
                    votos_turno_noche = contar_total_por_indice(matriz_votos, 3)
                    encontrar_mayor_imprimir_turno(votos_turno_mañana, votos_turno_tarde, votos_turno_noche)
                else: 
                    print("Debe cargar los votos primero") 
                    
                    
            case 6:
                if bandera_votos_cargados:
                    lista_superiores = encontrar_superior(matriz_votos)
                    if lista_superiores:
                        print("Lista elegida con mas del 50%")
                        print("-------------------------------------")
                        imprimir_matriz_votos(lista_superiores)
                    else:
                        print("No hay lista con mas del 50%. HAY BALLOTAGE!")
                        bandera_ballotage = True
                else: 
                    print("Debe cargar los votos primero")     
                  
                  
            case 7:
                if bandera_votos_cargados:
                    if bandera_ballotage:
                        pass
                else: 
                    print("Debe cargar los votos primero")
                  
                  
            case 8:
                if finalizar_programa():
                    break
                
                
            case _:
                print("FUERA DEL RANGO")

        os.system("pause")
        
        
def menu_parcial():
    """Imprime el menu de opciones, pide al usuario que ingrese un numero y lo valida"""
    imprimir_menu_desafio_ordenamiento()
    opcion = input("Ingrese una opcion de la lista: ").replace(" ", "").upper()
    opcion_valida = validar_opcion_numerica(opcion)
    if opcion_valida:
        return int(opcion)
    else:
        return -1
    
    
def imprimir_menu_desafio_ordenamiento()->None:
    """Imprime el menu de opciones"""
    print(
        """
        ***MENU DE OPCIONES***
        ----------------------
        OPCION 1: Cargar votos
        OPCION 2: Mostrar votos
        OPCION 3: Ordenar votos turno mañana
        OPCION 4: Mostrar listas con menos del 5%
        OPCION 5: Mostrar turno que mas voto
        OPCION 6: Informar electo o ballotage
        OPCION 7: 
        OPCION 8: FINALIZAR PROGRAMA
        """
    )
    
    
def finalizar_programa()->bool:
    """Solicita al usuario que ingrese un parametro.
        Y (Salir)
        N (Cancelar)
        
    Returns:
        bool: True (y) | False (n)
    """
    while True:
        confirmacion_final_programa = input("DESEA FINALIZAR PROGRAMA (y/n): ")
        confirmacion_final_programa = confirmacion_final_programa.strip().replace(" ", "").lower()
        if re.match(r'^[a-z]$', confirmacion_final_programa):
            if confirmacion_final_programa == 'y':
                print("PROGRAMA FINALIZADO")
                return True
            elif confirmacion_final_programa == 'n':
                print("Continuando programa")
                return False
            else:
                print("Letra ingresada no valida. Ingrese y/n.")
        else:
            print("El dato ingresado no coincide con los esperados. REINTENTE")
            
            
def validar_opcion_numerica(opcion: str)->bool:
    """Recibe un string y valida que este conformado unicamente por un numero.
    Devuelve True si cumple la condición o False si no la cumple."""
    if opcion and re.match(r'^[0-9]+$', opcion):
        return True
    else:
        print("INCORRECTO. Solo se puede ingresar un numero")
        return False
    
    
def inicializar_matriz(cantidad_filas: int, cantidad_columnas: int, valor_inicial:any)->list:
    """
    Inicializa una matriz con la extension pasada por parametro

    Args:
        cantidad_filas (int): Numero de filas de la matriz.
        cantidad_columnas (int): Numero de columnas de la matriz.
        valor_inicial (any): Valor con el que se inicializan los elementos de la matriz.

    Returns:
        list: Matriz
    """
    matriz = []
    
    for i in range(cantidad_filas):
        fila = [valor_inicial] * cantidad_columnas
        matriz += [fila]
    return matriz


def cargar_votos(matriz)->bool:
    """Recorre y carga los votos para cada lista

    Args:
        matriz (list): Matriz donde se colocan los votos

    Returns:
        bool: True si la carga es exitosa, False si la carga falla
    """
    if matriz:
        filas = len(matriz)
        columnas = len(matriz[0])

        for participante in range(filas):
            print(f"Ingresando votos para lista {participante + 1}:")
            for jurado in range(columnas):
                nota = solicitar_nota(1, 999, jurado)
                matriz[participante][jurado] = nota
        print("Votos cargados correctamente")
        return True
    else:
        print("La matriz está vacía y no se pueden cargar votos.")
        return False


def solicitar_nota(minimo: float, maximo: float, jurado)->float:
    """Solicita una numero al usuario y valida que este dentro del rango

    Args:
        minimo (float): valor minimo del rango
        maximo (float): valor maximo del rango

    Returns:
        float: numero validado, dentro del rango
    """
    if jurado == 0:
        turno = "TM"
    elif jurado == 1:
        turno = "TT"
    else:
        turno = "TN"
    while True:
        nota = input(f"Ingrese cantidad de votantes {turno} -> {minimo} y {maximo}: ")
        try: 
            nota = float(nota)
            if nota >= minimo and nota <= maximo:
                return nota
            else:
                print(f"Nota invalida. Reingrese un numero entre {minimo} y {maximo}: ")
        except ValueError:
            print("Eso no es un numero")

def contar_total_votos(matriz: list)->int:
    """Cuenta la cantidad total de votos de la matriz

    Args:
        matriz (list): Matriz con los votos
        int: Cantidad de votos totales
    """
    if matriz:
        filas = len(matriz)
        columnas = len(matriz[0])
        
        total_votos = 0
        
        for i in range(filas):
            for j in range(columnas):
                total_votos += matriz[i][j]
        return total_votos
            
    
def calcular_porcentaje_matriz(matriz: list, cantidad_votos_totales: int):
    """Calcula el porcentaje de una matriz agregandolo al final de la misma
    
    Args:
        matriz (list): Matriz a calcular
        cantidad_votos_totales (int): Cantidad de votos totales
    """
    if matriz:
        filas = len(matriz)
        columnas = len(matriz[0])
        
        for i in range(filas):
            votos_lista = 0
            for j in range(columnas):
                votos_lista += matriz[i][j]
            porcentaje = (votos_lista / cantidad_votos_totales) * 100
            matriz[i]+= [porcentaje]
    else:
        print("Matriz vacia")


def asignar_numero_lista(matriz: list):
    """Asigna un numero a lista
    
    Args:
        matriz (list): Matriz de las listas
    
    Returns:
        list: Matriz con nro de lista
    """
    if matriz:
        for i in range(len(matriz)):
            matriz[i] = [i + 1] + matriz[i]
    return matriz


def imprimir_matriz_votos(matriz:list):
    """Imprime la matriz en un formato prolijo, con votos y porcentaje de 
    cada lista con encabezado:
    "Nro Lista | CANT VOTOS TM ... PORC DE VOTOS:"

    Args:
        matriz (list): Matriz a imprimir
    """
    if matriz:
        filas = len(matriz)
        # columnas = len(matriz[0])

        print("MATRIZ VOTOS:")
        print("------------------")
        print(" Nro Lista | Votos TM | Votos TT | Votos TN | Porcentaje votos")
        for i in range(filas):
            print (f"{matriz[i][0]:^11}", end= "|")
            for j in range(1,4):
                print(f"{matriz[i][j]:^10}", end="|")
            print(f"{matriz[i][4]:^10.2f}")
    else:
        print("La matriz esta vacia")


def ordenar_matriz_por_indice(matriz: list, indice_ordenamiento: int, asc: bool = True):
    """Ordena la matriz de votantes según un indice especifico.

    Args:
        matriz (list): Matriz a ordenar.
        indice_ordenamiento (int): Índice por el que se ordenara la lista
        asc (bool, optional): True para ordenación ascendente, False para descendente. (por defecto, ascendente)
    """
    tam = len(matriz)

    for i in range(tam - 1):
        for j in range(0, tam - i - 1):
            if (asc and matriz[j][indice_ordenamiento] > matriz[j + 1][indice_ordenamiento]) or \
               (not asc and matriz[j][indice_ordenamiento] < matriz[j + 1][indice_ordenamiento]):
                aux = matriz[j]
                matriz[j] = matriz[j + 1]
                matriz[j + 1] = aux
                
                
def encontrar_inferior(matriz:list)-> list:
    """Encuentra las listas que tengan menos del 5% de los votos
    
    Args:
        matriz (list): Matriz de los votos

    Returns:
        list: Lista de las listas con menos del 5%
    """
    if matriz:
        filas = len(matriz)
        lista_inferiores = []
        for i in range(filas):
            if matriz[i][4] < 5:
                lista_inferiores += [matriz[i]]
        return lista_inferiores
    else:
        print("La matriz esta vacia")
        return []


def contar_total_por_indice(matriz: list, indice_turno)->list:
    """Recorre la matriz contando la cantidad de votos por turno

    Args:
        matriz (list): Matriz con los votos

    Returns:
        int: Contador total de votos
    """
    if matriz:
        filas = len(matriz)
        acumulador_turno = 0
        
        for i in range(filas):
            acumulador_turno += matriz[i][indice_turno]
        return acumulador_turno


def encontrar_mayor_imprimir_turno(total_turno_mañana: int, total_turno_tarde: int,
                                   total_turno_noche: int):
    """Encuentra el turno con mayor cantidad de votos y lo imprime en pantalla

    Args:
        total_turno_mañana (int): Cantidad total de votos TM
        total_turno_tarde (int): Cantidad total de votos TT
        total_turno_noche (int): Cantidad total de votos TN
    """
    if total_turno_mañana > total_turno_tarde and total_turno_mañana > total_turno_noche:
        print(f"Turno mañana con: {total_turno_mañana} votos.")
    else: 
        if total_turno_tarde >= total_turno_noche:
            print(f"Turno tarde con: {total_turno_tarde} votos.")
        else:
            print(f"Turno noche con: {total_turno_noche} votos.")
            
                
def encontrar_superior(matriz:list)-> list:
    """Encuentra las listas que tengan mas del 50% de los votos
    
    Args:
        matriz (list): Matriz de los votos

    Returns:
        list: Lista de las listas con menos del 50%
    """
    if matriz:
        filas = len(matriz)
        lista_superiores = []
        for i in range(filas):
            if matriz[i][4] > 50:
                lista_superiores += [matriz[i]]
        return lista_superiores
    else:
        print("La matriz esta vacia")
        return []
