from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, MappedAsDataclass,relationship, sessionmaker
from sqlalchemy import create_engine, select, ForeignKey, inspect
from datetime import date, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3
import smtplib
from typing import Optional, List
from dataclasses import dataclass





class Base(MappedAsDataclass,DeclarativeBase):
    pass

@dataclass
class Usuario(Base, order=True):
    __tablename__ = "usuarios"
    
    # sort_index: Mapped[str] = mapped_column(init=False)
    id: Mapped[int] = mapped_column(init=False, primary_key=True)

    dni:Mapped[str]
    nombre:Mapped[str]
    apellido:Mapped[str]
    nacimiento:Mapped[date]
    correo:Mapped[str]
    contrasenia:Mapped[str]
    type:Mapped[str]
    turnos: Mapped[List["Turno"]] = relationship("Turno", back_populates="paciente")
    # turnos: Mapped[Optional[List["Turno"]]] = relationship(cascade="all", back_populates="paciente")
    correo_enviado: Mapped[Optional[bool]] =mapped_column(default=None)
    tipo_usuario: Mapped[Optional[str]] =mapped_column(default=None)

    __mapper_args__={
        "polymorphic_identity": "usuario",
        "polymorphic_on": "type",
    }
    
    def __post_init__(self):
        self.sort_index=self.id

   
    @classmethod
    def crear_usuario(cls, tipo_usuario)->str:
        """Crea usuario y lo guarda en base de datos"""
        tipo_usuario=  tipo_usuario 

        try:
            print("Ingrese sus datos personales para realizar registro:")
            dni = input("\nDni: ")
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            fecha = input("Fecha de nacimiento (d/m/yyyy): ")
            nacimiento= datetime.strptime(fecha, "%d/%m/%Y").date()
            correo = input("Correo electrónico: ")         
            correo_enviado= False
            contrasenia=input("Contraseña: ")
            contrasenia2=input("Ingrese nuevamente contraseña: ")
            if contrasenia!=contrasenia2:
                print("¡Las contraseñas deben coincidir!")
                contrasenia2=input("Ingrese nuevamente contraseña: ")


        except Exception as e:
            print("Error al crear usuario")
            print(e)
        else:
            if not(dni or nombre or apellido or nacimiento or correo or contrasenia):
                print("Falta completar campo")
            else:
                if tipo_usuario=="paciente":
                    usuario = cls(turnos= [], dni=dni, nombre=nombre, apellido=apellido, nacimiento=nacimiento, correo=correo, contrasenia=contrasenia,type=tipo_usuario, correo_enviado=correo_enviado, tipo_usuario=tipo_usuario)
                else:
                    usuario = cls(dni=dni, nombre=nombre, apellido=apellido, nacimiento=nacimiento, correo=correo, contrasenia=contrasenia,type=tipo_usuario, correo_enviado=correo_enviado, tipo_usuario=tipo_usuario)

                with Session(engine) as session:
                    session.add(usuario)
                    session.commit()
                    print("Se ha registrado usuario")
                    
                    return dni

    @classmethod
    def enviar_mail_de_registro(cls, dni:str): 
         """envia mail al usuario seleccionado por dni"""
         with Session(engine) as session:
            try:
                consulta=select(cls).where(cls.dni == dni)
                per_1= session.scalars(consulta).one()
                correo_buscado=per_1.correo                               
            except Exception as e:
                print("El dni del usuario no se encuentra en la base de datos")
            
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
    def modificar_atributos(cls, correo:str):
        """modifica atributos de usuario ingresado por dni, si atributo vacio no modifica bd"""
        with Session(engine) as session:
            try:
                consulta=select(cls).where(cls.correo==correo)
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
                print("El DNI no está asociado a ningun usuario en la base de datos")



class Turno(Base):
    __tablename__ = "turno"
    
    turno_id: Mapped[int] = mapped_column(init=False, primary_key=True) #utilizo este para ordenar lista de administrador
    especialidad:Mapped[str]
    horario:Mapped[str] 
    paciente_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), init=False)
    paciente: Mapped["Usuario"] = relationship(back_populates="turnos")
    estado_turno:Mapped[Optional[bool]] =mapped_column(default=False) #si =false print sin asignar, si true, mostrar turno y para filtrar en lista administrador
    
    @classmethod
    def listado_sin_turno(cls):  #CORREGIR COMO SE MUESTRA LA LISTA
        """listado de pacientes sin turno asignado, ordenado por turno_id (orden de solicitud)"""
        print("lista de pacientes sin turno: ")
        with Session(engine) as session:        
             consulta=select(cls).where(cls.estado_turno==False).order_by(cls.turno_id)
             pacientes=session.scalars(consulta).all() 
             for paciente in pacientes:                 
                print("Id del paciente: ", paciente.paciente_id, " Especialidad requerida: ", paciente.especialidad)

    __mapper_args__ = {
        "polymorphic_identity": "turno",
    }

    @classmethod
    def consulta_disponibilidad(especialidad:str, dia:str):      
        try:
            with conexion:
                cursor.execute(f"SELECT horario, {dia} FROM {especialidad} ORDER BY id")
                turnos = cursor.fetchall()
                for turno in turnos:                              
                    print(turno[0], turno[1])
                
        except Exception as e:
            print(e)  
           
    @classmethod
    def asignar_turno(cls, paciente_id:str):#CORREGIR 
        """se asigna dia y hora de turno y se envia correo"""
        especialidad=input("Seleccione Especialidad: ")
        dia=input("Seleccione día en que desea asignar turno: ")

        cls.consulta_disponibilidad(especialidad,dia)
   
        hora=input("asigne hora como h-h: ")  
        horario= "Día: ", dia, "Hora: ", hora
        estado_turno=True

        with Session(engine) as session:        
            per_1 =session.scalars(select(cls). filter_by(cls.paciente_id==paciente_id)).first()
            turno=cls(especialidad, horario, estado_turno, per_1)
            session.add(turno)
            session.commit()
            print("Se ha asignado el turno correctamente")

                                    #Envío de correo con turno asignado           
            servidor = 'smtp.gmail.com'
            puerto = 587
            emisor = 'depruebacuenta712@gmail.com'
            contrasenia = 'jzpmjcnvuwcodesv'

            mail = MIMEMultipart()
            mail['from']= emisor
            mail['to']= per_1.correo
            mail['subject']='Turno Médico Asignado'
            texto= f'''         
            Su turno ha sido asignado.
            Especialidad:{turno.especialidad}
            Día y Horario del turno: {turno.horario} '''

            texto_a_insertar = MIMEText(texto, 'plain')
            mail.attach(texto_a_insertar)

            with smtplib.SMTP(servidor, puerto) as servidor:
                servidor.starttls()
                servidor.login(emisor, contrasenia)
                servidor.sendmail(emisor, per_1.correo, mail.as_string())
                session.commit()
                print("\n Correo enviado")
            print(e)  
            
        #Modifica grilla horario  FUNCION NO MODIFICA TABLA
        try:
            with conexion:
                cursor.execute(f"UPDATE {especialidad} SET {dia} = 'ocupado' WHERE horario={hora}")
                conexion.commit()
                print("El horario ha sido deshabilitado de la grilla de disponibilidad")
                
        except Exception as e:
            print(e) 

    @classmethod
    def eliminar_turno(cls, paciente_id:str, especialidad:str):
        with Session(engine) as session:
            consulta= select(cls).where(cls.paciente_id==paciente_id and cls.especialidad==especialidad)
            turno=session.scalars(consulta).first() 
            print(turno)
            print("Confirme día y hora del turno a eliminar: ")
            dia=input("Día: ")
            hora=input("Hora (h-h): ")                   
            session.delete(turno)
            session.commit()
            print("se eliminó el turno")

            #habilitar nuevamente el turno en la grilla de horarios 
        try:
            with conexion:
                cursor.execute(f"UPDATE {especialidad} SET {dia} = 'libre' WHERE horario={hora}")
                conexion.commit()
                print("El horario ha sido habilitado nuevamente en la grilla de disponibilidad")
                
        except Exception as e:
            print(e)
            
    @classmethod
    def consultar_estado_turno(cls, correo:str):

        with Session(engine) as session:   
            consulta =select(cls.horario, cls.especialidad, cls.estado_turno).where(Usuario.correo==correo)
            turnos= session.scalars(consulta).all()
            #quiero traer todos los turnos bajo el mismo id y mostrar estado y horario???
    
    @classmethod
    def solicitar_turno(cls, correo:str):
        especialidad=input(f"""Seleccione especialidad para la que requiere turno: 
                                1) Oftalmología
                                2) Otorrinolaringología
                                3) Odontología
                                4) Clínica
                                ->:                    """)
        
        with Session(engine) as session:        
            paciente =session.scalars(select(Usuario). filter_by(correo==correo)).first()
            turno=cls(especialidad, paciente)
            session.add(turno)
            session.commit()
            print("Se ha realizado la solicitud. Cuando se asigne un turno será notificado por correo")    
   

        


engine = create_engine("sqlite:///database-usuarios.db")
conexion = sqlite3.connect('database-usuarios.db')
cursor = conexion.cursor()


if __name__ == "__main__":
    Base.metadata.create_all(engine) 
    try:
        # dni=Usuario.crear_usuario("paciente")
        # print (dni)
        Usuario.enviar_mail_de_registro("123")
      
        # Turno.consulta_disponibilidad("clinica")
    except Exception as e:
        print (e)