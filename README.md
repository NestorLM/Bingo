# Bingo Web

Aplicación web de Bingo con generación de cartones en PDF y cartón interactivo web. Incluye un lanzador gráfico para iniciar y detener el servidor fácilmente.

## Características
- Sorteo de números de Bingo.
- Visualización del último y los últimos 5 números sorteados.
- Generación de cartones en PDF listos para imprimir.
- Cartón interactivo web para jugar desde el móvil o PC.
- Lanzador `.exe` con botones para iniciar/detener el servidor y abrir la web.

## Uso

1. Instala los requerimientos:
   ```
   pip install -r requirements.txt
   ```
2. Ejecuta el lanzador:
   ```
   python launcher.py
   ```
3. Para crear el `.exe`:
   ```
   pip install pyinstaller
   pyinstaller --onefile --noconsole launcher.py
   ```
   El ejecutable estará en la carpeta `dist/`.

## Acceso desde otros dispositivos

Asegúrate de que el puerto 5000 esté abierto en el firewall y que ambos dispositivos estén en la misma red.

---