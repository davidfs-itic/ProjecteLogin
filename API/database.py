import mysql.connector
from dotenv import load_dotenv
import os

def inicialitzar_base_dades(db_config):
    try:
        # Connectar a la base de dades
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()

        # Comprovar si la taula 'usuaris' existeix
        mycursor.execute("SHOW TABLES LIKE 'usuaris'")
        result = mycursor.fetchone()

        # Crear les taules si no existeixen
        if not result:
            mycursor.execute("""
                CREATE TABLE usuaris (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nom_usuari VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    contrassenya VARCHAR(255) NOT NULL,
                    token VARCHAR(255) NOT NULL,
                    validat BOOLEAN DEFAULT FALSE
                )
            """)
            mycursor.execute("CREATE TABLE passwords (flag VARCHAR(100))")
            mycursor.execute("INSERT INTO passwords (flag) VALUES ('It was good that all beautiful things were also a little sad. It made them seem more real.')")
            mydb.commit()
            print("Taules creades correctament.")
        else:
            print("Les taules ja existeixen.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            print("Connexió a la base de dades tancada.")