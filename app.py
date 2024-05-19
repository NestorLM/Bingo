import io
import Sorteo
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask import Flask, render_template, jsonify, send_file
from Cartela import generar_carton_bingo

app = Flask(__name__)

numeros_sorteados = set()

# Definimos el rango de letras
rangos_letras = {'B': (1, 18), 'I': (19, 36), 'N': (37, 54), 'G': (55, 72), 'O': (73, 90)}

@app.route('/')
def index():
    return render_template('index.html', rangos_letras=rangos_letras)  # Pasamos rangos_letras al contexto del template

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
    carton = generar_carton_bingo()

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Dibujar la tabla del cartón de bingo
    x_offset = 50
    y_offset = height - 100
    cell_width = 100
    cell_height = 40

    # Título
    p.setFont("Helvetica-Bold", 24)
    p.drawString(x_offset, y_offset, "Cartón de Bingo")
    
    y_offset -= 50

    # Encabezados de columnas
    columnas = ['B', 'I', 'N', 'G', 'O']
    p.setFont("Helvetica-Bold", 12)
    for i, columna in enumerate(columnas):
        p.drawString(x_offset + i * cell_width + 30, y_offset, columna)
    
    y_offset -= cell_height

    # Números del cartón
    p.setFont("Helvetica", 12)
    for fila in carton:
        for i, numero in enumerate(fila):
            p.drawString(x_offset + i * cell_width + 30, y_offset, str(numero))
        y_offset -= cell_height

    p.showPage()
    p.save()

    buffer.seek(0)
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='carton_bingo.pdf'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

