from clases.clases import Paciente, Administrador
from validaciones.validar_usuario import validar_usuario

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

    if tipo_usuario=="paciente":
        opc=input(f"""Seleccione opción correspondiente:
                            1)Paciente Registrado
                            2)Crear Registro
                            ->
                         """)
        if opc=="1":
            correo = input("Correo electrónico: ") 
            contrasenia=input("Contraseña: ")
            validacion=validar_usuario(correo,contrasenia,tipo_usuario)
            if validacion == True:
                print("Acceso Correcto")

                #llevar este menu a otro modulo
                opc=input(f"""Seleccione Acción que desea realizar:
                            1)Modificar datos de registro
                            2)Solicitar Turno
                            3)Visualizar estado de asignacion de turno
                            ->
                         """)
                if opc=="1":
                    Paciente.modificar_atributos()
                elif opc=="2":
                    Paciente.solicitar_turno(correo)
                elif opc=="3":
                    Paciente.visualizar_turno(correo)
                else:
                    print("Opción invalida")
        
        elif opc=="2":
            Paciente.crear_usuario()
        else:
            print("Opción invalida")






if __name__ == "__main__":
    main()