import sqlite3
from sqlite3 import Error

import hashlib
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

def name_session(user, password):
    try:
        with sqlite3.connect("TJX_productos.db") as con:
            cur = con.cursor()
            query=cur.execute("SELECT Contraseña FROM Usuarios WHERE Correo=?",[user]).fetchone()
            if query!=None:
                if check_password_hash(query[0],password):
                    return user
                else:
                    return False
            else:
                return False
    except Error:
        return False