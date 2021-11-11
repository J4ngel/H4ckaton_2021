from flask import Flask, render_template, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def principal():
    return render_template('tienda.html')

# Yessid: Inicio de usuario (similar a "/")
@app.route('/usuario')
def usuario():
    return render_template('usuarioExterno.html')

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

if __name__ == '__main__':
    app.run(debug=True, port=8000)