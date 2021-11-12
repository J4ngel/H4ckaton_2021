import sqlite3
from sqlite3 import Error

import hashlib
from werkzeug.security import check_password_hash

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
        
def name_session(ced, pas):
    try:
        with sqlite3.connect("/home/carlosortega/Documentos/hackaton_2021/H4ckaton_2021/orion.db") as con:
            cur = con.cursor()
            query=cur.execute("SELECT Contraseña,Username FROM Usuarios WHERE cedula=?",[ced]).fetchone()
            if query!=None:
                if query[0]==pas:
                    return query
                else:
                    return False
            else:
                return "No existe el usuario"
    except Error:
        return False