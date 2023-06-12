from clases.clases import Persona, Base
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, MappedAsDataclass
from sqlalchemy import create_engine, select
from datetime import date, datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from typing import Optional
from dataclasses import dataclass, field


class Paciente(Persona):
   
    derivacion:Mapped[Optional[datetime]]= mapped_column(default=None)
    turno:Mapped[Optional[datetime]]= mapped_column(default=None)

    def __post_init__(self):
        super().__post_init__()

        
    @classmethod
    #hacer una tabla con cada especialidad y horarios disponibles
    def solicitar_turno(cls,correo):
        """Permite al paciente seleccionar especialidad a la cual requiere un turno"""
        opcion=input(f"""Seleccione especialidad para la que requiere turno: 
                                1) Oftalmología
                                2) Otorrinolaringología
                                3) Odontología
                                4) Clínica
                                ->:                    """)
        
        if opcion not in range(1,4):
            print("Opción Incorrecta")
        else:
            if opcion=="1":
                derivacion="Oftalmo"
            elif opcion=="2":
                derivacion="Otorrino"
            elif opcion=="3":
                derivacion="Odonto"
            elif opcion=="4":
                derivacion="Clinica"

        with Session(engine) as session:
            try:
                consulta=select(cls).where(cls.correo == correo)
                per_1= session.scalars(consulta).one()
                per_1.derivacion=derivacion
                session.commit()
                print("\n La derivación ha sido cargada. Se le informará por correo cuando se le asigne turno")
            except Exception as e:
                print("La especialidad no ha sido cargada")

    @classmethod
    def visualizar_turno(cls,correo):
        with Session(engine) as session:
            try:
                consulta=select(cls).where(cls.correo == correo)
                per= session.scalars(consulta).one()
                turno=per.turno

                if turno is None:
                    print("El turno aun no ha sido asignado. Se le notificará a su casilla de correo electrónico")
                else:
                    print (turno.strftime( "Su turno es el día %d del mes %m a las %H:%M"))                  
            except Exception as e:
                print("Error al visualizar turno:" , e)


engine = create_engine("sqlite:///database-usuarios.db")


if __name__ == "__main__":
    try:
        Base.metadata.create_all(engine)
        print("BS creada")
        # tipo_usuario="paciente"
        # Paciente.crear_usuario(tipo_usuario)
    except Exception as e:
        print (e)
