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
    if request.method == 'POST':
        cedula = escape(request.form['cedula'])
        password = escape(request.form['password'])
        
        status_1 = verifications.empity_login(cedula,password)

        if not status_1['state']:
            flash(status_1['error'])
            redirect('/login')
        else:
            status_2 = db_manager.login_session(cedula,password)

            if not status_2['state']:
                flash(status_2['error'])
                return redirect('/login')

            else:
                session['user']=cedula
                session['name']=status_2['data'][1]
                session['rol']=status_2['data'][2]
                print("logueo con exito")
                return redirect('/')

    if 'user' in session:
        return redirect('/') #Se redirige al perfil
    else:
        return render_template('login.html')
        
@app.route('/login/recuperar_usuario', methods=['POST'])
def recuperar_usuario():
    name = escape(request.form['name'])
    birthday= escape(request.form['birthday'])
    phrase = escape(request.form['phrase'])

    status_1 = verifications.empity_recuperar_info(name,birthday,phrase)

    if not status_1['state']:
        flash(status_1['error'])
        return redirect('/login')
    else:
        status_2 = db_manager.recuperar_usuario(name,birthday,phrase)
        
        if not status_2['state']:
            flash(status_2['error'])
            return redirect('/login')
        else:
            flash(f"Su usuario es: {status_2['data'][0]}")
            return redirect('/login')

@app.route('/login/recuperar_contraseña', methods=['POST'])
def verificar_persona():
    name = escape(request.form['name'])
    birthday= escape(request.form['birthday'])
    phrase = escape(request.form['phrase'])

    status_1 = verifications.empity_recuperar_info(name,birthday,phrase)

    if not status_1['state']:
        flash(status_1['error'])
        return redirect('/login')
    else:
        status_2 = db_manager.recuperar_usuario(name,birthday,phrase)
            
        if not status_2['state']:
            flash(status_2['error'])
            return redirect('/login')
        else:
            session['valid_change']=True
            session['id_user'] = status_2['data'][1]
            return redirect('/login/cambio_contraseña')

@app.route('/login/cambio_contraseña', methods=['GET', 'POST'])
def recuperar_pass():
    if request.method == 'POST':
        password = escape(request.form['password'])
        check_pass= escape(request.form['check_pass'])
        
        status_1 = verifications.valid_recuperar_pass(password, check_pass)

        if not status_1['state']:
            flash(status_1['error'])
            return redirect('/login/cambio_contraseña')
        else:
            hash_pass = generate_password_hash(password)
            status_2 = db_manager.recuperar_pass(hash_pass,session['id_user'])

            if not status_2['state']:
                flash(status_2['error'])
                return redirect('/login/cambio_contraseña')
            else:
                session.pop('valid_change')
                session.pop('id_user')
                flash(status_2['data'])
                return redirect('/login')

    if 'valid_change' in session:
        return render_template('recuperar.html')
    else:
        flash("primero debe ingresar los datos dispuestos en el apartado recuperar información")
        return redirect('/login')

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

            status_2 = db_manager.reg_1(cedula,name,gender,birthday,city,adds,hash_phrase,hash_pass,rol)           
            
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

if __name__ == '__main__':
    app.run(debug=True, port=8000)