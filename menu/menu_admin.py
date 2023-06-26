from clases.clases import Usuario, Paciente, Turno, Administador
from sqlalchemy import create_engine

engine = create_engine("sqlite:///database-usuarios.db")


def menu_admin(correo):

    opc=input(f"""Seleccione Acción que desea realizar:
                                1)Modificar datos personales
                                2)Ver listado pacientes
                                ->
                            """)
    if opc=="1":
        Paciente.modificar_atributos()
    elif opc=="2":
        Turno.listado_sin_turno()   
        opc=input(f"""Seleccione Acción que desea realizar:
                                1)Buscar paciente por dni
                                2)Asignar turno
                                3)Eliminar turno
                                ->
                            """)

        if opc=="1":
            dni=input("Ingrese dni del paciente que desea encontrar: ")
            Paciente.buscar_por_dni(dni)
        elif opc=="2": 
            paciente_id=input("ingrese el id del paciente al que desea asignar turno: ")
            especialidad=input("Ingrese especialidad del turno a asignar: ")
            Turno.consulta_disponibilidad(especialidad)
            Turno.asignar_turno(paciente_id)  
        elif opc=="3":
            especialidad=input("Ingrese especialidad del turno a eliminar: ")
            paciente_id=input("ingrese el id del paciente al que desea eliminar el turno: ")
            Turno.eliminar_turno(paciente_id, especialidad)  
        else:
            print("Opción invalida")