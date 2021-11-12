import re

def valid_pass(password):
    expresion_regular = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
    if re.search(expresion_regular, password):
        return True
    else:
        return False

def valid_reg_1(cedula, name, gender, birthday, city, adds, phrase, password, check_pass, conditions):
    status = {'state':True, 'error': None}
    if conditions == 'None':
        status['state'] = False
        status['error'] = "Debe aceptar los terminos y condiciones"
        return status
    
    else:
        if len(cedula) == 0 or len(name) == 0 or len(gender) == 0 or len(city) == 0 or len(adds) == 0 or len(phrase) == 0 or len(password) == 0 or len(check_pass) == 0:
            status['state'] = False
            status['error'] = "Algunos campos estan vacíos, verifiquelos y trate de nuevo"
            return status

        else:
            if not valid_pass(password):
                status['state'] = False
                status['error'] = "La contraseña debe contener minimo 8 caracteres, entre ellos: numeros, letras (mayus y min) y un caracter especial"
                return status

            else:
                if password != check_pass:
                    status['state'] = False
                    status['error'] = "Las contraseñas no coinciden"
                    return status
                
                else:
                    return status