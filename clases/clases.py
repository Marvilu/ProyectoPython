from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, MappedAsDataclass
from sqlalchemy import create_engine, select
from datetime import date, datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from typing import Optional


class Base(MappedAsDataclass,DeclarativeBase):
    pass

class Persona(Base, order=True):
    __tablename__ = "usuarios"
    sort_index: Mapped[str] = mapped_column(init=False)
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    dni:Mapped[str]
    nombre:Mapped[str]
    apellido:Mapped[str]
    nacimiento:Mapped[date]
    correo:Mapped [str]
    contrasenia:Mapped [str]
    correo_enviado:Mapped [bool]
    tipo_usuario:Mapped [str]

    def __post_init__(self):
        self.sort_index=self.dni

    @classmethod
    def crear_usuario(cls):
        """Crea usuario y lo guarda en base de datos"""
        try:
            dni = input("\nDni: ")
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            fecha = input("Fecha de nacimienro (d/m/yyyy): ")
            correo = input("Correo electrónico: ")
            contrasenia=("Contraseña: ")
            contrasenia2=("Ingrese nuevamente contraseña: ")
            correo_enviado= False
            nacimiento= datetime.strptime(fecha, "%d/%m/%Y").date() 
            
            if contrasenia!= contrasenia2:        
                raise Exception("Las contraseñas no coinciden")
            
        except Exception as e:
            print("Error al crear usuario")
            print(e)
        else:
            usuario = cls(dni, nombre, apellido, nacimiento, correo, contrasenia, correo_enviado)
            with Session(engine) as session:
                session.add(usuario)
                session.commit()
                print("Se ha registrado cliente")

    @classmethod
    def enviar_mail_de_registro(cls, dni:str): 
         """envia mail al usuario seleccionado por dni"""
         with Session(engine) as session:
            try:
                consulta=select(cls).where(cls.dni == dni)
                per_1= session.scalars(consulta).one()
                correo_buscado=per_1.correo                               
            except Exception as e:
                print("El nombre del usuario no se encuentra en la base de datos")
            
            servidor = 'smtp.gmail.com'
            puerto = 587
            emisor = 'depruebacuenta712@gmail.com'
            contrasenia = 'jzpmjcnvuwcodesv'

            mail = MIMEMultipart()
            mail['from']= emisor
            mail['to']= correo_buscado
            mail['subject']='Datos del Usuario'

            texto= f'''
        Los datos del registro son:
            Dni:{per_1.dni}
            Nombre: {per_1.nombre}
            Apellido: {per_1.apellido}
            Nacimiento: {per_1.nacimiento}
            Correo electrónico: {per_1.correo}
            Contrasenia: {per_1.contrasenia}
            '''

            texto_a_insertar = MIMEText(texto, 'plain')
            mail.attach(texto_a_insertar)

            with smtplib.SMTP(servidor, puerto) as servidor:
                servidor.starttls()
                servidor.login(emisor, contrasenia)
                servidor.sendmail(emisor, correo_buscado, mail.as_string())
                per_1.correo_enviado= True
                session.commit()
                print("\n Correo enviado")

    @classmethod
    def modificar_atributos(cls, dni):
        """modifica atributos de cliente ingresado por dnio, si atributo vacio no modifica bd"""
        with Session(engine) as session:
            try:
                consulta=select(cls).where(cls.dni == dni)
                per_1= session.scalars(consulta).one()
                print(f'''
                Los datos del registro son:
                    Dni:{per_1.dni}
                    Nombre: {per_1.nombre}
                    Apellido: {per_1.apellido}
                    Nacimiento: {per_1.nacimiento}
                    Correo electrónico: {per_1.correo}
                    ''')
                print()

                print("Ingrese los datos que desee modificar:")
                dni=input("\nDni: ")
                if dni.isspace()==True:
                    per_1.dni = dni                

                nombre= input("Nombre: ")
                if nombre:
                    per_1.nombre = nombre
                   
                apellido= input("Apellido: ")
                if apellido:
                    per_1.apellido =apellido
                    
                fecha= input("Fecha de nacimienro (d/m/yyyy): ")
                if fecha:
                    nacimiento= datetime.strptime(fecha, "%d/%m/%Y").date()
                    per_1.nacimiento=nacimiento
                
                correo=input("Correo electrónico: ")
                if correo:
                    per_1.correo = correo

                session.commit()
                print("\n Se han modificado los atributos")
            except Exception as e:
                print("El DNI no está asociado a ningun cliente en la base de datos")


class Paciente(Persona,Base):
    __tablename__ = "pacientes"
    
    derivacion:Mapped[Optional[datetime]]= mapped_column(default=None)
    turno:Mapped[Optional[datetime]]= mapped_column(default=None)

    def __post_init__(self):
        super().__post_init__()

        
    @classmethod
    def solicitar_turno(cls,dni):
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
                    consulta=select(cls).where(cls.dni == dni)
                    per_1= session.scalars(consulta).one()
                    per_1.derivacion=derivacion
                    session.commit()
                    print("\n La derivación ha sido cargada. Se le informará por correo cuando se le asigne turno")
                except Exception as e:
                    print("La especialidad no ha sido cargada")

class Administrador(Persona,Base):
    __tablename__ = "administrador"
   
    def __post_init__(self):
        super().__post_init__()
    
    @classmethod
    def lista_pacientes(self)->str:
        """visualiza lista de pacientes ordenada por dni (cuyos turnos== vacio) y devuelve dni del seleccionado"""
        #acceder a la tabla pacientes, filtrar turnos ya asignados y retornar dni de paciente seleccionado

    def asignar_turno(dni):
        
        #acceder a tabla con turnos disponibles de cada especialidad????
        with Session(engine) as session:
            
            consulta="'select * FROM turnos_disponibles"
            turnos= session.scalars(consulta).all()
            print(sorted(turnos)) 
            
            #turno=turno_disponible

        #acceder a tabla pacientes?? y asignar turno traido de tabla de turnos disponibles
            try:
                consulta="'select * FROM pacientes WHERE dni=?', dni)"
                per_1= session.scalars(consulta).one()
               # per_1.turno=turno
                session.commit()
                print("\n Se asignó Turno correspondiente")
            except Exception as e:
                print("No ")

        #enviar correo una vez que el turno ha sido asignado



        
        




    
        



engine = create_engine("sqlite:///database-usuarios.db")

