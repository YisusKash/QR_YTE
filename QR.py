from flask import Flask, render_template, request, send_file
import segno
import io

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generar', methods=['POST'])
def generar():
    data = request.form.get('data')
    tipo = request.form.get('tipo')
    color = request.form.get('color')
    
    qr = segno.make(data, error='h')
    img_buf = io.BytesIO()
    qr.save(img_buf, kind='png', scale=10, dark=color)
    img_buf.seek(0)
    return send_file(img_buf, mimetype='image/png')

if __name__ == "__main__":
    app.run()
