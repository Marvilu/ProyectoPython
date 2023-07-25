import sqlite3



conexion = sqlite3.connect('database-usuarios.db')
cursor = conexion.cursor()

def consulta_disponibilidad(especialidad:str,dia:str):      
    try:
        with conexion:
            cursor.execute(f"SELECT horario, {dia} FROM {especialidad} ORDER BY id")
            turnos = cursor.fetchall()
            print("Disponibilidad de día " +dia+ ": ")  
            for turno in turnos:                         
                print(turno[0], turno[1])
            
    except Exception as e:
        print(e)        

def cambia_horario(especialidad:str):
    dia=input("dia: ")
    hora=input("horaa: ")
    try:
            with conexion:
                cursor.execute(f"UPDATE {especialidad} SET {dia} = 'ocupado' WHERE horario='{hora}'")
                conexion.commit()
                print("El horario ha sido deshabilitado de la grilla de disponibilidad")

            consulta_disponibilidad(especialidad,dia)                    
    except Exception as e:
                print(e) 

if __name__ == "__main__":
    try:
    #  dia=input("Seleccione día que desee conocer disponibilidad: ")
    #  consulta_disponibilidad("clinica",dia) 
        cambia_horario("clinica")  
    except Exception as e:
        print (e)