import random
import sys

def sortear_numero():
    rangos_letras = {'B': (1, 18), 'I': (19, 36), 'N': (37, 54), 'G': (55, 72), 'O': (73, 90)}
    letra = random.choice(list(rangos_letras.keys()))
    numero = random.randint(rangos_letras[letra][0], rangos_letras[letra][1])
    return letra, numero

def imprimir_numero(letra, numero):
    print(f"{letra} {numero}")

#if __name__ == "__main__":
#    numeros_sorteados = set()
#    numero = 0
#    print("Presiona ENTER para sortear un número (q para salir):")
#    while len(numeros_sorteados) < 90:
#        entrada = input()
#        if entrada.lower() == 'q':
#            sys.exit("¡Hasta luego!")
#        while numero in numeros_sorteados or numero == 0:
#            letra, numero = sortear_numero()
#        if numero not in numeros_sorteados:
#            numeros_sorteados.add(numero)
#            imprimir_numero(letra, numero)
