import io
import Sorteo
import pdfkit
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
    rendered = render_template('pdf_template.html', carton=carton)
    
    # Especifica la ruta a wkhtmltopdf si no está en tu PATH
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdf = pdfkit.from_string(rendered, False, configuration=config)
    
    return send_file(
        io.BytesIO(pdf),
        mimetype='application/pdf',
        as_attachment=True,
        download_name='carton_bingo.pdf'
    )

if __name__ == '__main__':
    app.run(debug=True)
