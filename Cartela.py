import random

def generar_numero_sin_repetir(inicio, fin, numeros_seleccionados):
    numero = random.randint(inicio, fin)
    while numero in numeros_seleccionados:
        numero = random.randint(inicio, fin)
    numeros_seleccionados.append(numero)
    return numero

def generar_carton_bingo():
    carton = []
    numeros_seleccionados = []
    rangos_letras = {'B': (1, 18), 'I': (19, 36), 'N': (37, 54), 'G': (55, 72), 'O': (73, 90)}
    
    for _ in range(5):
        fila = []
        for letra, rango in rangos_letras.items():
            numero = generar_numero_sin_repetir(rango[0], rango[1], numeros_seleccionados)
            fila.append(numero)
        carton.append(fila)
    return carton

def imprimir_carton(carton):
    bingo = ["B","I","N","G","O"]
    print(bingo)
    for fila in carton:
        print(fila)

if __name__ == "__main__":
    carton = generar_carton_bingo()
    imprimir_carton(carton)