from flask import Flask, render_template, request, send_file
import segno
import io
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Esta ruta busca el archivo index.html dentro de la carpeta /templates
    return render_template('Index.html')

@app.route('/generar', methods=['POST'])
def generar():
    try:
        # Obtenemos los datos enviados desde el formulario HTML
        data = request.form.get('data')
        color_qr = request.form.get('color', '#000000') # Negro por defecto
        
        if not data:
            return "Error: No ingresaste datos", 400

        # Creamos el QR con nivel de error alto para mayor seguridad
        qr = segno.make(data, error='h')
        
        # Guardamos el resultado en un buffer de memoria (evita llenar el servidor de archivos)
        img_buf = io.BytesIO()
        qr.save(img_buf, kind='png', scale=10, dark=color_qr, light="white")
        img_buf.seek(0)
        
        return send_file(img_buf, mimetype='image/png')
    
    except Exception as e:
        return f"Ocurrió un error: {str(e)}", 500

if __name__ == "__main__":
    # IMPORTANTE: host='0.0.0.0' permite que el servicio sea visible en internet
    # El puerto lo asigna la plataforma (Railway/Render) automáticamente
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
