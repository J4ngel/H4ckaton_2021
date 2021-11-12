from flask import Flask, render_template, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

# Jacke: Pagina principal
@app.route('/')
def principal():
    return render_template('index.html')

# Yessid: Pagina de usuario externo
@app.route('/usuario')
def usuario():
    return render_template('usuarioExterno.html')

# Yessid: Pagina de usuario interno
@app.route('/empleado')
def empleado():
    return render_template('usuarioInterno.html')

# Yessid: Pagina de productos (clientte)
@app.route('/productos')
def tienda():
    return render_template('tienda.html')

# Yessid: Pagina de productos (empleado)
@app.route('/productos/enlatados')
def precios():
    return render_template('productoEnlatado.html')

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')

# Yessid: Pagina de recuperar contraseña
@app.route('/login/recuperar')
def recuperar():
    return render_template('recuperar.html')

@app.route('/registrarse')
def registrarse():
    return render_template('registrarse.html')

# Jacke: Pagina de administrador
@app.route('/login/dashboard')
def dashboard():
    return render_template('dashboard/dashboard.html')

@app.route('/login/dashboard/productos')
def dashboard_productos():
    return render_template('dashboard/dashboard_productos.html')

@app.route('/login/dashboard/empleados')
def dashboard_empleados():
    return render_template('dashboard/dashboard_empleados.html')

@app.route('/login/dashboard/clientes')
def dashboard_clientes():
    return render_template('dashboard/dashboard_clientes.html')

@app.route('/registro/empleado')
def registro_empleado():
    return render_template('registro_empleado.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)