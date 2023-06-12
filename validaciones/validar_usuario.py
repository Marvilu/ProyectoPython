import sqlite3

def validar_usuario(usuario, contrasenia, tabla_usuario)->bool:
    """ compara la contraseña ingresada con la que le corresponde al correo ingresado en la BD"""

    conn = sqlite3.connect('database-usuarios.db')
    cursor = conn.cursor()
    consulta = "SELECT contrasenia FROM {} WHERE correo=?".format(tabla_usuario)
    cursor.execute(consulta, (usuario,))
    contrasenia_encontrada = cursor.fetchone()

    if contrasenia_encontrada[0]==contrasenia:
        return True
    else:
        raise Exception("Contraseña Incorrecta")

    



