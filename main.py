import os
import hashlib
import db_manager
import verifications

from flask import Flask, render_template, request, redirect, url_for, session, flash
from markupsafe import escape
from flask_bootstrap import Bootstrap
from werkzeug.security import check_password_hash, generate_password_hash
from flask.helpers import get_env

app = Flask(__name__)
Bootstrap(app)
app.secret_key = os.urandom(24)

#---------------------------FUNCIONES UTILES JACKE--------------------------------
def confBd():
    path = ''
    if get_env == 'production':
        path = os.path.abspath(os.getcwd())
    return path
#-------------------------------------------------------------------------------


# Jacke: Pagina principal
@app.route('/')
def principal():
    return render_template('index.html')

# Yessid: Pagina de usuario externo
@app.route('/usuario')
def usuario():
    if 'user' in session and session['rol'] == 1:
        return render_template('usuarioExterno.html')
    else:
        return redirect('/login/dashboard')

# Yessid: Pagina de usuario interno
@app.route('/empleado')
def empleado():
    if 'user' in session and session['rol'] == 2:
        return render_template('usuarioInterno.html')
    else:
        return redirect('/login/dashboard')

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
        username = escape(request.form['username'])
        password = escape(request.form['password'])
        
        status_1 = verifications.empity_login(username,password)

        if not status_1['state']:
            flash(status_1['error'])
            redirect('/login')
        else:
            status_2 = db_manager.login_session(username,password)

            if not status_2['state']:
                flash(status_2['error'])
                return redirect('/login')

            else:
                session['user']=username
                session['name']=status_2['data'][1]
                session['rol']=status_2['data'][2]
                print("logueo con exito")

                if session['rol'] == 3:
                    return redirect('/login/dashboard')
                elif session['rol'] == 2:
                    return redirect('/empleado')
                else:
                    return redirect('/usuario')

    if 'user' in session:
        if session['rol']==3:
            return redirect('/login/dashboard')
        elif session['rol']==2:
            return redirect('/empleado')
        else:
            return redirect('/usuario')
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
@app.route('/registro/usuario', methods=['GET','POST'])
def registrarse():
    if request.method == 'POST':
        cedula      = escape(request.form['cedula'])
        name        = escape(request.form['name'])
        gender      = escape(request.form['gender'])
        birthday     = escape(request.form['birthday'])
        city        = escape(request.form['city'])
        adds        = escape(request.form['adds'])
        username        = escape(request.form['username'])
        phrase      = escape(request.form['phrase'])
        password    = escape(request.form['password'])
        check_pass  = escape(request.form['check_pass'])
        conditions  = escape(request.form.get('conditions'))
        rol = 1  # 1 -> usuario externo / 2 -> usuario interno / 3 -> Admin   

        status_1 = verifications.valid_reg_1(cedula,name,gender,birthday,city,adds,phrase,username,password,check_pass,conditions)
        if not status_1['state']:
            flash(status_1['error'])
            return redirect('/registrarse')
        else:
            hash_pass = generate_password_hash(password)
            hash_phrase = generate_password_hash(phrase)

            status_2 = db_manager.reg_1(cedula,name,gender,birthday,city,adds, username,hash_phrase,hash_pass,rol)           
            
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
        username        = escape(request.form['username'])
        phrase      = escape(request.form['phrase'])
        password    = escape(request.form['password'])
        check_pass  = escape(request.form['check_pass'])
        conditions  = escape(request.form.get('conditions'))
        rol = 2  # 1 -> usuario externo / 2 -> usuario interno / 3 -> admin  

        status_1 = verifications.valid_reg_2(cedula,name,job,gender,birthday,city,adds,username,phrase,password,check_pass,conditions)
        if not status_1['state']:
            flash(status_1['error'])
            return redirect('/registro/empleado')
        else:
            hash_pass = generate_password_hash(password)
            hash_phrase = generate_password_hash(phrase)

            status_2 = db_manager.reg_2(cedula,name,job,gender,birthday,city,adds,username,hash_phrase,hash_pass,rol)
        
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
@app.route('/login/dashboard', methods=['GET','POST'])
def dashboard():
    if request.method == 'POST':
        if 'user' in session:
            session.clear()
            flash('Sesión cerrada exitosamente!')
            return redirect('/login')
        else:
            flash("Primero debe iniciar sesion")
            return redirect('/login')

    if 'user' in session:
        if session['rol'] == 3:
            return render_template('dashboard/dashboard.html')
        elif session['rol'] == 2:
            return redirect('/empleado')
        else:
            return redirect('/')
    else:
        return redirect('/')

@app.route('/login/dashboard/productos/<tipo_producto>')
@app.route('/login/dashboard/productos')
def dashboard_productos(tipo_producto):
    if request.method == 'GET':
        columnas = []
        busqueda_columnas = db_manager.get_columns_productos()
        # Agrego a columnas los nombres de las columnas buscado en bd
        for i in busqueda_columnas:
            columnas.append(f'{i}')
        #Organizo la información mostrada por defecto, todos los médicos
        productos = []
        db_productos = db_manager.get_productos()
        for row in db_productos:
            productos.append(row)
        
        categoria = []
        for i in range(len(productos)):
            if productos [i][2] == tipo_producto:
                categoria.append(productos [i])
                
        return render_template('dashboard/dashboard_productos.html', columnas=columnas, productos=categoria)
    else:
        return 'Hola'
 
@app.route('/login/dashboard/empleados')
def dashboard_empleados():
    if request.method == 'GET':
        columnas = []
        busqueda_columnas = db_manager.get_columns_usuario()
        # Agrego a columnas los nombres de las columnas buscado en bd
        for i in busqueda_columnas:
            columnas.append(f'{i}')
        #Organizo la información mostrada por defecto, todos los médicos
        empleados = []
        db_empleados = db_manager.get_empleados()
        for row in db_empleados:
            empleados.append(row)
        
        return render_template('dashboard/dashboard_empleados.html', columnas=columnas, empleados=empleados)
    else:
        return 'Hola'

@app.route('/login/dashboard/clientes', methods = ['GET', 'POST'])
def dashboard_clientes():
    if request.method == 'GET':
        columnas = []
        busqueda_columnas = db_manager.get_columns_usuario()
        # Agrego a columnas los nombres de las columnas buscado en bd
        for i in busqueda_columnas:
            columnas.append(f'{i}')
        #Organizo la información mostrada por defecto, todos los médicos
        clientes = []
        db_clientes = db_manager.get_clientes()
        for row in db_clientes:
            clientes.append(row)
        
        return render_template('dashboard/dashboard_clientes.html', columnas=columnas, clientes=clientes)
    else:
        return 'Hola'
      #coincidencia = []
        '''global cedula_cliente 
        cedula_cliente = request.form['cliente_buscado']
        busqueda_cedula = db_manager.(cedula_a_buscar_paciente)
        if len(busqueda_cedula)>0:
            cond = True
            for i in range(len(busqueda_columnas)):
                coincidencia.append(f'{busqueda_cedula[0][i]}')
            return render_template("administradorPaciente.html", user=user(cedula_init), coincidencia=coincidencia, columnas=columnas,cond=cond)
        else:
            error = f'El usuario con la identificacion {cedula_a_buscar_paciente} no se encuentra registrado '
            return render_template("administradorPaciente.html", user=user(cedula_init), error = error)
    return render_template('dashboard/dashboard_clientes.html')'''

if __name__ == '__main__':
    app.run(debug=True, port=8000)