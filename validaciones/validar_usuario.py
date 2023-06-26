
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from clases import Persona
engine = create_engine("sqlite:///database.db")

def validar_usuario(usuario, contrasenia, tipo_usuario)->bool:
    with Session(engine) as session:
        try:
            cons= select(Persona).where(Persona.correo == usuario)
            persona=session.scalars(cons).one()
            if persona.contrasenia==contrasenia and persona.tipo_usuario== tipo_usuario:
                return True

        except Exception as e:
            print("No se encuentra usuario con ese correo")






    



