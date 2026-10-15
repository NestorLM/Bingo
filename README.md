# Bingo Web

Aplicacion de Bingo con interfaz web para anfitrion, carton interactivo para jugadores y generacion de cartones en PDF.

## Caracteristicas

- Panel principal con numero actual grande, historial de ultimos sorteos y tablero B-I-N-G-O.
- Carton interactivo para marcar numeros desde celular o PC.
- Generacion de PDF listo para imprimir (4 cartones por hoja).
- 100% frontend: HTML, CSS y JavaScript sin necesidad de Python ni servidor.

## Como ejecutar

Simplemente abre `index.html` en tu navegador (doble click). No se requiere instalacion ni servidor.

### Opcional: servir con Python

Si querés acceder desde otros dispositivos en tu red:

```bash
python -m http.server 8080
```

Luego abri `http://TU_IP:8080/index.html` desde el otro dispositivo.

## Archivos

- **index.html** — Panel principal del anfitrion (sorteo, tablero, QR, generacion de PDF).
- **carton_bingo.html** — Carton interactivo para jugadores (marcar numeros).

## Dependencias

Todas se cargan desde CDN (no requiere instalacion):

- Tailwind CSS (estilos)
- QRCode.js (generacion de QR)
- jsPDF (generacion de PDF)