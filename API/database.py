import mysql.connector
import logging
from dotenv import load_dotenv
import os
import sys

# Configura el logger per escriure a stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)  # Escriu els logs a stdout
    ]
)



def inicialitzar_base_dades(db_config):
    try:
        # Connectar al servidor de base de dades sense especificar la base de dades
        mydb = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            collation='utf8mb4_general_ci'
        )
    except mysql.connector.Error as err:
        logging.error(f"Error de connexió a la base de dades: {err}")
        sys.exit(1)  # Finalitzar l'aplicació amb codi d'error 1

    try:
 
        mycursor = mydb.cursor()

        # Comprovar si la base de dades existeix
        mycursor.execute(f"SHOW DATABASES LIKE '{db_config['database']}'")
        result = mycursor.fetchone()

        if not result:
            # Intentar crear la base de dades
            try:
                mycursor.execute(f"CREATE DATABASE {db_config['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
                logging.info(f"Base de dades '{db_config['database']}' creada correctament.")
            except mysql.connector.Error as err:
                logging.error(f"Error: No es pot crear la base de dades. Potser no tens els privilegis necessaris. Detalls: {err}")
                sys.exit(1)  # Finalitzar l'aplicació amb codi d'error 1
        else:
            logging.info("La base de dades ja existeix.")

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
            logging.info("Taules creades correctament.")
        else:
            logging.info("Les taules ja existeixen.")

    except mysql.connector.Error as err:
        logging.error(f"Error: {err}")
        sys.exit(1)  # Finalitzar l'aplicació amb codi d'error 1

    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            logging.info("Connexió a la base de dades tancada.")