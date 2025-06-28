import io
import Sorteo
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask import Flask, render_template, jsonify, send_file, request, url_for
from Cartela import generar_carton_bingo
import qrcode
from reportlab.lib.utils import ImageReader

app = Flask(__name__)

numeros_sorteados = set()

# Definimos el rango de letras
rangos_letras = {'B': (1, 18), 'I': (19, 36), 'N': (37, 54), 'G': (55, 72), 'O': (73, 90)}

@app.route('/')
def index():
    # Construir la URL absoluta para /carton_bingo
    carton_url = url_for('carton_bingo', _external=True)
    # Generar el QR dinámicamente en memoria
    qr_img = qrcode.make(carton_url)
    qr_buffer = io.BytesIO()
    qr_img.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)
    qr_data = qr_buffer.getvalue()
    import base64
    qr_base64 = base64.b64encode(qr_data).decode('utf-8')
    return render_template('index.html', rangos_letras=rangos_letras, qr_base64=qr_base64)  # Pasamos rangos_letras al contexto del template

@app.route('/sortear_numero')
def sortear_numero():
    global numeros_sorteados
    numero = 0
    letra = "a"
    while len(numeros_sorteados) < 90:
        while numero in numeros_sorteados or numero == 0:
            letra, numero = Sorteo.sortear_numero()
        if numero not in numeros_sorteados:
            numeros_sorteados.add(numero)
            break  # Salir del bucle una vez que se ha encontrado un número único
    return jsonify({'letra': letra, 'numero': numero})

@app.route('/reset')
def reset():
    global numeros_sorteados
    numeros_sorteados = set()
    return 'Reset realizado'

@app.route('/generar_pdf', methods=['POST'])
def generar_pdf():
    try:
        cantidad_hojas = int(request.form.get('cantidad_hojas', 1))
    except ValueError:
        cantidad_hojas = 1

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    for _ in range(cantidad_hojas):
        cartones = [generar_carton_bingo() for _ in range(4)]
        for idx, carton in enumerate(cartones):
            # Márgenes y espacio para 2x2 cartones por hoja
            margen_x = 30
            margen_y = 30
            espacio_x = (width - 2 * margen_x) / 2
            espacio_y = (height - 2 * margen_y) / 2
            x0 = margen_x + (idx % 2) * espacio_x
            y0 = height - margen_y - (idx // 2) * espacio_y

            filas = 5
            columnas = 5

            # Celdas cuadradas: el lado es el menor entre ancho y alto disponible para la tabla
            lado_celda = min((espacio_x - 30) / columnas, (espacio_y - 60) / filas)
            tabla_ancho = lado_celda * columnas
            tabla_alto = lado_celda * filas

            # Centrar la tabla dentro del espacio del cartón
            tabla_x = x0 + (espacio_x - tabla_ancho) / 2
            tabla_y = y0 - 35  # Espacio para el título y encabezados

            # Título
            p.setFont("Helvetica-Bold", 13)
            p.drawCentredString(x0 + espacio_x/2, y0 - 15, "Cartón de Bingo")

            # Encabezados de columnas
            columnas_letras = ['B', 'I', 'N', 'G', 'O']
            p.setFont("Helvetica-Bold", 12)
            for i, letra in enumerate(columnas_letras):
                p.drawCentredString(
                    tabla_x + i * lado_celda + lado_celda/2,
                    tabla_y,
                    letra
                )

            # Paleta de colores pastel
            colores = [
                (0.85, 0.93, 0.98),  # celeste claro
                (0.93, 0.98, 0.85),  # verde claro
                (0.98, 0.93, 0.85),  # naranja claro
                (0.96, 0.85, 0.98),  # lila claro
                (0.98, 0.98, 0.85),  # amarillo claro
            ]

            # Dibujar celdas cuadradas con color de fondo alternado
            p.setLineWidth(1)
            for fila in range(filas):
                for col in range(columnas):
                    x1 = tabla_x + col * lado_celda
                    y1 = tabla_y - 10 - fila * lado_celda
                    color = colores[col % len(colores)]
                    p.setFillColorRGB(*color)
                    p.rect(x1, y1 - lado_celda, lado_celda, lado_celda, fill=1, stroke=0)
                    # Borde de celda
                    p.setStrokeColorRGB(0.7, 0.7, 0.7)
                    p.rect(x1, y1 - lado_celda, lado_celda, lado_celda, fill=0, stroke=1)

            # Borde exterior más grueso y oscuro
            p.setLineWidth(2)
            p.setStrokeColorRGB(0.2, 0.4, 0.7)
            p.rect(tabla_x, tabla_y - 10 - filas * lado_celda, lado_celda * columnas, lado_celda * filas, fill=0, stroke=1)

            # Números del cartón
            p.setFont("Helvetica-Bold", 13)
            for fila in range(filas):
                for col in range(columnas):
                    numero = carton[fila][col]
                    # Texto oscuro con leve sombra blanca para contraste
                    p.setFillColorRGB(1, 1, 1)
                    p.drawCentredString(
                        tabla_x + col * lado_celda + lado_celda/2 + 0.7,
                        tabla_y - 10 - fila * lado_celda - lado_celda/2 + 4 - 0.7,
                        str(numero)
                    )
                    p.setFillColorRGB(0.15, 0.2, 0.3)
                    p.drawCentredString(
                        tabla_x + col * lado_celda + lado_celda/2,
                        tabla_y - 10 - fila * lado_celda - lado_celda/2 + 4,
                        str(numero)
                    )

        p.showPage()

    p.save()
    buffer.seek(0)
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='cartones_bingo.pdf'
    )

@app.route('/carton_bingo')
def carton_bingo():
    carton = generar_carton_bingo()
    return render_template('carton_bingo.html', carton=carton)
#
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

