from sqlalchemy import create_engine, select, Column, Integer, String, inspect
from sqlalchemy.orm import Session, declarative_base, sessionmaker, exc


engine = create_engine("sqlite:///database-usuarios.db")
Base = declarative_base()


class Grilla(Base):
    especialidad=input("Ingrese especialidad de la que desea generar una grilla de horarios: ")
    __tablename__ = especialidad
    id = Column(Integer, primary_key=True)
    horario= Column(String)
    lunes  = Column(String)
    martes = Column(String)
    miercoles = Column(String)
    jueves = Column(String)
    viernes = Column(String)


    @classmethod
    def crear_grilla(cls):
        """Crea una grilla de lunes a viernes con 4 turnos para la especialidad que se indique"""
        

        with Session(engine) as session:
            grilla1 = cls(horario='9-10', lunes='libre', martes='libre', miercoles='libre', jueves='libre', viernes='libre')
            grilla2 = cls(horario='10-11', lunes='libre', martes='libre', miercoles='libre', jueves='libre', viernes='libre')
            grilla3 = cls(horario='11-12', lunes='libre', martes='libre', miercoles='libre', jueves='libre', viernes='libre')
            grilla4 = cls(horario='12-13', lunes='libre', martes='libre', miercoles='libre', jueves='libre', viernes='libre')
            
            session.add_all([grilla1, grilla2, grilla3, grilla4])
            session.commit()
            print("grilla de horarios creada")

    
        
    #
    # 
    # 
    # 
    # @classmethod
    # def deshabilitar_turno(cls, dia:str, hora:str):
    #      """cambiar de o a 1 cuando se asigna turno para deshabilitar de grilla"""
         
    #      with Session(engine) as session: 
    #       #COMO HACER CONSULTA SEGUN NOMBRE DE LA COLUMNA(dia) y hora
                   
    #         turno.horario ="1"
    #         session.commit()
    #         print("turno deshabilitado de grilla")
    





if __name__ == "__main__":
    Base.metadata.create_all(engine) 

    try:
        Grilla.crear_grilla()
        
    except Exception as e:
        print(e)
    
    
    
