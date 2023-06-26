def validar_admin(contrasenia)->bool:
    """ valida el acceso del administrador con contraseña unica "privado" """
    if contrasenia== "privado":
        return True
    else:
        raise Exception("Acceso inválido")
    
