from clases.clases import Paciente, Turno, Administador
from validaciones import validar_usuario, validar_admin
from menu import menu_paciente, menu_admin

def main():
    
    opc=input(f"""Ingrese tipo de usuario:
                            1)Paciente
                            2)Administrador
                            ->
                         """)
    if opc=="1":
        tipo_usuario="paciente"
    elif opc=="2":
        tipo_usuario="administrador"
    else:
        print("Opción invalida")

        #ACCESO COMO PACIENTE

    if tipo_usuario=="paciente":
        opc=input(f"""Seleccione opción correspondiente:
                            1)Paciente Registrado
                            2)Crear Registro
                            ->
                         """)
        if opc=="1":
            correo = input("Correo electrónico: ") 
            contrasenia=input("Contraseña: ")
            validacion=validar_usuario(correo,contrasenia,"paciente")
            if validacion == True:
                print("Acceso Correcto")
                menu_paciente(correo)
              
        elif opc=="2":
            dni=Paciente.crear_usuario("paciente")
            Paciente.enviar_mail_de_registro(correo)
        else:
            print("Opción invalida")

        #ACCESO COMO ADMINISTRADOR

    if tipo_usuario=="administrador":
        acceso=False
        codigo=input("ingrese codigo de acceso de administrador: ")
        acceso=validar_admin(codigo)

        while acceso==False:
            acceso=validar_admin(codigo)
            codigo=input("ingrese codigo de acceso de administrador: ")

        opc=input(f"""Seleccione opción correspondiente:
                            1)Administrador Registrado
                            2)Crear Registro
                            ->
                         """)
        
        if opc=="1":
            correo = input("Correo electrónico: ") 
            contrasenia=input("Contraseña: ")
            validacion=validar_usuario(correo,contrasenia,"administrador")
            if validacion == True:
                print("Acceso Correcto")
                menu_admin(correo)
              
        elif opc=="2":
            Administador.crear_usuario("administrador")
        else:
            print("Opción invalida")
        
        








if __name__ == "__main__":
    main()