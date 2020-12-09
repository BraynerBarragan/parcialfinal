from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('login.html')
    
@app.route('/registrarse')
def registro():
    return render_template('registro.html')

@app.route('/index')
def inicio():
    return render_template('enseccion/index.html')

@app.route('/categorias')
def categorias():
    return render_template('enseccion/admin/categorias.html')

@app.route('/productos')
def productos():
    return render_template('enseccion/admin/productos.html')

@app.route('/perfil')
def editar_perfil():
    return render_template('enseccion/editarusuario.html')





app.run(debug=True, port='5100')