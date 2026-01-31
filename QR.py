from flask import Flask, render_template, request, send_file
import segno
import io
import os

# Forzamos a Flask a buscar la carpeta de plantillas correctamente
app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generar', methods=['POST'])
def generar():
    try:
        data = request.form.get('data')
        color = request.form.get('color', '#000000')
        
        qr = segno.make(data, error='h')
        img_buf = io.BytesIO()
        qr.save(img_buf, kind='png', scale=10, dark=color)
        img_buf.seek(0)
        return send_file(img_buf, mimetype='image/png')
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Railway usa la variable PORT, si no existe usamos 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
