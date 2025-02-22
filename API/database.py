import mysql.connector
from dotenv import load_dotenv
import os
import sys

def inicialitzar_base_dades(db_config):
    try:
        # Connectar al servidor de base de dades sense especificar la base de dades
        mydb = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        mycursor = mydb.cursor()

        # Comprovar si la base de dades existeix
        mycursor.execute(f"SHOW DATABASES LIKE '{db_config['database']}'")
        result = mycursor.fetchone()

        if not result:
            # Intentar crear la base de dades
            try:
                mycursor.execute(f"CREATE DATABASE {db_config['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
                print(f"Base de dades '{db_config['database']}' creada correctament.")
            except mysql.connector.Error as err:
                print(f"Error: No es pot crear la base de dades. Potser no tens els privilegis necessaris. Detalls: {err}")
                sys.exit(1)  # Finalitzar l'aplicació amb codi d'error 1

        # Connectar a la base de dades específica
        mydb.database = db_config['database']
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
        sys.exit(1)  # Finalitzar l'aplicació amb codi d'error 1

    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            print("Connexió a la base de dades tancada.")