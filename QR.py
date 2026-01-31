from flask import Flask, render_template, request, send_file
import segno
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    tipo = request.form.get('tipo')
    contenido = request.form.get('contenido')
    color = request.form.get('color', '#000000')
    
    # Lógica según tipo
    if tipo == 'wifi':
        ssid = request.form.get('ssid')
        password = request.form.get('password')
        qr = segno.make_wifi(ssid=ssid, password=password, security='WPA')
    else:
        qr = segno.make(contenido, error='h')

    img_buf = io.BytesIO()
    qr.save(img_buf, kind='png', scale=10, dark=color)
    img_buf.seek(0)
    
    return send_file(img_buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
