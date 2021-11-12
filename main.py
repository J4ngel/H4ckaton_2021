import os
import hashlib
import db_manager
import verifications

from flask import Flask, render_template, request, redirect, url_for, session, flash
from markupsafe import escape
from flask_bootstrap import Bootstrap
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
Bootstrap(app)
app.secret_key = os.urandom(24)

@app.route('/')
def principal():
    return render_template('tienda.html')

# Yessid: Inicio de usuario (similar a "/")
@app.route('/usuario')
def usuario():
    return render_template('usuarioExterno.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        cedula = escape(request.form['cedula'])
        password = escape(request.form['password'])
        

    if 'user' in session:
        return redirect('/') #Se redirige al perfil
    else:
        return render_template('login.html')

# Yessid: Pagina de recuperar contraseña
@app.route('/login/recuperar')
def recuperar():
    return render_template('recuperar.html')

@app.route('/registrarse', methods=['GET','POST'])
def registrarse():
    if request.method == 'POST':
        cedula      = escape(request.form['cedula'])
        name        = escape(request.form['name'])
        gender      = escape(request.form['gender'])
        birthday     = escape(request.form['birthday'])
        city        = escape(request.form['city'])
        adds        = escape(request.form['adds'])
        phrase      = escape(request.form['phrase'])
        password    = escape(request.form['password'])
        check_pass  = escape(request.form['check_pass'])
        conditions  = escape(request.form.get('conditions'))
        rol = 1  # 1 -> usuario externo / 2 -> usuario externo / 3 -> usuario externo   

        status_1 = verifications.valid_reg_1(cedula,name,gender,birthday,city,adds,phrase,password,check_pass,conditions)
        if not status_1['state']:
            print(status_1['error'])
        else:
            hash_pass = generate_password_hash(password)
            hash_phrase = generate_password_hash(phrase)

            status_2 = db_manager.reg_1(cedula,name,gender,birthday,city,adds,hash_phrase,hash_pass,rol)
            
            if not status_2['state']:
                print(status_2['error'])
            else:
                print("Registro exitoso")

    if 'user' in session:
        return redirect('/')
    else:
        return render_template('registrarse.html')

@app.route('/registro/empleado')
def registro_empleado():
    return render_template('registro_empleado.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)