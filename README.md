# Bingo Web

Aplicacion de Bingo con interfaz web para anfitrion, carton interactivo para jugadores y generacion de cartones en PDF.

## Caracteristicas

- Panel principal con numero actual grande, historial de ultimos sorteos y tablero B-I-N-G-O.
- Carton interactivo para marcar numeros desde celular o PC.
- Generacion de PDF listo para imprimir (4 cartones por hoja).
- Lanzador de escritorio con botones para iniciar y detener servidor.
- Seleccion de puerto automatica y configurable.

## Requisitos

- Python 3.10 o superior.
- Dependencias del proyecto (archivo actual: requiments.txt).

Instalacion:

```bash
pip install -r requiments.txt
```

## Ejecutar en modo desarrollo

```bash
python launcher.py
```

El launcher abre automaticamente el navegador en la URL local.

## Puerto del servidor

La aplicacion intenta usar estos puertos en orden:

1. Puerto definido en la variable de entorno BINGO_PORT.
2. 8080
3. 5000
4. 8000
5. 8888
6. Si todos estan ocupados, toma uno libre automaticamente.

Ejemplo para forzar puerto:

```bash
set BINGO_PORT=8080
python launcher.py
```

## Compilar ejecutable (.exe)

Usa el script build_exe.bat:

```bat
build_exe.bat
```

El ejecutable se genera en:

- dist\\launcher.exe

## Acceso desde otros dispositivos

- Conecta ambos equipos a la misma red local.
- Permite el puerto elegido en el firewall de Windows si es necesario.
- Escanea el QR del panel principal para abrir el carton interactivo.