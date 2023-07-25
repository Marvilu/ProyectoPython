
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from clases.clases import Usuario
engine = create_engine("sqlite:///database-usuarios.db")

def validar_usuario(usuario, contrasenia, tipo_usuario)->bool:
    with Session(engine) as session:
        try:
            cons= select(Usuario).where(Usuario.correo == usuario)
            persona=session.scalars(cons).first()
            if persona.contrasenia==contrasenia and persona.tipo_usuario== tipo_usuario:
                return True

        except Exception as e:
            print("No se encuentra usuario con ese correo")






    



