from clases.clases import Paciente, Turno


def menu_paciente(correo):
    opc=input(f"""Seleccione Acción que desea realizar:
                                1)Modificar datos de registro
                                2)Solicitar Turno
                                3)Visualizar estado de asignacion de turno
                                ->
                            """)
    if opc=="1":
        Paciente.modificar_atributos()
    elif opc=="2":
        Turno.solicitar_turno(correo)
    elif opc=="3":
        Turno.consultar_estado_turno(correo)
    else:
        print("Opción invalida")