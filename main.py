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
    #     ced=escape(request.form['cedula'])
    #     pas=escape(request.form['contrasena'])
    #     result=db_manager.name_session(ced,pas)
    #     user=result[1]
    #     password=result[0]

    # return render_template('login.html')
        cedula = escape(request.form['cedula'])
        password = escape(request.form['password'])
        
        if cedula == "1234" and password=="1234":
            session['user'] = 1234
            session['rol'] = 3
            flash(f"logueado con exito {session['user']}: {session['rol']}")
            return redirect("/registro/empleado")
        else:
            flash("Credenciales invalidas!!")
            return redirect("/login")

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
            flash(status_1['error'])
            return redirect('/registrarse')
        else:
            hash_pass = generate_password_hash(password)
            hash_phrase = generate_password_hash(phrase)

            #status_2 = db_manager.reg_1(cedula,name,gender,birthday,city,adds,hash_phrase,hash_pass,rol)
            status_2 = {'state':True} #Linea SOLO PARA PRUEBAS
            if not status_2['state']:
                flash(status_2['error'])
                return redirect('/registrarse')
            else:
                if 'user' in session and session['rol'] == 3:  
                    flash("Registro exitoso, nuevo cliente agregado con exito")
                else:
                    flash("Registro exitoso, ahora puede dirigirse a login e iniciar sesión")
                return redirect('/registrarse')

    if 'user' in session and session['rol'] != 3:
        return redirect('/')
    else:
        return render_template('registrarse.html')

@app.route('/registro/empleado', methods=['GET', 'POST'])
def registro_empleado():
    if request.method == 'POST':
        cedula      = escape(request.form['cedula'])
        name        = escape(request.form['name'])
        job         = escape(request.form['job'])
        gender      = escape(request.form['gender'])
        birthday     = escape(request.form['birthday'])
        city        = escape(request.form['city'])
        adds        = escape(request.form['adds'])
        phrase      = escape(request.form['phrase'])
        password    = escape(request.form['password'])
        check_pass  = escape(request.form['check_pass'])
        conditions  = escape(request.form.get('conditions'))
        rol = 2  # 1 -> usuario externo / 2 -> usuario interno / 3 -> admin  

        status_1 = verifications.valid_reg_2(cedula,name,job,gender,birthday,city,adds,phrase,password,check_pass,conditions)
        if not status_1['state']:
            flash(status_1['error'])
            return redirect('/registro/empleado')
        else:
            hash_pass = generate_password_hash(password)
            hash_phrase = generate_password_hash(phrase)

            #status_2 = db_manager.reg_2(cedula,name,job,gender,birthday,city,adds,hash_phrase,hash_pass,rol)
            status_2 = {'state':True} #Linea SOLO PARA PRUEBAS
            if not status_2['state']:
                flash(status_2['error'])
                return redirect('/registro/empleado')
            else:
                flash("Registro exitoso, nuevo empleado agregado con exito")
                return redirect('/registro/empleado')

    if 'user' in session and session['rol'] != 3:
        return redirect('/')
    else:
        return render_template('registro_empleado.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)