import sqlite3
from sqlite3 import Error

import hashlib
from werkzeug.security import check_password_hash

from flask import g
import main


#----->REGISTRO DE UN USUARIO EXTERNO (CLIENTE)
def reg_1(cedula, name, gender, birthday, city, adds, phrase, password, rol):
    status={'state':True, 'error':None}
    try:
        with sqlite3.connect("orion.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Usuarios(Cedula, Nombre_y_apellido, Sexo, Fecha_de_nacimiento, Direccion, Ciudad, Contraseña, rol) VALUES (?,?,?,?,?,?,?,?)",(cedula,name,gender,birthday,adds,city,password, rol))
            con.commit()
            return status
            
    except Error:
        status['state'] = False
        status['error'] = "Algo salió mal" + Error
        return status

#----->REGISTRO DE UN USUARIO INTERNO (EMPLEADO)
def reg_2(cedula, name, job, gender, birthday, city, adds, phrase, password, rol):
    status={'state':True, 'error':None}
    try:
        with sqlite3.connect("orion.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Usuarios(Cedula, Nombre_y_apellido, Sexo, Fecha_de_nacimiento, Direccion, Ciudad, Contraseña, rol, Cargo) VALUES (?,?,?,?,?,?,?,?,?)",(cedula,name,gender,birthday,adds,city,password,rol,job))
            con.commit()
            return status
            
    except Error:
        status['state'] = False
        status['error'] = "Algo salió mal" + Error
        return status
        
def login_session(cedula, password):
    status = {'state':True, 'error':None, 'data':None}
    try:
        with sqlite3.connect("orion.db") as con:
            cur = con.cursor()
            query=cur.execute("SELECT Contraseña, Nombre_y_apellido, rol FROM Usuarios WHERE Cedula=?",[cedula]).fetchone()
            if query!=None:
                if check_password_hash(query[0],password):
                    status['data']=query
                    return status
                else:
                    status['state'] = False
                    status['error'] = "Credenciales invalidas verifique la cedula y/o la contraseña"
                    return status
                    
            else:
                status['state'] = False
                status['error'] = "Credenciales invalidas verifique la cedula y/o la contraseña"
                return status
        
    except Error:
        status['state'] = False
        status['error'] = "Algo salió mal "+ Error
        return status

#-----------------------------Administrador-----------------------------------
def sql_connection():
    try:
        if 'con' not in g:
            path = main.confBd()
            g.con = sqlite3.connect(path + "orion.db")
        return g.con
    except Error:
        print(Error)

def get_columns_usuario():
    strsql = 'select * from Usuarios'
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    names = list(map(lambda x: x[0], cursor.description))
    return names

def sql_search_user(cedula):
    strsql = 'select * from Usuarios where Cedula = ?', (cedula,)
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(*strsql)
    response = cursor.fetchall()
    return response

def get_clientes():
    strsql = 'select * from Usuarios where rol = ?',('1',)
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(*strsql)
    response = cursor.fetchall()
    return response