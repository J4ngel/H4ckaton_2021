import sqlite3
from sqlite3 import Error

import hashlib
from werkzeug.security import check_password_hash

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